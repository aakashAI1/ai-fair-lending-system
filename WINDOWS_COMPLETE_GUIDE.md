# 🪟 Complete Windows Setup Guide - Step by Step

This guide will take you from downloading the project from GitHub to running it on Windows.

## 📋 Prerequisites - Install These First

### Step 1: Install Python 3.11 (IMPORTANT: Use 3.11, NOT 3.12!)

**⚠️ IMPORTANT:** Use Python 3.11.9, NOT Python 3.12! Python 3.12 has compatibility issues with this project.

1. **Go to Python 3.11.9 download page:**
   - Visit: https://www.python.org/downloads/release/python-3119/
   - Scroll down to "Files" section
   - Click "Windows installer (64-bit)" to download

2. **Download Python 3.11.9:**
   - It will download `python-3.11.9-amd64.exe`
   - Save it to your Downloads folder

3. **Install Python:**
   - Double-click the downloaded file
   - **IMPORTANT:** Check the box "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

4. **Verify Python is installed:**
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - In the Command Prompt, type:
     ```
     python --version
     ```
   - You should see: `Python 3.11.9` (or 3.11.x)
   - **If you see Python 3.12.x**, you need to uninstall it and install 3.11.9 instead
   - If you see "python is not recognized", Python is not in PATH - reinstall and check the "Add to PATH" box

**Why Python 3.11?** Python 3.12 has breaking changes that cause errors with pydantic v1 (used by langchain). See `WINDOWS_PYTHON312_FIX.md` if you encounter compatibility errors.

### Step 2: Install Node.js 18 or Higher

1. **Go to Node.js website:**
   - Visit: https://nodejs.org/
   - Download the **LTS version** (recommended, usually on the left)

2. **Install Node.js:**
   - Double-click the downloaded `.msi` file
   - Click "Next" through the installation wizard
   - Accept the license agreement
   - Keep default installation path
   - Click "Install"
   - Wait for installation
   - Click "Finish"

3. **Verify Node.js is installed:**
   - Open a **new** Command Prompt (close and reopen if needed)
   - Type:
     ```
     node --version
     ```
   - You should see: `v18.x.x` or higher
   - Also verify npm:
     ```
     npm --version
     ```
   - You should see: `9.x.x` or higher

### Step 3: Install Git (Optional - if you don't have it)

1. **Go to Git website:**
   - Visit: https://git-scm.com/download/win
   - Download will start automatically

2. **Install Git:**
   - Double-click the downloaded file
   - Click "Next" through the installation
   - Keep default options
   - Click "Install"
   - Click "Finish"

3. **Verify Git:**
   - Open Command Prompt
   - Type:
     ```
     git --version
     ```
   - You should see: `git version 2.x.x`

---

## 📥 Step 4: Download the Project from GitHub

### Option A: Using Git (Recommended)

1. **Open Command Prompt:**
   - Press `Windows Key + R`
   - Type `cmd` and press Enter

2. **Navigate to where you want the project:**
   ```
   cd Desktop
   ```
   (Or `cd Documents` if you prefer)

3. **Clone the repository:**
   ```
   git clone https://github.com/aayusharmaaa/hitl-project-testing.git
   ```

4. **Navigate into the project:**
   ```
   cd hitl-project-testing
   ```

### Option B: Download as ZIP

1. **Go to GitHub:**
   - Visit: https://github.com/aayusharmaaa/hitl-project-testing
   - Click the green "Code" button
   - Click "Download ZIP"

2. **Extract the ZIP:**
   - Right-click the downloaded ZIP file
   - Select "Extract All..."
   - Choose a location (e.g., Desktop)
   - Click "Extract"

3. **Open Command Prompt:**
   - Navigate to the extracted folder:
     ```
     cd Desktop
     cd hitl-project-testing
     ```

---

## ⚙️ Step 5: Set Up the Project (Automated)

### Quick Setup Using the Script

1. **Make sure you're in the project folder:**
   ```
   cd hitl-project-testing
   ```
   (Verify you see files like `setup-windows.bat`, `README.md`, etc.)

2. **Run the setup script:**
   - **Option 1:** Double-click `setup-windows.bat`
   - **Option 2:** In Command Prompt, type:
     ```
     setup-windows.bat
     ```

3. **Wait for setup to complete:**
   - The script will:
     - Check Python and Node.js
     - Create virtual environment
     - Install all Python packages
     - Install all Node.js packages
     - Create configuration files
   - This may take 5-10 minutes depending on your internet speed

4. **If you see errors:**
   - Make sure Python and Node.js are installed correctly
   - Make sure you're connected to the internet
   - Try running the script again

---

## 🔑 Step 6: Configure API Key

1. **Get your Gemini API Key:**
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key (it looks like: `AIzaSy...`)

2. **Edit the .env file:**
   - Navigate to: `hitl-project-testing\backend\`
   - Open the `.env` file in Notepad:
     - Right-click `.env`
     - Select "Open with" → "Notepad"
   - Find this line:
     ```
     GEMINI_API_KEY=your-gemini-api-key-here
     ```
   - Replace `your-gemini-api-key-here` with your actual API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Save the file (Ctrl+S)
   - Close Notepad

---

## 🚀 Step 7: Start the Application

You need to run **two servers** - one for backend, one for frontend.

### Start Backend Server

**Option 1: Using the Script (Easiest)**
- Double-click `start-backend-windows.bat`
- A Command Prompt window will open
- You should see: `Uvicorn running on http://0.0.0.0:8000`
- **Keep this window open!**

**Option 2: Manual Start**
1. Open Command Prompt
2. Navigate to project:
   ```
   cd Desktop
   cd hitl-project-testing
   cd backend
   ```
3. Activate virtual environment:
   ```
   venv\Scripts\activate
   ```
   (You should see `(venv)` at the start of your prompt)
4. Start server:
   ```
   python -m uvicorn app.main:app --reload --port 8000
   ```
5. You should see: `Uvicorn running on http://0.0.0.0:8000`
6. **Keep this window open!**

### Start Frontend Server

**Option 1: Using the Script (Easiest)**
- Double-click `start-frontend-windows.bat`
- A **new** Command Prompt window will open
- You should see: `Ready on http://localhost:3000`
- **Keep this window open!**

**Option 2: Manual Start**
1. Open a **NEW** Command Prompt window
2. Navigate to project:
   ```
   cd Desktop
   cd hitl-project-testing
   cd frontend
   ```
3. Start server:
   ```
   npm run dev
   ```
4. You should see: `Ready on http://localhost:3000`
5. **Keep this window open!**

---

## 🌐 Step 8: Open the Application

1. **Open your web browser** (Chrome, Edge, Firefox, etc.)

2. **Go to:**
   ```
   http://localhost:3000
   ```

3. **You should see:**
   - The Fair Lending AI Validation dashboard
   - An upload section at the top
   - Welcome message if no data is uploaded yet

4. **Test the backend:**
   - Go to: http://localhost:8000/health
   - You should see: `{"status":"healthy"}`

5. **View API documentation:**
   - Go to: http://localhost:8000/docs
   - You should see the Swagger UI with all API endpoints

---

## 📤 Step 9: Upload Data (Optional)

1. **On the dashboard** (http://localhost:3000), you'll see an upload section

2. **Upload a ZIP file:**
   - Click the upload area or drag and drop a ZIP file
   - The system will process and import student profiles
   - Wait for "Successfully imported" message

3. **View results:**
   - After upload, the dashboard will refresh
   - You'll see metrics, heatmaps, and findings

---

## 🛑 Step 10: Stop the Application

When you're done:

1. **Stop Backend:**
   - Go to the backend Command Prompt window
   - Press `Ctrl + C`
   - Type `Y` if asked to confirm

2. **Stop Frontend:**
   - Go to the frontend Command Prompt window
   - Press `Ctrl + C`
   - Type `Y` if asked to confirm

3. **Close the windows**

---

## ❌ Troubleshooting

### Problem: "python is not recognized"

**Solution:**
1. Reinstall Python 3.11.9 from https://www.python.org/downloads/release/python-3119/
2. **Make sure to check "Add Python to PATH"** during installation
3. Restart Command Prompt after installation

### Problem: "TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument"

**This means you're using Python 3.12, which is incompatible!**

**Solution:**
1. **Uninstall Python 3.12** (if installed)
2. **Install Python 3.11.9** from: https://www.python.org/downloads/release/python-3119/
3. **Recreate virtual environment:**
   ```cmd
   cd backend
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. See `WINDOWS_PYTHON312_FIX.md` for detailed fix instructions

### Problem: "node is not recognized"

**Solution:**
1. Reinstall Node.js from https://nodejs.org/
2. Restart Command Prompt after installation

### Problem: "Port 8000 already in use"

**Solution:**
1. Find what's using the port:
   ```
   netstat -ano | findstr :8000
   ```
2. Note the PID number (last column)
3. Kill the process:
   ```
   taskkill /PID <PID_NUMBER> /F
   ```
4. Or change the port in `start-backend-windows.bat`

### Problem: "Port 3000 already in use"

**Solution:**
- Same as above, but use port 3000:
  ```
  netstat -ano | findstr :3000
  taskkill /PID <PID_NUMBER> /F
  ```

### Problem: "Cannot connect to backend"

**Solution:**
1. Make sure backend is running (check the Command Prompt window)
2. Check http://localhost:8000/health in browser
3. Make sure Windows Firewall isn't blocking it
4. Verify `.env.local` in frontend folder has:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Problem: "pip install fails"

**Solution:**
1. Make sure virtual environment is activated (you see `(venv)`)
2. Upgrade pip:
   ```
   python -m pip install --upgrade pip
   ```
3. Try installing again:
   ```
   pip install -r requirements.txt
   ```

### Problem: "npm install fails"

**Solution:**
1. Clear npm cache:
   ```
   npm cache clean --force
   ```
2. Delete `node_modules` folder in frontend directory
3. Try again:
   ```
   npm install
   ```

### Problem: Setup script doesn't work

**Solution:**
1. Make sure you're in the project root folder
2. Try running it from Command Prompt:
   ```
   cd path\to\hitl-project-testing
   setup-windows.bat
   ```
3. Check for error messages
4. Follow manual setup in Step 5 (Option 2)

---

## 📚 Additional Resources

- **Windows Setup Guide:** `WINDOWS_SETUP.md` (detailed troubleshooting)
- **Quick Start:** `QUICK_START.md`
- **API Documentation:** http://localhost:8000/docs (when backend is running)
- **Main README:** `README.md`

---

## ✅ Quick Checklist

Before running, make sure:
- [ ] Python 3.11+ installed and in PATH
- [ ] Node.js 18+ installed
- [ ] Project cloned/downloaded from GitHub
- [ ] `setup-windows.bat` run successfully
- [ ] API key added to `backend\.env`
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Browser opened to http://localhost:3000

---

## 🎉 You're All Set!

Once both servers are running and you can access http://localhost:3000, you're ready to use the application!

**Need help?** Check the troubleshooting section above or refer to `WINDOWS_SETUP.md` for more detailed help.

---

**Happy Coding! 🚀**

