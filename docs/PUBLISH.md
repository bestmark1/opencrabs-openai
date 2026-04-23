# Publish

## Safe publication flow

1. Keep the live FitMentor support-agent untouched.
2. Develop extraction only in this separate repository.
3. Publish this repository under a new GitHub repo.
4. Continue moving generic logic here in small passes.
5. Do not switch production to this repo until project hooks are implemented.

## Commands

```bash
cd /tmp/opencrabs-agent-base
git status
git remote add origin git@github.com:<your-org-or-user>/opencrabs-agent-base.git
git push -u origin main
```

## If using GitHub CLI

```bash
gh auth login
gh repo create opencrabs-agent-base --public --source=. --remote=origin --push
```
