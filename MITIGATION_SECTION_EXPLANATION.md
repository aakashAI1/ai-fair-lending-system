# Mitigation Section - How It Works

## Overview

The Mitigation section implements an **iterative, GenAI-powered bias reduction process** that gradually improves fairness scores through multiple cycles. This aligns with real banking industry standards where changes are made conservatively and incrementally.

## How It Works (Step-by-Step)

### 1. **User Flow**

```
Feedback Section → Submit Feedback → Mitigation Section → Run Mitigation → View Results
```

### 2. **Components**

#### **MitigationForm.tsx**
- **Purpose**: Allows users to configure and start a mitigation cycle
- **Inputs**:
  - **Test Run ID**: The test run containing the profiles to improve
  - **Feedback Selection**: Choose which feedback entries to use for improvement
  - **Max Iterations**: Number of improvement cycles (default: 5, max: 10)
  - **Target Fairness Score**: Goal to achieve (default: 85/100)

#### **ComparisonTable.tsx**
- **Purpose**: Displays the iterative improvement results
- **Shows**:
  - Each iteration's before/after fairness scores
  - Improvement percentage per iteration
  - Overall progress summary

### 3. **Backend Process**

When you click "Run Mitigation":

1. **Load Feedback**: Retrieves selected feedback entries with root cause analysis and mitigation suggestions

2. **Iterative Improvement Loop** (up to 5 iterations):
   ```
   For each iteration (1-5):
     a. Generate Refined Prompt using GenAI
        - Analyzes feedback and current metrics
        - Creates improved scoring prompt (conservative, 5-15% improvement)
        - Addresses one bias factor at a time
     
     b. Save Refined Prompt
        - Stores prompt version (fair_v2, fair_v3, etc.)
        - Links to feedback used
     
     c. Re-Score All Profiles
        - Applies new refined prompt to all profiles
        - Uses GenAI with the refined prompt
     
     d. Recalculate Metrics
        - Computes new bias metrics
        - Calculates new fairness scores
     
     e. Check Progress
        - Compares new score vs. target
        - If target achieved OR max iterations reached → Stop
        - Otherwise → Continue to next iteration
   ```

3. **Return Results**:
   - All iteration results
   - Initial vs. final fairness scores
   - Total improvement percentage
   - Whether target was achieved

### 4. **Realistic Banking Constraints**

The system enforces conservative, incremental improvements:

- **5-15% improvement per iteration** (not 50%+ jumps)
- **2-5 percentage point weight adjustments** per cycle
- **Gradual bias factor removal** (reduce by 50% first, not 100%)
- **One bias factor addressed per iteration**
- **Maintains scoring logic integrity** (Academic Merit 40%, Creditworthiness 30%, Repayment Capacity 30%)

### 5. **Example Iteration Flow**

```
Initial State:
- Fairness Score: 45.2
- Approval Parity (Urban vs Rural): 0.00

Iteration 1:
- GenAI generates prompt: "Reduce geographic weight by 30%"
- Re-score profiles
- New Fairness Score: 52.8 (+16.8%)
- Approval Parity: 0.15

Iteration 2:
- GenAI generates prompt: "Further reduce geographic weight, add income normalization"
- Re-score profiles
- New Fairness Score: 60.5 (+14.6%)
- Approval Parity: 0.32

Iteration 3:
- GenAI generates prompt: "Remove geographic factors completely, normalize income-to-loan ratio"
- Re-score profiles
- New Fairness Score: 67.2 (+11.1%)
- Approval Parity: 0.58

Iteration 4:
- GenAI generates prompt: "Fine-tune weights, add compensating factors"
- Re-score profiles
- New Fairness Score: 73.8 (+9.8%)
- Approval Parity: 0.78

Iteration 5:
- GenAI generates prompt: "Optimize remaining disparities"
- Re-score profiles
- New Fairness Score: 79.5 (+7.7%)
- Approval Parity: 0.92

Final Result:
- Total Improvement: +75.9%
- Target Achieved: No (target was 85, reached 79.5)
- But significant progress made gradually
```

## How to Use

### Step 1: Provide Feedback
1. Go to **Feedback** section
2. Select a bias finding
3. Fill in:
   - Is this discriminatory? (Yes/No/Partially)
   - Root Cause Analysis
   - Severity Rating
   - Suggested Mitigation (or use AI suggestions)
4. Submit feedback

### Step 2: Run Mitigation
1. Go to **Mitigation** section
2. Enter **Test Run ID** (from Dashboard or Profile Generation)
3. **Select Feedback** entries to use (checkboxes)
4. Set **Max Iterations** (default: 5)
5. Set **Target Fairness Score** (default: 85)
6. Click **"Run Mitigation"**

### Step 3: View Results
1. Wait for processing (may take 1-3 minutes)
2. View **Before/After Comparison Table**:
   - Each iteration's progress
   - Improvement percentages
   - Overall summary

## What Makes It Realistic

1. **Gradual Improvement**: Each iteration makes small, conservative changes
2. **Iterative Refinement**: Multiple cycles to reach target
3. **Feedback-Driven**: Uses human feedback to guide improvements
4. **Auditable**: All changes are logged and trackable
5. **Compliant**: Changes are explainable for regulatory requirements
6. **Risk-Aware**: Maintains credit quality while improving fairness

## Technical Details

- **Prompt Refinement**: GenAI analyzes feedback and generates improved scoring prompts
- **Prompt Versioning**: Each iteration creates a new prompt version (fair_v1, fair_v2, etc.)
- **Scoring Integration**: Refined prompts are used to re-score all profiles
- **Metrics Recalculation**: Bias metrics recalculated after each iteration
- **Progress Tracking**: All iterations saved to database for audit trail

## Benefits for Presentation

✅ Shows realistic, industry-aligned process  
✅ Demonstrates measurable improvement over time  
✅ Highlights iterative, conservative approach  
✅ Proves feedback actually improves the system  
✅ Provides complete audit trail  

---

**Note**: The system is designed to be conservative and realistic, making gradual improvements that real banks would implement in production environments.
