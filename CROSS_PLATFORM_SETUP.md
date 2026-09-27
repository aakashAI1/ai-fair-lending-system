# Cross-Platform Setup Guide

This guide ensures the project works seamlessly on **Windows**, **Mac**, and **Linux**.

## 🔧 Automatic Line Ending Handling

The project uses `.gitattributes` to automatically handle line endings:
- **Windows**: Files use CRLF (`\r\n`)
- **Mac/Linux**: Files use LF (`\n`)
- Git automatically converts based on your OS

**No action needed** - Git handles this automatically when you clone or pull.

## 🚀 Quick Setup

### Windows

```cmd
# Run the setup script
setup-windows.bat

# Or use PowerShell
.\setup-windows.ps1

# Start backend (in one terminal)
start-backend-windows.bat

# Start frontend (in another terminal)
start-frontend-windows.bat
```

### Mac / Linux

```bash
# Make scripts executable (first time only)
chmod +x setup.sh start-backend.sh start-frontend.sh

# Run setup
./setup.sh

# Start backend (in one terminal)
./start-backend.sh

# Start frontend (in another terminal)
./start-frontend.sh
```

## 📁 Path Handling

The project uses Python's `pathlib.Path` which automatically handles:
- Windows paths (`C:\Users\...`)
- Unix paths (`/home/user/...`)
- Path separators (`/` vs `\`)

**All paths in the codebase are cross-platform compatible.**

## 🔑 Environment Variables

### Backend (.env)

Create `backend/.env`:

```env
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
DEBUG=True
ENVIRONMENT=development
DATABASE_URL=sqlite:///./fairlending.db
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

**Note**: SQLite paths work the same on all platforms with `sqlite:///./`

### Frontend (.env.local)

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐍 Python Virtual Environment

### Windows
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

## 📦 Dependencies

All dependencies are platform-agnostic:
- **Python**: Uses `requirements.txt` (works on all platforms)
- **Node.js**: Uses `package.json` (works on all platforms)

## 🔄 Git Workflow

### When Pulling Changes

1. **Line endings**: Git automatically converts based on your OS
2. **File permissions**: Shell scripts may need `chmod +x` on Mac/Linux
3. **Paths**: All paths are relative, no changes needed

### When Pushing Changes

1. **Commit normally**: Git handles line endings automatically
2. **Include both**: `.bat` files for Windows, `.sh` files for Mac/Linux
3. **Test on your platform**: Before pushing, test that scripts work

## 🛠️ Troubleshooting

### Issue: "Permission denied" on Mac/Linux

**Solution:**
```bash
chmod +x setup.sh start-backend.sh start-frontend.sh
```

### Issue: "Scripts not found" on Windows

**Solution:**
- Use `.bat` files on Windows
- Use `.sh` files on Mac/Linux
- Both are included in the repository

### Issue: Path errors

**Solution:**
- All paths use `pathlib.Path` (cross-platform)
- If you see path errors, check that you're using relative paths
- Database path: `sqlite:///./fairlending.db` works on all platforms

### Issue: Line ending warnings

**Solution:**
- Git should handle this automatically with `.gitattributes`
- If you see warnings, run: `git config core.autocrlf true` (Windows) or `git config core.autocrlf input` (Mac/Linux)

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend starts without errors: `http://localhost:8000/health`
- [ ] Frontend starts without errors: `http://localhost:3000`
- [ ] API connection works (check browser console)
- [ ] Database file created: `backend/fairlending.db`
- [ ] Uploads directory exists: `backend/uploads/`

## 🔐 Security Notes

- **Never commit** `.env` or `.env.local` files
- These are in `.gitignore`
- Each developer should create their own `.env` files

## 📝 Platform-Specific Notes

### Windows
- Use Command Prompt or PowerShell
- Virtual environment: `venv\Scripts\activate`
- Path separator: `\` (but code uses `/` which works)

### Mac/Linux
- Use Terminal or Bash
- Virtual environment: `source venv/bin/activate`
- Path separator: `/`
- May need `chmod +x` for shell scripts

## 🤝 Collaboration

When working with teammates:

1. **Pull latest changes** before starting work
2. **Test on your platform** before pushing
3. **Include both** Windows and Mac/Linux scripts
4. **Document** any platform-specific issues

## 📚 Additional Resources

- [Git Attributes Documentation](https://git-scm.com/docs/gitattributes)
- [Python pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
- [Node.js Cross-Platform Guide](https://nodejs.org/en/docs/guides/)

---

**Need help?** Check the main README.md or open an issue on GitHub.

