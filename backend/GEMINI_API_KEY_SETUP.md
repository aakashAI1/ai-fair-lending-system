# Gemini API Key Setup

## ✅ API Key Verified

Your Gemini API key has been tested and is working correctly!

**API Key:** `your_gemini_api_key_here`
**Model:** `gemini-2.0-flash`

## How to Set the API Key

### Option 1: Environment Variable (Recommended)

Set the environment variable before running the backend:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export GEMINI_MODEL="gemini-2.0-flash"
```

### Option 2: .env File

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
DEBUG=True
ENVIRONMENT=development
EOF
```

**Note:** The `.env` file is in `.gitignore` and won't be committed to Git.

### Option 3: System Environment (Permanent)

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export GEMINI_MODEL="gemini-2.0-flash"
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Testing the API Key

Run the test script to verify:

```bash
cd backend
python3 test_gemini_key.py
```

Or test the full GenAI service:

```bash
cd backend
python3 test_genai_service.py
```

## Verification

When the API key is working, you should see:
- ✅ Provider: `gemini` (not `mock`)
- ✅ Real profile generation from Gemini
- ✅ Real scoring responses from Gemini

## Troubleshooting

If you see "using mock provider":
1. Check that `GEMINI_API_KEY` is set correctly
2. Verify the API key is valid (run `test_gemini_key.py`)
3. Check that `google-generativeai` is installed: `pip install google-generativeai`

## Current Status

✅ API Key: **WORKING**
✅ Model: **gemini-2.0-flash**
✅ Service: **Initialized correctly**
✅ Profile Generation: **Working**
✅ Scoring: **Working**

