# Train ML Model State Distribution Fix

## ✅ **Problem Fixed**

The `train_ml_model.py` script was hardcoding `'state': 'Delhi'` for all profiles, causing every profile to show "Delhi" in the UI.

## 🔧 **Solution**

Updated `train_ml_model.py` to use the same **research-based state distribution** as the other data generation scripts:

### **Changes Made:**

1. **Added Research-Based State Distribution**:
   - 57% Southern states (Maharashtra, Kerala, Andhra Pradesh, Tamil Nadu, Karnataka)
   - 16% Northern states (Uttar Pradesh, Delhi, Punjab, etc.)
   - 12% Western states (Gujarat, Rajasthan, Madhya Pradesh)
   - 10% Eastern states (West Bengal, Bihar, Odisha, Jharkhand)
   - 5% Northeastern states (Assam, Tripura, Manipur)

2. **Updated Mapping Functions**:
   - `map_dataset1_to_profile()`: Now uses `get_state_for_region()` instead of hardcoded 'Delhi'
   - `map_dataset2_to_profile()`: Now uses `get_state_for_region()` instead of hardcoded 'Delhi'

3. **State Cycling**:
   - States are cycled through based on profile index
   - Ensures diversity even when importing many profiles
   - Maintains research-based proportions per region

## 📋 **What You Need to Do**

**Simply run the training script again:**

```cmd
cd backend
venv\Scripts\activate
python scripts\train_ml_model.py
```

The script will:
1. ✅ Clear old profiles (with "Delhi" state)
2. ✅ Import datasets with research-based state distribution
3. ✅ Generate diverse states (Maharashtra, Kerala, Tamil Nadu, etc.)
4. ✅ Train ML model on the new data
5. ✅ Score profiles and calculate metrics

## 🎯 **Expected Result**

After running the script, profiles will show:
- ✅ **~57% from Southern states** (Maharashtra, Kerala, Tamil Nadu, Karnataka, Andhra Pradesh, Telangana)
- ✅ **~16% from Northern states** (Uttar Pradesh, Delhi, Punjab, Haryana, Uttarakhand)
- ✅ **~12% from Western states** (Gujarat, Rajasthan, Madhya Pradesh)
- ✅ **~10% from Eastern states** (West Bengal, Bihar, Odisha, Jharkhand)
- ✅ **~5% from Northeastern states** (Assam, Tripura, Manipur)

**No more "Delhi" on every profile!**

## 📊 **Verification**

After running the script, check:
1. Go to the Profiles page in your frontend
2. You should see diverse states listed on each profile card
3. States should match the research-based distribution above

---

**The fix is complete! Just run the training script again to see the changes.**
