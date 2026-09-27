# Frontend Module Not Found Fix

## Problem
```
Module not found: Can't resolve '@/lib/utils'
```

## Solution

### Step 1: Clear Next.js Cache

1. **Stop the frontend server** (Press Ctrl+C in the terminal)

2. **Delete the .next folder:**
   ```cmd
   cd frontend
   rmdir /s /q .next
   ```

3. **Clear node_modules cache (optional but recommended):**
   ```cmd
   rmdir /s /q node_modules
   npm install
   ```

### Step 2: Restart the Server

```cmd
npm run dev
```

## If Still Not Working

### Alternative Fix: Reinstall Dependencies

1. **Delete node_modules and package-lock.json:**
   ```cmd
   cd frontend
   rmdir /s /q node_modules
   del package-lock.json
   ```

2. **Reinstall:**
   ```cmd
   npm install
   ```

3. **Clear Next.js cache:**
   ```cmd
   rmdir /s /q .next
   ```

4. **Start server:**
   ```cmd
   npm run dev
   ```

## Verify tsconfig.json

Make sure your `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

The `baseUrl: "."` is important for Windows path resolution.

## Quick Fix Command (All in One)

Run this in the `frontend` directory:
```cmd
rmdir /s /q .next && rmdir /s /q node_modules && del package-lock.json && npm install && npm run dev
```

This will:
1. Delete .next cache
2. Delete node_modules
3. Delete package-lock.json
4. Reinstall all dependencies
5. Start the dev server

---

**Most common fix:** Just delete `.next` folder and restart:
```cmd
rmdir /s /q .next
npm run dev
```

