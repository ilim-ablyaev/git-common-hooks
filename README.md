# Git Hooks Setup

## Stop Writing Hook Setup Docs! 🚀

Tired of writing documentation on how to set up Git hooks? Make them part of your repository and just tell your team to run a script!

## Problem Statement

Git does not allow committing the `.git/hooks` directory, making it difficult to share project-specific hooks among team members. This script ensures that hooks are stored in a version-controlled `hooks` directory and automatically linked to `.git/hooks`, so everyone can set them up in seconds.

## Installation

1. Clone this repository (or navigate to your existing repo).
2. Run the setup script using Python:
   
   ```sh
   python git_common_hooks.py
   ```

   If you want to explicitly create hooks or set up symbolic links separately:
   
   ```sh
   python git_common_hooks.py --mode create   # Only create hooks
   python git_common_hooks.py --mode setup    # Only set up symbolic links
   ```

3. The script will:
   - Create a `hooks` directory in the repository root.
   - Set up default Git hooks (`post-checkout`, `post-commit`, `post-merge`, `pre-push`).
   - Add a `functions.sh` file to handle local hook execution.
   - Add `hooks/local` to `.gitignore` to prevent accidental commits.
   - If `.git/hooks` exists, it will be backed up before creating a symbolic link.

## Custom Options

- **Specify a custom hooks directory:**
  
  If you want to use a different directory for hooks, specify it with `--directory`:
  
  ```sh
  python git_common_hooks.py --directory my_hooks
  ```

- **Reset existing hooks:**
  
  If hooks already exist and you want to overwrite them, use the `--reset` flag:
  
  ```sh
  python git_common_hooks.py --reset
  ```

## Default Hooks

The following hooks are set up by default:

- **post-checkout**: Ensures `git-lfs` is available and runs `git lfs post-checkout`.
- **post-commit**: Runs `git lfs post-commit`.
- **post-merge**: Ensures `git-lfs` is available and runs `git lfs post-merge`.
- **pre-push**: Ensures `git-lfs` is available and runs `git lfs pre-push`.

Each hook also executes local hooks stored in `hooks/local`.

## Local Hooks

To add a custom hook for `post-checkout`, create `hooks/local/post-checkout`:

```sh
#!/bin/sh
echo "Example post-checkout hook! Happy coding"
```

Make sure it is executable:

```sh
chmod +x hooks/local/post-checkout
```

## Uninstalling

To remove the custom hooks setup:

```sh
rm -rf hooks .git/hooks
```

If needed, restore the backup of `.git/hooks`:

```sh
mv .git/hooks_backup_<timestamp> .git/hooks
```

## License

MIT License

