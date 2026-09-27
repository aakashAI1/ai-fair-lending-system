# 🔍 Troubleshooting: Windows Not Visible

## ✅ **Fixed Batch File:**

Updated `run-complete-setup.bat` to ensure windows open visibly.

---

## 🪟 **What Should Happen:**

When you run `run-complete-setup.bat`, **2 new windows** should open:

1. **"Fair Lending - Backend Server"** window
2. **"Fair Lending - Frontend Server"** window

---

## 🔍 **If Windows Don't Appear:**

### **Option 1: Check Taskbar**
- Look at the bottom taskbar
- Find windows with titles "Fair Lending - Backend Server" or "Fair Lending - Frontend Server"
- Click them to bring to front

### **Option 2: Use Alt+Tab**
- Press `Alt + Tab` to see all open windows
- Look for the backend/frontend server windows
- Select them to bring to front

### **Option 3: Check Task Manager**
- Press `Ctrl + Shift + Esc` to open Task Manager
- Look for `cmd.exe` processes
- Right-click → "Bring to front" or "Switch to"

### **Option 4: Check if Servers Are Running**
- Open browser: http://localhost:8000/docs (backend)
- Open browser: http://localhost:3000 (frontend)
- If they load, servers are running (just windows hidden)

---

## 🔧 **Alternative: Manual Start**

If batch file doesn't work, start manually:

**Terminal 1 (Backend):**
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

**Terminal 2 (Frontend):**
```cmd
cd frontend
npm run dev
```

---

## ✅ **Updated Batch File:**

The batch file now:
- ✅ Removed `/MIN` flag (was minimizing windows)
- ✅ Uses absolute paths for reliability
- ✅ Shows clear window titles
- ✅ Provides troubleshooting tips

**Try running `run-complete-setup.bat` again - windows should be visible now!** 🎯
