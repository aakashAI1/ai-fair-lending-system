# Quick Data Setup Guide

## 🎯 Problem

When you clone the repository, the database is **empty** because:
- Database files (`.db`) are in `.gitignore` (not committed to GitHub)
- Each developer needs to populate their own local database

## ✅ Solution

The setup scripts **automatically populate sample data** for you!

### Windows
```cmd
setup-windows.bat
```
This will:
1. Install dependencies
2. Set up virtual environment
3. **Automatically populate sample data** (100 profiles, metrics, etc.)

### Mac/Linux
```bash
chmod +x setup.sh
./setup.sh
```
This will:
1. Install dependencies
2. Set up virtual environment
3. **Automatically populate sample data** (100 profiles, metrics, etc.)

## 📊 What Data Gets Populated?

After running setup, you'll have:
- ✅ **100 student profiles** (synthetic Indian student loan applicants)
- ✅ **200 scoring results** (100 fair + 100 biased scores)
- ✅ **3 bias metrics** (Geographic, Income, Credit dimensions)
- ✅ **2 human feedback entries** (example annotations)
- ✅ **2 mitigation results** (example improvement iterations)

## 🚀 After Setup

1. Start the backend: `start-backend-windows.bat` (Windows) or `./start-backend.sh` (Mac/Linux)
2. Start the frontend: `start-frontend-windows.bat` (Windows) or `./start-frontend.sh` (Mac/Linux)
3. Open http://localhost:3000/dashboard
4. **You should see all metrics displayed!** 🎉

## 🔄 Manual Data Population

If you need to regenerate or repopulate data manually:

### Windows
```cmd
cd backend
venv\Scripts\activate
python scripts\populate_mock_data.py
```

### Mac/Linux
```bash
cd backend
source venv/bin/activate
python3 scripts/populate_mock_data.py
```

## 📝 Notes

- The sample data is **synthetic** (not real student information)
- It's designed to demonstrate bias patterns and system functionality
- Each developer gets their own local database
- Data is **not** shared between developers (by design)

## 🆘 Troubleshooting

### "No data visible on dashboard"
1. Check if backend is running: http://localhost:8000/health
2. Check if database exists: `backend/fairlending.db`
3. Run populate script manually (see above)
4. Check browser console for errors

### "Database is empty"
Run the populate script:
```bash
cd backend
python scripts/populate_mock_data.py
```

### "Setup script failed to populate data"
This is OK! Just run the populate script manually after setup completes.

---

**Need help?** Check the main README.md or open an issue on GitHub.

