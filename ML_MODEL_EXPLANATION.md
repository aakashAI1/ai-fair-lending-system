# ML Model Training & Usage - Clarification

## 🤔 Common Confusion: "Does the model train every time?"

**Answer: NO!** The model is trained **once** (or when you want to retrain), then saved to disk and reused.

---

## 📋 How It Actually Works

### Step 1: Initial Training (One-Time Setup)

**Run this once:**
```bash
cd backend
venv\Scripts\activate
python scripts\train_ml_model.py
```

**What happens:**
1. Loads datasets (2000+ profiles)
2. Trains scikit-learn RandomForest model
3. **Saves model to disk:** `backend/models/scoring_model.pkl`
4. Creates initial test run with metrics

**Time:** Takes 1-2 minutes (one time only)

---

### Step 2: Runtime Scoring (Automatic)

**Every time you score profiles** (via API or dashboard):
1. System checks if `backend/models/scoring_model.pkl` exists
2. **If file exists:**
   - Loads pre-trained model from disk (cached in memory)
   - Uses ML model predictions for **biased scoring**
   - Uses deterministic scoring for **fair scoring**
3. **If file doesn't exist:**
   - Falls back to deterministic scoring for both fair and biased

**Time:** Instant (model already trained)

---

## 🔄 Model Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│  TRAINING (One-Time Setup)                              │
│  ┌──────────────────────────────────────────┐          │
│  │ python scripts/train_ml_model.py         │          │
│  │  ↓                                        │          │
│  │ Train RandomForest on 2000+ profiles     │          │
│  │  ↓                                        │          │
│  │ Save to: models/scoring_model.pkl        │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  SCORING (Runtime - Happens Automatically)              │
│  ┌──────────────────────────────────────────┐          │
│  │ User scores profiles via API/Dashboard   │          │
│  │  ↓                                        │          │
│  │ Check: Does scoring_model.pkl exist?     │          │
│  │  ↓                                        │          │
│  │ YES → Load model from disk                │          │
│  │      → Use ML predictions (biased)        │          │
│  │      → Use deterministic (fair)           │          │
│  │  ↓                                        │          │
│  │ NO  → Use deterministic for both         │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 When Each Scoring Method Is Used

### Fair Scoring:
- **Always uses:** `DeterministicScoringEngine.calculate_fair_score()`
- **Reason:** Fair scoring should be rule-based and unbiased (no ML bias)

### Biased Scoring:
- **If model file exists:** Uses `MLScoringModel.predict_score()` 
  - ML model learned biases from training data
  - More realistic (demonstrates real-world AI bias)
- **If model file doesn't exist:** Uses `DeterministicScoringEngine.calculate_biased_score()`
  - Rule-based bias penalties
  - Still works, but less realistic

---

## 🔍 Code Flow

### Training Script (`train_ml_model.py`):
```python
# Train model
ml_model = MLScoringModel(model_type="random_forest")
ml_model.train(train_df)  # Trains on data
# Model is saved to: backend/models/scoring_model.pkl
```

### Scoring Service (`scoring_service.py`):
```python
def get_ml_model():
    """Lazy loading - loads model once, then caches it"""
    global _ml_model
    if _ml_model is None:
        _ml_model = MLScoringModel()
        try:
            _ml_model.load_model()  # Loads from disk
        except FileNotFoundError:
            _ml_model = None  # No model file, use fallback
    return _ml_model

# During scoring:
ml_model = get_ml_model()
if ml_model and ml_model.is_trained:
    # Use ML model for biased scoring
    result = ml_model.predict_score(profile, apply_bias=True)
else:
    # Use deterministic fallback
    result = deterministic.calculate_biased_score(profile)
```

---

## ❓ FAQ

### Q: Do I need to train the model every time I start the server?
**A:** No! The model file persists on disk. Training is a one-time setup step.

### Q: When should I retrain the model?
**A:** Only when:
- You add significant new training data
- You want to test different model types
- The model performance degrades

### Q: What if I delete the model file?
**A:** The system will automatically fall back to deterministic scoring. Everything still works, just less realistic.

### Q: Can I train on different datasets?
**A:** Yes! Modify `train_ml_model.py` to load your datasets, then run it to train a new model.

### Q: How do I know if the model is being used?
**A:** Check backend logs. You'll see:
- `"ML model loaded successfully"` → Using ML model
- `"ML model not found, will use deterministic scoring"` → Using fallback

---

## ✅ Summary

- **Training:** One-time setup (or when you want to retrain)
- **Scoring:** Automatic - loads saved model if it exists
- **Model File:** Persists on disk (`backend/models/scoring_model.pkl`)
- **Fallback:** Deterministic scoring if model file doesn't exist
- **No Retraining Needed:** Model is reused for all scoring operations

**Bottom Line:** Train once, use forever (until you want to retrain)!
