# Fix for Python 3.12 Compatibility Issue

## Problem
If you're getting this error:
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

This happens because **Python 3.12** has breaking changes that are incompatible with `pydantic v1` (used by langchain).

## Solution 1: Use Python 3.11 (Recommended)

**The project is designed for Python 3.11.** Python 3.12 has compatibility issues with some dependencies.

### Steps:

1. **Uninstall Python 3.12** (optional, you can keep both versions)

2. **Download Python 3.11:**
   - Go to: https://www.python.org/downloads/release/python-3119/
   - Download "Windows installer (64-bit)"
   - Install it (check "Add Python to PATH")

3. **Verify Python 3.11:**
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x`

4. **Recreate virtual environment:**
   ```cmd
   cd backend
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Start the server:**
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

## Solution 2: Quick Fix for Python 3.12 (Workaround)

If you must use Python 3.12, try this workaround:

1. **Install typing_extensions:**
   ```cmd
   cd backend
   venv\Scripts\activate
   pip install typing_extensions==4.8.0
   ```

2. **Set environment variable:**
   ```cmd
   set PYDANTIC_SKIP_MEMBER_COUNT=1
   ```

3. **Try starting again:**
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

**Note:** This workaround may not work for all cases. Python 3.11 is strongly recommended.

## Solution 3: Update Dependencies (Advanced)

If you want to use Python 3.12, you may need to update to newer versions:

```cmd
cd backend
venv\Scripts\activate
pip install --upgrade langchain langchain-openai langchain-google-genai pydantic
```

**Warning:** This may break other parts of the code. Test thoroughly.

## Recommended: Use Python 3.11

The project is tested and works best with **Python 3.11.9**. 

### Quick Reinstall Guide:

1. **Download Python 3.11.9:**
   - https://www.python.org/downloads/release/python-3119/
   - Choose "Windows installer (64-bit)"

2. **Install:**
   - Check "Add Python to PATH"
   - Click "Install Now"

3. **Verify:**
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.9`

4. **Recreate venv:**
   ```cmd
   cd backend
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Start server:**
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

---

**For your teammate:** The easiest fix is to install Python 3.11.9 instead of 3.12.

