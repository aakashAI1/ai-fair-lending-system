"""
Deterministic scoring models for fair and biased loan approval.
These models provide consistent, reproducible scores for showcasing.
"""

import math
from typing import Dict, Any


class DeterministicScoringEngine:
    """
    Deterministic scoring engine that provides consistent results
    without requiring GenAI API calls.
    """
    
    @staticmethod
    def calculate_fair_score(profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate fair (unbiased) score based only on merit factors.
        
        Scoring Formula:
        - Academic Merit (40%): Based on GPA and educational background
        - Creditworthiness (30%): Based on CIBIL score
        - Repayment Capacity (30%): Based on income-to-loan ratio and stability
        """
        # Extract profile data
        gpa = profile.get("gpa", 7.0)  # Indian GPA scale: 0-10
        cibil_score = profile.get("cibil_score", 650)
        family_income = profile.get("family_income", 2000000)
        requested_loan_amount = profile.get("requested_loan_amount", 1000000)
        educational_background = profile.get("educational_background", "").lower()
        employment_type = profile.get("employment_type", "").lower()
        co_applicant = profile.get("co_applicant", "").lower()
        college_tier = profile.get("college_tier", "").lower() if profile.get("college_tier") else ""
        
        # 1. Academic Merit Component (40% = 4.0 points max)
        # Normalize GPA from 0-10.0 to 0-3.0 scale (Indian 10-point system)
        gpa_score = (gpa / 10.0) * 3.0
        
        # Educational background bonus (max 0.8 point)
        edu_bonus = 0.0
        if "engineering" in educational_background or "engineering" in profile.get("course", "").lower():
            edu_bonus = 0.5
        elif "commerce" in educational_background or "mba" in profile.get("course", "").lower():
            edu_bonus = 0.3
        elif "science" in educational_background:
            edu_bonus = 0.2
        
        # College tier bonus (max 0.5 point) - Better colleges = better placement prospects = better repayment capacity
        # This is fair because it's based on merit-based admission and career prospects
        college_bonus = 0.0
        university_name = profile.get("university_name") or ""
        university_name_lower = university_name.lower() if university_name else ""
        if college_tier == "tier1" or "iit" in university_name_lower or "iim" in university_name_lower:
            college_bonus = 0.5  # Top tier (IITs, IIMs, top central universities) - best placement prospects
        elif college_tier == "tier2" or any(x in university_name_lower for x in ["nit", "bits", "vit", "manipal"]):
            college_bonus = 0.3  # Good tier (NITs, top private universities) - good placement prospects
        elif college_tier == "tier3":
            college_bonus = 0.1  # Lower tier - standard placement prospects
        
        academic_merit = min(4.0, gpa_score + edu_bonus + college_bonus)
        
        # 2. Creditworthiness Component (30% = 3.0 points max)
        # Normalize CIBIL from 300-900 to 0-3.0 scale
        cibil_normalized = (cibil_score - 300) / 600  # 0 to 1
        creditworthiness = cibil_normalized * 3.0
        
        # 3. Repayment Capacity Component (30% = 3.0 points max)
        # Income-to-loan ratio
        if requested_loan_amount > 0:
            income_ratio = family_income / requested_loan_amount
        else:
            income_ratio = 0
        
        # Base capacity score (0-2.0 points)
        if income_ratio >= 3.0:  # Income is 3x loan amount
            capacity_score = 2.0
        elif income_ratio >= 2.0:  # Income is 2x loan amount
            capacity_score = 1.5
        elif income_ratio >= 1.5:  # Income is 1.5x loan amount
            capacity_score = 1.0
        elif income_ratio >= 1.0:  # Income equals loan amount
            capacity_score = 0.5
        else:
            capacity_score = 0.2
        
        # Stability bonus (0-1.0 point)
        stability_bonus = 0.0
        if employment_type == "government":
            stability_bonus = 0.5
        elif employment_type == "salaried":
            stability_bonus = 0.3
        elif employment_type == "self-employed":
            stability_bonus = 0.1
        
        # Co-applicant bonus (if parent/spouse with income)
        if co_applicant in ["parent", "spouse"]:
            stability_bonus += 0.2
        
        repayment_capacity = min(3.0, capacity_score + stability_bonus)
        
        # Total score (1-10 scale)
        total_score = academic_merit + creditworthiness + repayment_capacity
        
        # Add small random variation (0.1) for realism, but keep deterministic
        # Using profile_id hash for deterministic "randomness"
        profile_id = profile.get("profile_id", "")
        hash_val = hash(profile_id) % 10 if profile_id else 0
        variation = (hash_val / 10.0) * 0.2 - 0.1  # -0.1 to 0.1
        
        final_score = max(1.0, min(10.0, total_score + variation))
        
        # Determine approval decision (lenient thresholds for fair scoring to ensure good baseline)
        # This ensures fair scoring has high approval rates, making parity calculation meaningful
        if final_score >= 8.0:
            approval_decision = "approve"
            interest_rate = 9.0
            collateral_required = False
        elif final_score >= 6.5:
            approval_decision = "approve"
            interest_rate = 10.5
            collateral_required = False
        elif final_score >= 5.0:
            approval_decision = "approve"  # Lower threshold for better baseline
            interest_rate = 11.5
            collateral_required = True
        elif final_score >= 4.0:
            approval_decision = "conditional"
            interest_rate = 13.0
            collateral_required = True
        else:
            approval_decision = "reject"
            interest_rate = 15.0
            collateral_required = True
        
        college_info = ""
        if college_tier or profile.get("university_name"):
            college_name = profile.get("university_name", "Unknown")
            if college_tier == "tier1":
                college_info = f" College: {college_name} (Tier-1 - excellent placement prospects)."
            elif college_tier == "tier2":
                college_info = f" College: {college_name} (Tier-2 - good placement prospects)."
            elif college_tier == "tier3":
                college_info = f" College: {college_name} (Tier-3 - standard placement prospects)."
            else:
                college_info = f" College: {college_name}."
        
        reasoning = (
            f"Fair evaluation: Academic merit {gpa:.2f} GPA ({academic_merit:.1f}/4.0), "
            f"CIBIL {cibil_score} ({creditworthiness:.1f}/3.0), "
            f"Repayment capacity {income_ratio:.2f}x ({repayment_capacity:.1f}/3.0).{college_info} "
            f"Total: {final_score:.2f}/10.0"
        )
        
        return {
            "score": round(final_score, 2),
            "approval_decision": approval_decision,
            "interest_rate": round(interest_rate, 2),
            "collateral_required": collateral_required,
            "reasoning": reasoning
        }
    
    @staticmethod
    def calculate_biased_score(profile: Dict[str, Any], fair_score_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate biased score by applying realistic bias penalties.
        
        Biases Applied (MINIMIZED for showcase initial parity ~0.65-0.75):
        1. Rural penalty: -0.3 points (significantly reduced for better parity)
        2. Low income penalty (<₹20L): -0.2 points (significantly reduced)
        3. Self-employed penalty: -0.25 points (significantly reduced)
        4. Tier-2/3 penalty: -0.15 points (significantly reduced)
        5. State-based penalty (Bihar, UP, MP): -0.1 points (significantly reduced)
        6. Single parent/widow penalty: -0.15 points (significantly reduced)
        7. Lower-tier college penalty: -0.25 for tier3, -0.15 for tier2 (significantly reduced)
        
        This ensures initial approval parity is around 0.65-0.75 for showcase, which can be
        improved to ≥0.95 in 5-10 realistic mitigation iterations.
        """
        # Start with fair score if provided, otherwise calculate it
        if fair_score_result:
            base_score = fair_score_result["score"]
        else:
            base_score = DeterministicScoringEngine.calculate_fair_score(profile)["score"]
        
        score = base_score
        
        # Extract profile data
        region = profile.get("region", "").lower()
        state = profile.get("state", "").lower()
        family_income = profile.get("family_income", 2000000)
        employment_type = profile.get("employment_type", "").lower()
        family_structure = profile.get("family_structure", "").lower()
        college_tier = profile.get("college_tier", "").lower() if profile.get("college_tier") else ""
        
        # Bias 1: Rural penalty (-0.3 points, significantly reduced for better parity)
        if "rural" in region:
            score -= 0.3
        
        # Bias 2: Low income penalty (-0.2 points, significantly reduced)
        if family_income < 2000000:  # Less than ₹20L
            score -= 0.2
        
        # Bias 3: Self-employed penalty (-0.25 points, significantly reduced)
        if employment_type == "self-employed":
            score -= 0.25
        
        # Bias 4: Tier-2/3 geographic penalty (-0.15 points, significantly reduced)
        if "tier2" in region or "tier3" in region:
            score -= 0.15
        
        # Bias 5: State-based penalty (-0.1 points, significantly reduced)
        low_credit_states = ["bihar", "up", "uttar pradesh", "mp", "madhya pradesh"]
        if any(state_name in state for state_name in low_credit_states):
            score -= 0.1
        
        # Bias 6: Single parent/widow penalty (-0.15 points, significantly reduced)
        if "single_parent" in family_structure or "widow" in family_structure:
            score -= 0.15
        
        # Bias 7: Lower-tier college penalty (significantly reduced)
        # This reflects real-world bias where lenders prefer top-tier colleges for better placement guarantees
        university_name = profile.get("university_name") or ""
        university_name_lower = university_name.lower() if university_name else ""
        if college_tier == "tier3" or (not college_tier and not any(x in university_name_lower for x in ["iit", "iim", "nit", "bits", "vit"])):
            score -= 0.25  # Tier-3 or unknown colleges penalized (significantly reduced)
        elif college_tier == "tier2":
            score -= 0.15  # Tier-2 colleges get moderate penalty (significantly reduced)
        
        # Ensure score stays within bounds
        score = max(1.0, min(10.0, score))
        
        # Determine approval decision (very lenient thresholds to achieve showcase initial parity ~0.65-0.75)
        # Lower thresholds mean more approvals, leading to better initial parity
        # Count both "approve" and "conditional" as approvals for realistic rates
        if score >= 6.5:
            approval_decision = "approve"
            interest_rate = 9.5
            collateral_required = False
        elif score >= 5.0:
            approval_decision = "approve"
            interest_rate = 10.5
            collateral_required = False
        elif score >= 4.0:
            approval_decision = "approve"  # Much lower threshold for approve
            interest_rate = 11.5
            collateral_required = True
        elif score >= 3.0:
            approval_decision = "conditional"  # Lower threshold for conditional
            interest_rate = 13.0
            collateral_required = True
        elif score >= 2.5:
            approval_decision = "conditional"  # Even lower threshold for conditional
            interest_rate = 14.0
            collateral_required = True
        else:
            approval_decision = "reject"
            interest_rate = 15.0
            collateral_required = True
        
        # Build reasoning that shows bias
        bias_factors = []
        if "rural" in region:
            bias_factors.append("rural location")
        if family_income < 2000000:
            bias_factors.append("lower income bracket")
        if employment_type == "self-employed":
            bias_factors.append("self-employed status")
        if "tier2" in region or "tier3" in region:
            bias_factors.append("tier-2/3 city")
        if any(state_name in state for state_name in low_credit_states):
            bias_factors.append("higher-risk state")
        if "single_parent" in family_structure or "widow" in family_structure:
            bias_factors.append("family structure")
        if college_tier == "tier3" or (not college_tier and not any(x in university_name_lower for x in ["iit", "iim", "nit", "bits", "vit"])):
            bias_factors.append("lower-tier college")
        elif college_tier == "tier2":
            bias_factors.append("mid-tier college")
        
        if bias_factors:
            bias_explanation = f" Adjusted for risk factors: {', '.join(bias_factors)}."
        else:
            bias_explanation = ""
        
        reasoning = (
            f"Risk-adjusted evaluation: Base score {base_score:.2f}, "
            f"Final score {score:.2f}/10.0.{bias_explanation} "
            f"Regional and demographic factors considered in assessment."
        )
        
        return {
            "score": round(score, 2),
            "approval_decision": approval_decision,
            "interest_rate": round(interest_rate, 2),
            "collateral_required": collateral_required,
            "reasoning": reasoning
        }

