# Important: Regenerate Profiles for State Diversity

## ⚠️ Current Issue

If you're seeing "Delhi" on all profiles, this is because **existing profiles in the database were generated before the diversity fix was applied**.

## ✅ Solution: Regenerate Profiles

The mock profile generation logic has been fixed to ensure diverse states aligned with tiers. However, you need to **generate new profiles** to see the changes:

### Steps:

1. **Go to the Profiles page** (`/profiles`)
2. **Click "Generate Profiles"** (or use the dashboard)
3. **Generate a new batch** (e.g., 50-100 profiles)
4. **New profiles will show diverse states:**
   - **Urban Tier-1:** Delhi, Maharashtra, Karnataka, Tamil Nadu, West Bengal, Telangana, Gujarat
   - **Rural Tier-2:** Bihar, Uttar Pradesh, Madhya Pradesh, Odisha, Rajasthan, Haryana, Punjab
   - **Rural Tier-3:** Jharkhand, Chhattisgarh, Assam, Manipur, Tripura, Meghalaya, Mizoram

### What Changed:

- ✅ State selection now cycles through all available states per tier
- ✅ Ensures diversity even for small batches
- ✅ States are properly aligned with tier labels
- ✅ Each region gets different states systematically

### Note:

Old profiles in the database will still show "Delhi" unless regenerated. The fix applies to **new profile generations only**.
