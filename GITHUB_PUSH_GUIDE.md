# GitHub Push Guide 📤

## Quick Push Workflow (3 Commands)

### Step 1: Check What Changed
```bash
git status
```
Shows which files were modified/added.

### Step 2: Add All Changes
```bash
git add .
```
Adds all modified and new files to staging.

### Step 3: Commit and Push
```bash
git commit -m "Your descriptive message here"
git push
```

**Done!** Your changes are now on GitHub.

---

## Detailed Workflow

### 1. Check Status
```bash
git status
```
**What you'll see:**
- `M` = Modified file
- `??` = New untracked file
- `A` = Added file (staged)

### 2. Add Changes
```bash
# Add all changes
git add .

# OR add specific files
git add filename1.py filename2.tsx

# OR add by directory
git add backend/
git add frontend/
```

### 3. Commit Changes
```bash
# Good commit messages:
git commit -m "Add cross-platform setup scripts"
git commit -m "Fix dashboard metrics display"
git commit -m "Update README with setup instructions"
git commit -m "Add bias analysis filtering feature"
```

**Commit Message Tips:**
- ✅ Be descriptive: "Add feature X" not "update"
- ✅ Use present tense: "Add" not "Added"
- ✅ Keep it short (50 chars or less for summary)

### 4. Push to GitHub
```bash
git push
```

If it's your first push to a branch:
```bash
git push -u origin main
# or
git push -u origin master
```

---

## Common Scenarios

### Scenario 1: Daily Workflow
```bash
# Make your changes in code...

# Check what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Fix dashboard API endpoint"

# Push to GitHub
git push
```

### Scenario 2: Multiple Changes
```bash
# Add specific files
git add backend/app/main.py
git add frontend/app/dashboard/page.tsx

# Commit
git commit -m "Update dashboard and backend config"

# Push
git push
```

### Scenario 3: New Files
```bash
# New files need to be added
git add new-file.py
git add new-directory/

# Commit
git commit -m "Add new feature files"

# Push
git push
```

### Scenario 4: Pull Before Push (Important!)
```bash
# Always pull first to get teammate's changes
git pull

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge teammate's changes"
git push
```

---

## Before Pushing Checklist

✅ **Check what you're committing:**
```bash
git status
```

✅ **Review your changes:**
```bash
git diff
```

✅ **Make sure you're on the right branch:**
```bash
git branch
```

✅ **Pull latest changes first:**
```bash
git pull
```

✅ **Test your changes work:**
- Start backend and frontend
- Test the feature you changed
- Make sure nothing broke

---

## What NOT to Commit

These files are in `.gitignore` (don't commit them):
- ❌ `.env` files (contain API keys)
- ❌ `*.db` files (database files)
- ❌ `node_modules/` (dependencies)
- ❌ `venv/` (Python virtual environment)
- ❌ `.next/` (Next.js build files)
- ❌ `__pycache__/` (Python cache)

**Good!** These are automatically ignored.

---

## Branch Workflow (Optional)

### Create Feature Branch
```bash
git checkout -b feature/new-feature
# Make changes...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

### Switch Back to Main
```bash
git checkout main
```

### Merge Feature Branch
```bash
git merge feature/new-feature
git push
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| **Check status** | `git status` |
| **Add all changes** | `git add .` |
| **Commit** | `git commit -m "message"` |
| **Push** | `git push` |
| **Pull latest** | `git pull` |
| **See changes** | `git diff` |
| **See commit history** | `git log` |

---

## Troubleshooting

### "Your branch is ahead of origin"
**Solution:**
```bash
git push
```

### "Your branch is behind origin"
**Solution:**
```bash
git pull
# Resolve any conflicts
git add .
git commit -m "Merge remote changes"
git push
```

### "Merge conflicts"
**Solution:**
1. Open conflicted files
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Resolve conflicts manually
4. Save files
5. `git add .`
6. `git commit -m "Resolve merge conflicts"`
7. `git push`

### "Permission denied"
**Solution:**
- Check you're logged into GitHub
- Verify SSH keys or HTTPS credentials
- Check repository permissions

### "Nothing to commit"
**Solution:**
- All changes are already committed
- Or no files were modified
- Check `git status` to verify

---

## Best Practices

1. ✅ **Pull before push** - Always get latest changes first
2. ✅ **Commit often** - Small, frequent commits are better
3. ✅ **Write good messages** - Describe what changed and why
4. ✅ **Test before push** - Make sure your changes work
5. ✅ **Don't commit secrets** - Never commit `.env` files or API keys

---

## Quick Push Script (Optional)

Create a file `quick-push.bat` (Windows) or `quick-push.sh` (Mac/Linux):

**Windows (`quick-push.bat`):**
```batch
@echo off
echo Checking status...
git status
echo.
echo Adding all changes...
git add .
echo.
set /p message="Enter commit message: "
git commit -m "%message%"
echo.
echo Pushing to GitHub...
git push
echo.
echo Done!
pause
```

**Mac/Linux (`quick-push.sh`):**
```bash
#!/bin/bash
echo "Checking status..."
git status
echo ""
echo "Adding all changes..."
git add .
echo ""
read -p "Enter commit message: " message
git commit -m "$message"
echo ""
echo "Pushing to GitHub..."
git push
echo ""
echo "Done!"
```

Then just run: `quick-push.bat` or `./quick-push.sh`

---

**That's it!** Just 3 commands: `git add .`, `git commit -m "message"`, `git push` 🚀

