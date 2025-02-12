# Git Hooks Setup

This repository includes a script to set up local Git hooks. The script creates a `hooks` directory, configures symbolic links to `.git/hooks`, and ensures proper integration with Git LFS.

## Installation

1. Clone this repository (or navigate to your existing repo).

2. Run the setup script using Python:

   ```sh
   python script.py
   ```

   If you want to explicitly create hooks or set up symbolic links separately:

   ```sh
   python script.py --mode create   # Only create hooks
   python script.py --mode setup    # Only set up symbolic links
   ```

3. The script will:

   - Create a `hooks` directory in the repository root.
   - Set up default Git hooks (`post-checkout`, `post-commit`, `post-merge`, `pre-push`).
   - Add a `functions.sh` file to handle local hook execution.
   - Add `hooks/local` to `.gitignore` to prevent accidental commits.
   - If `.git/hooks` exists, it will be backed up before creating a symbolic link.

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

