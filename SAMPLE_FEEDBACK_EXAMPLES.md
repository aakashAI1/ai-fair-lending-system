# Sample Feedback Examples for Fair Lending Validation

Use these realistic feedback examples when testing the feedback learning system. Copy and paste them into the feedback form for different bias findings.

---

## 1. Geographic Bias - Urban vs Rural

**Bias Finding:** Urban vs Rural - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Yes

**Severity Rating:** 5 (Critical)

**Root Cause Analysis:**
The scoring algorithm is penalizing rural applicants based solely on their geographic location, which is not a legitimate risk factor for loan approval. Rural applicants with strong academic credentials, good CIBIL scores, and adequate repayment capacity are being systematically rejected. This suggests the algorithm is over-weighting geographic indicators (postcode, region classification) as proxies for creditworthiness, when these factors should not influence loan decisions for student loans. The geographic bias may also stem from training data that historically shows lower repayment rates from rural areas due to structural factors (lack of employment opportunities, not creditworthiness).

**Suggested Mitigation:**
1. Completely remove geographic location (postcode, region, state) from all scoring calculations
2. Replace geographic proxies with actual merit-based factors: GPA, course quality, college tier, CIBIL score
3. Use income-to-loan ratio instead of absolute income to normalize for regional cost differences
4. Add explicit guardrails that reject any scoring model that considers geographic location
5. Recalibrate the model to focus solely on academic merit (40%), creditworthiness (30%), and repayment capacity based on income stability (30%)

---

## 2. Geographic Bias - Tier-1 vs Tier-2/3

**Bias Finding:** Tier-1 vs Tier-2/3 - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Yes

**Severity Rating:** 5 (Critical)

**Root Cause Analysis:**
The algorithm is treating college tier classification as a proxy for creditworthiness, which creates unfair discrimination against students from Tier-2 and Tier-3 cities. While college tier may correlate with placement opportunities, it should not directly impact loan approval decisions. A student from a Tier-2 city with an excellent GPA and strong academic record is being penalized simply because of their location, not their ability to repay. This violates fair lending principles as geographic origin is not a protected characteristic but is being used as a discriminatory factor.

**Suggested Mitigation:**
1. Separate college tier (which relates to academic quality) from geographic tier (which relates to location)
2. Use college tier as a bonus factor for academic merit, not as a penalty for geographic origin
3. Remove all geographic indicators from risk assessment calculations
4. Consider college tier only in the context of placement probability and future income potential, not as a geographic risk factor
5. Ensure students from Tier-2/3 cities with strong academic profiles receive equivalent treatment to Tier-1 urban students with similar credentials

---

## 3. Income Bias - High Income vs Low Income

**Bias Finding:** High Income (≥20L) vs Low Income (<₹15L) - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Partially

**Severity Rating:** 4 (High)

**Root Cause Analysis:**
The algorithm is using absolute family income as a primary factor for loan approval, which creates systematic bias against economically disadvantaged students. While repayment capacity is a legitimate consideration, the current implementation penalizes students from lower-income families even when their income-to-loan ratio and academic credentials indicate strong repayment potential. The algorithm should consider income relative to loan amount, not absolute income levels. Lower-income students with high GPAs from good colleges may have better repayment prospects than higher-income students with poor academic records, but the current model doesn't account for this.

**Suggested Mitigation:**
1. Replace absolute income thresholds with income-to-loan ratio (ITL ratio) as the primary repayment capacity metric
2. Set ITL ratio thresholds that are fair across income levels (e.g., ITL ratio > 0.3 for approval)
3. Consider income stability (employment type) rather than income level alone
4. Add academic merit as a compensating factor - students with excellent GPAs and strong college placements should be evaluated more favorably regardless of family income
5. Implement income-based interest rate adjustments instead of approval/rejection decisions based on income alone

---

## 4. Credit Bias - Good Credit vs Fair Credit

**Bias Finding:** Good Credit (≥750) vs Fair Credit (650-750) - Approval Parity: 1.17 (Low Severity)

**Is this discriminatory?** No

**Severity Rating:** 2 (Low)

**Root Cause Analysis:**
The slight disparity (approval parity of 1.17) is within acceptable limits and appears to be based on legitimate risk factors. CIBIL score is a well-established indicator of creditworthiness and repayment behavior. The difference in approval rates between excellent credit (≥750) and fair credit (650-750) is expected and reasonable. However, we should ensure that students with fair credit scores but strong academic profiles and adequate repayment capacity are not unduly penalized.

**Suggested Mitigation:**
1. Use CIBIL score as a factor, not a threshold - students with fair credit but strong academic merit should still be approved
2. Implement tiered interest rates based on credit scores rather than binary approval/rejection
3. Consider compensating factors: if a student has fair credit (650-750) but excellent GPA (>8.5) and high family income relative to loan, approve with slightly higher interest rate
4. Monitor to ensure the approval parity doesn't widen beyond acceptable limits (>1.2)

---

## 5. Credit Bias - Good Credit vs Poor Credit

**Bias Finding:** Good Credit (≥750) vs Poor Credit (<600) - Approval Parity: 5.51 (Medium Severity)

**Is this discriminatory?** Partially

**Severity Rating:** 3 (Medium)

**Root Cause Analysis:**
While CIBIL score is a legitimate risk indicator, the current model may be overly penalizing first-time borrowers (students often have limited credit history). Students from lower-income backgrounds may have poor credit scores not due to poor repayment behavior, but due to lack of credit history or limited access to formal credit systems. The algorithm should distinguish between poor credit due to bad repayment history versus poor credit due to limited credit history.

**Suggested Mitigation:**
1. Separate credit history length from credit score - treat students with limited credit history differently from those with poor repayment history
2. For first-time borrowers (credit history < 2 years), rely more heavily on academic merit and co-applicant credit scores
3. Consider parent/spouse co-applicant credit scores as primary indicator for students with limited credit history
4. Implement conditional approvals with higher interest rates for fair credit scores rather than outright rejection
5. Add a "credit history type" factor: penalize poor repayment history, but not limited credit history

---

## 6. Edge Cases - Self-Employed vs Salaried

**Bias Finding:** Self-Employed vs Salaried - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Partially

**Severity Rating:** 4 (High)

**Root Cause Analysis:**
The algorithm is penalizing self-employed co-applicants significantly more than salaried applicants, treating self-employment as inherently riskier. While income stability is a legitimate concern, the current implementation doesn't account for self-employed individuals with stable, documented income (business tax returns, bank statements). In India, many successful small business owners and entrepreneurs have stable income but are systematically penalized. The algorithm should evaluate income stability based on documentation and consistency, not employment type alone.

**Suggested Mitigation:**
1. Remove employment type as a direct penalty factor
2. Replace with income stability metrics: 2-3 years of tax returns, bank statements showing consistent income, business continuity
3. For self-employed applicants, require additional documentation (ITR, bank statements) but don't automatically penalize
4. Use income volatility (month-to-month variation) as a risk factor instead of employment type
5. Consider business type and industry - a stable retail business owner should be treated similarly to a salaried employee

---

## 7. Edge Cases - Single Parent vs Nuclear Family

**Bias Finding:** Single Parent vs Nuclear Family - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Yes

**Severity Rating:** 5 (Critical)

**Root Cause Analysis:**
The algorithm is treating single-parent families as inherently riskier, which is discriminatory and not based on legitimate credit factors. Family structure has no direct correlation with loan repayment ability. A single parent with stable income and good credit history should be evaluated the same as a nuclear family with equivalent financials. The bias appears to stem from implicit assumptions that single-parent households have less financial stability, which is not supported by data and violates fair lending principles.

**Suggested Mitigation:**
1. Completely remove family structure from all scoring calculations
2. Focus on actual financial indicators: income, credit score, employment stability
3. If the concern is about repayment capacity, use income-to-loan ratio and credit score, not family structure
4. Add explicit prohibition against considering family structure, marital status, or number of dependents
5. Ensure single-parent applicants with strong financial profiles receive equal treatment to nuclear family applicants

---

## 8. Income Bias - Normalization Needed

**Bias Finding:** High Income (≥20L) vs Low Income (<₹15L) - Approval Parity: 0.00 (Critical)

**Is this discriminatory?** Yes

**Severity Rating:** 5 (Critical)

**Root Cause Analysis:**
The algorithm is using absolute income thresholds that don't account for regional cost-of-living differences. A family earning ₹15L in a Tier-2 city may have the same purchasing power and repayment capacity as a family earning ₹25L in Mumbai. Additionally, the algorithm doesn't consider loan amount - a student requesting ₹5L loan from a ₹12L income family has better repayment capacity (ITL ratio: 0.24) than a student requesting ₹20L loan from a ₹25L income family (ITL ratio: 0.80). The current model penalizes lower absolute income without considering these contextual factors.

**Suggested Mitigation:**
1. Use income-to-loan ratio (ITL) instead of absolute income: ITL ratio = Annual Income / Loan Amount
2. Set fair ITL ratio thresholds: >0.25 for approval, 0.20-0.25 for conditional approval
3. Normalize for regional cost differences using postcode-based cost-of-living indices (but don't use this in approval decision, only for context)
4. Consider loan purpose and future income potential - education loans should factor in post-graduation earning potential
5. For lower income families, allow compensating factors: excellent academic record (GPA >9.0) or strong co-applicant profile can offset lower family income

---

## Tips for Using These Examples:

1. **Copy the entire block** for each bias finding you want to test
2. **Adjust the severity rating** based on the actual metrics you see
3. **Modify the suggested mitigation** to match your specific concerns
4. **Use multiple feedback entries** for the same bias to see how the system aggregates feedback
5. **Try different feedback styles** - some detailed (like above), some brief, to see how GenAI processes them

## What Happens Next:

After submitting feedback:
1. Go to the **Mitigation** section
2. Select the feedback entries you want to use
3. Run the mitigation cycle
4. Watch the system generate improved prompts based on your feedback
5. See the metrics improve as profiles are re-scored with the refined prompts

---

**Example Brief Feedback (Alternative Style):**

For the same Urban vs Rural bias:

**Is this discriminatory?** Yes  
**Severity Rating:** 5  
**Root Cause Analysis:** Geographic location is being used as a proxy for creditworthiness, which is unfair and discriminatory.  
**Suggested Mitigation:** Remove all geographic indicators (postcode, region, state) from scoring. Use only merit-based factors: GPA, CIBIL score, income-to-loan ratio.
