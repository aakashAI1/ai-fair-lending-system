# 🔧 Windows Visibility Fix

## ✅ **Fixed:**

Removed `/MIN` flag so windows open **visibly** instead of minimized.

---

## 🪟 **What You'll See:**

After running `run-complete-setup.bat`, you should see **3 windows**:

1. **Window 1: "Fair Lending - Backend Server"**
   - Shows backend server logs
   - Running on http://localhost:8000
   - **Keep this open!**

2. **Window 2: "Fair Lending - Frontend Server"**
   - Shows frontend server logs
   - Running on http://localhost:3000
   - **Keep this open!**

3. **Window 3: Setup Script Window**
   - Shows setup progress
   - Can be closed after setup completes

---

## 🔍 **If Windows Still Don't Appear:**

1. **Check Taskbar:**
   - Look for minimized windows in taskbar
   - Click to restore them

2. **Check Alt+Tab:**
   - Press `Alt + Tab` to see all open windows
   - Select the backend/frontend windows

3. **Manually Check:**
   - Open Task Manager (`Ctrl + Shift + Esc`)
   - Look for `cmd.exe` or `node.exe` processes
   - Right-click → "Bring to front"

---

## ✅ **Updated Batch File:**

The batch file now:
- ✅ Opens windows visibly (not minimized)
- ✅ Uses absolute paths (`%~dp0`) for reliability
- ✅ Shows clear headers in each window
- ✅ Properly activates virtual environment

**Try running `run-complete-setup.bat` again - windows should be visible now!** 🎯
