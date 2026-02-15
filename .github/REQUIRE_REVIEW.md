# Pull Request Review Policy

This project requires **maintainer approval** before any pull request can be merged.

## Branch protection (set in GitHub)

To enforce this, configure branch protection on your default branch:

1. Go to **Settings** → **Branches** → **Add rule** (or edit the existing rule)
2. Branch name pattern: `main` or `master`
3. Enable:
   - **Require a pull request before merging**
   - **Require approvals** (set to 1)
   - **Require review from Code Owners** (optional but recommended)
4. Save

## CODEOWNERS

The [CODEOWNERS](/CODEOWNERS) file lists reviewers. Replace `@your-github-username` with your GitHub username so you are automatically requested to review every PR.
