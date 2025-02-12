import os
import sys
import argparse
import shutil

def create_local_hooks(directory, reset):
    repo_root = os.popen("git rev-parse --show-toplevel").read().strip()
    if not repo_root:
        print("Not a Git repository.")
        sys.exit(1)

    hooks_dir = directory or os.path.join(repo_root, "hooks")
    local_dir = os.path.join(hooks_dir, "local")
    os.makedirs(local_dir, exist_ok=True)

    gitignore_path = os.path.join(repo_root, ".gitignore")
    gitignore_entry = "hooks/local\n"

    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write(gitignore_entry)
    else:
        with open(gitignore_path, "r+") as f:
            content = f.read()
            if gitignore_entry.strip() not in content:
                f.write(f"\n{gitignore_entry}")

    functions_sh = os.path.join(hooks_dir, "functions.sh")
    if not os.path.exists(functions_sh) or reset:
        with open(functions_sh, "w") as f:
            f.write("function run_local_hook() {\n  local_hook=$(dirname $0)/local/$(basename $0)\n  test -f $local_hook && $local_hook \"$@\" || true\n}\n")

    local_post_checkout = os.path.join(local_dir, "post-checkout")
    if not os.path.exists(local_post_checkout) or reset:
        with open(local_post_checkout, "w") as f:
            f.write("#!/bin/sh\necho \"Example post-checkout hook! Happy coding\"\n")
        os.chmod(local_post_checkout, 0o755)

    git_lfs_check = "command -v git-lfs >/dev/null 2>&1 || { echo >&2 \"\nThis repository is configured for Git LFS but 'git-lfs' was not found on your path. If you no longer wish to use Git LFS, remove this hook by deleting the '$0' file in the hooks directory (set by 'core.hookspath'; usually '.git/hooks').\n\"; exit 2; }\n"
    git_lfs_command = "git lfs $0 \"$@\"\n"
    source_local_hook = "source $(dirname $0)/functions.sh\nrun_local_hook\n"

    default_hooks = {
        "post-checkout": f"#!/bin/sh\n{git_lfs_check}\n{git_lfs_command.format('$0')}\n{source_local_hook}",
        "post-commit": f"#!/bin/sh\n{git_lfs_command.format('post-commit')}\n{source_local_hook}",
        "post-merge": f"#!/bin/sh\n{git_lfs_check}\n{git_lfs_command.format('$0')}\n{source_local_hook}",
        "pre-push": f"#!/bin/sh\n{git_lfs_check}\n{git_lfs_command.format('$0')}\n{source_local_hook}"
    }

    for hook, content in default_hooks.items():
        hook_path = os.path.join(hooks_dir, hook)
        if not os.path.exists(hook_path) or reset:
            with open(hook_path, "w") as f:
                f.write(content)
            os.chmod(hook_path, 0o755)

    print(f"Created local hooks directory at: {local_dir}")

def setup_local_hooks(directory):
    repo_root = os.popen("git rev-parse --show-toplevel").read().strip()
    if not repo_root:
        print("Not a Git repository.")
        sys.exit(1)

    git_hooks_dir = os.path.join(repo_root, ".git", "hooks")
    project_hooks_dir = directory or os.path.join(repo_root, "hooks")

    if not os.path.exists(project_hooks_dir):
        print(f"Hooks directory '{project_hooks_dir}' not found.")
        sys.exit(1)

    if os.path.exists(git_hooks_dir) and not os.path.islink(git_hooks_dir):
        backup_dir = os.path.join(repo_root, ".git", f"hooks_backup_{int(os.path.getmtime(git_hooks_dir))}")
        shutil.move(git_hooks_dir, backup_dir)
        print(f"Existing .git/hooks directory backed up to: {backup_dir}")

    os.symlink(project_hooks_dir, git_hooks_dir)
    print(f"Git hooks directory is now linked to: {project_hooks_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["create", "setup"], help="Mode to run: create or setup (if omitted, both will be executed)")
    parser.add_argument("--directory", help="Optional directory for hooks")
    parser.add_argument("--reset", action="store_true", help="Reset existing hooks if set")
    args = parser.parse_args()

    if args.mode == "create" or args.mode is None:
        create_local_hooks(args.directory, args.reset)
    if args.mode == "setup" or args.mode is None:
        setup_local_hooks(args.directory)
