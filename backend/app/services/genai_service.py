"""
GenAI service for profile generation and scoring using LangChain + OpenAI/Gemini.
"""

import json
import logging
import random
import uuid
from typing import List, Dict, Any, Optional
import asyncio

# Try to import LangChain packages, but handle if not installed
LANGCHAIN_AVAILABLE = False
try:
    from langchain_openai import ChatOpenAI
    LANGCHAIN_OPENAI_AVAILABLE = True
except ImportError:
    LANGCHAIN_OPENAI_AVAILABLE = False
    ChatOpenAI = None

# Try to import LangChain Gemini first
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_GEMINI_AVAILABLE = True
except ImportError:
    LANGCHAIN_GEMINI_AVAILABLE = False
    ChatGoogleGenerativeAI = None

# Try direct google-generativeai (always try, even if LangChain is available)
GOOGLE_GENAI_AVAILABLE = False
genai = None
try:
    import google.generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    pass

try:
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = LANGCHAIN_OPENAI_AVAILABLE or LANGCHAIN_GEMINI_AVAILABLE
except ImportError:
    # Try alternative import path
    try:
        from langchain_core.messages import HumanMessage, SystemMessage
        LANGCHAIN_AVAILABLE = LANGCHAIN_OPENAI_AVAILABLE or LANGCHAIN_GEMINI_AVAILABLE
    except ImportError:
        LANGCHAIN_AVAILABLE = False

if not LANGCHAIN_AVAILABLE:
    logger = logging.getLogger(__name__)
    logger.warning("LangChain packages not installed, using mock responses")

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    TENACITY_AVAILABLE = True
except ImportError:
    # Mock retry decorator if tenacity not available
    def retry(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    TENACITY_AVAILABLE = False

from app.config import settings
from genai.prompts import (
    format_profile_generation_prompt,
    format_fair_scoring_prompt,
    format_biased_scoring_prompt,
    format_mitigation_prompt,
    format_mitigation_suggestions_prompt,
)

logger = logging.getLogger(__name__)


class GenAIService:
    """Service for GenAI operations using LangChain."""
    
    def __init__(self):
        """Initialize GenAI service with configured provider."""
        self.provider = self._get_provider()
        self.model = self._initialize_model()
        
    def _get_provider(self) -> str:
        """Determine which GenAI provider to use."""
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your-openai-api-key-here":
            return "openai"
        elif settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your-gemini-api-key-here":
            return "gemini"
        else:
            # Return a mock provider for demo purposes
            return "mock"
    
    def _initialize_model(self):
        """Initialize the GenAI model."""
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not available, using mock responses")
            return None
            
        if self.provider == "openai":
            try:
                return ChatOpenAI(
                    model_name=settings.OPENAI_MODEL,
                    temperature=settings.OPENAI_TEMPERATURE,
                    openai_api_key=settings.OPENAI_API_KEY,
                    verbose=settings.LANGCHAIN_VERBOSE,
                )
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}, using mock")
                return None
        elif self.provider == "gemini":
            try:
                # Prefer direct google-generativeai over LangChain for Gemini
                # because LangChain's ChatGoogleGenerativeAI doesn't handle SystemMessage well
                if GOOGLE_GENAI_AVAILABLE and genai:
                    # Use google-generativeai directly
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    # Return a wrapper object that mimics LangChain interface
                    class DirectGeminiModel:
                        def __init__(self, model_name):
                            # Strip 'models/' prefix if present
                            self.model_name = model_name.replace('models/', '')
                            self.model = genai.GenerativeModel(self.model_name)
                        
                        def invoke(self, messages):
                            # Convert messages to text
                            # Gemini doesn't support SystemMessage, so we combine it with HumanMessage
                            text_parts = []
                            for msg in messages:
                                msg_type = type(msg).__name__
                                content = getattr(msg, 'content', str(msg))
                                # For SystemMessage, prepend as instruction
                                if msg_type == 'SystemMessage':
                                    text_parts.append(f"Instructions: {content}")
                                else:
                                    text_parts.append(content)
                            text = "\n\n".join(text_parts)
                            response = self.model.generate_content(text)
                            class Response:
                                content = response.text
                            return Response()
                    
                    return DirectGeminiModel(settings.GEMINI_MODEL)
                elif LANGCHAIN_GEMINI_AVAILABLE and ChatGoogleGenerativeAI:
                    # Fallback to LangChain if direct API not available
                    return ChatGoogleGenerativeAI(
                        model=settings.GEMINI_MODEL,
                        temperature=settings.OPENAI_TEMPERATURE,
                        google_api_key=settings.GEMINI_API_KEY,
                        verbose=settings.LANGCHAIN_VERBOSE,
                    )
                else:
                    logger.warning("No Gemini implementation available")
                    return None
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}, using mock")
                return None
        else:
            # Mock model for demo
            logger.warning("No GenAI API key configured, using mock responses")
            return None
    
    def _generate_mock_profiles(self, count: int) -> str:
        """Generate mock profiles with research-based state distribution and realistic data."""
        profiles = []
        
        # Import realistic Indian names from shared module
        try:
            from app.data.indian_names import INDIAN_NAMES
        except ImportError:
            # Fallback if module doesn't exist
            INDIAN_NAMES = [
                "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
                "Anjali Gupta", "Rahul Mehta", "Kavita Desai", "Suresh Iyer", "Meera Nair",
                "Arjun Joshi", "Divya Rao", "Karan Malhotra", "Pooja Shah", "Nikhil Agarwal",
                "Riya Kapoor", "Aditya Verma", "Shreya Chaturvedi", "Rohan Bhatia", "Neha Trivedi",
                "Ravi Kumar", "Sunita Patel", "Manoj Singh", "Kiran Reddy", "Deepak Sharma",
                "Nisha Gupta", "Vivek Agarwal", "Manisha Desai", "Sachin Iyer", "Preeti Nair",
                "Akshay Kumar", "Jyoti Singh", "Varun Patel", "Swati Reddy", "Ajay Kumar",
                "Kavita Sharma", "Nikhil Patel", "Anita Iyer", "Rohit Nair", "Pooja Desai"
            ]
        
        # Research-based state distribution (same as train_ml_model.py)
        # 57% Southern, 16% Northern, 12% Western, 10% Eastern, 5% Northeastern
        SOUTHERN_STATES = [
            {"state": "Maharashtra", "postcode": "400001", "region": "urban_tier1"},
            {"state": "Kerala", "postcode": "682001", "region": "urban_tier1"},
            {"state": "Andhra Pradesh", "postcode": "500001", "region": "urban_tier1"},
            {"state": "Tamil Nadu", "postcode": "600001", "region": "urban_tier1"},
            {"state": "Karnataka", "postcode": "560001", "region": "urban_tier1"},
            {"state": "Telangana", "postcode": "500001", "region": "urban_tier1"},
            {"state": "Tamil Nadu", "postcode": "625001", "region": "rural_tier2"},
            {"state": "Kerala", "postcode": "686001", "region": "rural_tier2"},
            {"state": "Karnataka", "postcode": "577001", "region": "rural_tier2"},
        ]
        NORTHERN_STATES = [
            {"state": "Uttar Pradesh", "postcode": "201301", "region": "rural_tier2"},
            {"state": "Delhi", "postcode": "110001", "region": "urban_tier1"},
            {"state": "Punjab", "postcode": "141001", "region": "rural_tier2"},
            {"state": "Haryana", "postcode": "121001", "region": "rural_tier2"},
            {"state": "Uttarakhand", "postcode": "248001", "region": "rural_tier2"},
        ]
        WESTERN_STATES = [
            {"state": "Gujarat", "postcode": "380001", "region": "urban_tier1"},
            {"state": "Rajasthan", "postcode": "302001", "region": "rural_tier2"},
            {"state": "Madhya Pradesh", "postcode": "486001", "region": "rural_tier2"},
        ]
        EASTERN_STATES = [
            {"state": "West Bengal", "postcode": "700001", "region": "urban_tier1"},
            {"state": "Bihar", "postcode": "841427", "region": "rural_tier3"},
            {"state": "Odisha", "postcode": "751001", "region": "rural_tier3"},
            {"state": "Jharkhand", "postcode": "834001", "region": "rural_tier3"},
        ]
        NORTHEASTERN_STATES = [
            {"state": "Assam", "postcode": "781001", "region": "rural_tier3"},
            {"state": "Tripura", "postcode": "799001", "region": "rural_tier3"},
            {"state": "Manipur", "postcode": "795001", "region": "rural_tier3"},
        ]
        
        # Weighted state list
        ALL_STATES_WEIGHTED = (
            SOUTHERN_STATES * 57 +
            NORTHERN_STATES * 16 +
            WESTERN_STATES * 12 +
            EASTERN_STATES * 10 +
            NORTHEASTERN_STATES * 5
        )
        random.shuffle(ALL_STATES_WEIGHTED)
        
        # Course distribution: Engineering 52%, Commerce/MBA 14%, Science 20%, Arts 14%
        courses_engineering = ["BTech", "BE", "MTech", "BArch", "MCA"]
        courses_commerce = ["BCom", "MCom", "MBA", "BBA", "PGDM"]
        courses_science = ["BSc", "MSc", "MBBS", "BPharm"]
        courses_arts = ["BA", "MA", "BFA"]
        
        # Indian colleges/universities by tier
        tier1_colleges = [
            "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur",
            "IIT Roorkee", "IIT Guwahati", "IIM Ahmedabad", "IIM Bangalore", "IIM Calcutta",
            "AIIMS Delhi", "BITS Pilani", "NIT Trichy", "NIT Warangal", "JNU Delhi"
        ]
        tier2_colleges = [
            "NIT Surathkal", "NIT Rourkela", "VIT Vellore", "Manipal University", "SRM University",
            "Amity University", "Symbiosis International", "NMIMS Mumbai", "Xavier's College",
            "St. Stephen's College", "Lady Shri Ram College", "Christ University", "PES University"
        ]
        tier3_colleges = [
            "State Engineering College", "Regional University", "City College", "Local University",
            "District College", "Private Engineering College", "State Commerce College"
        ]
        
        # Employment distribution
        employment_weights = [("salaried", 50), ("self-employed", 20), ("government", 15), ("student", 10), ("other", 5)]
        family_structure_weights = [("nuclear", 60), ("joint", 25), ("single_parent", 10), ("widow", 5)]
        co_applicant_weights = [("parent", 60), ("sibling", 20), ("spouse", 10), ("none", 10)]
        
        def weighted_choice(choices):
            total = sum(w for _, w in choices)
            r = random.uniform(0, total)
            upto = 0
            for item, weight in choices:
                upto += weight
                if upto >= r:
                    return item
            return choices[0][0]
        
        for i in range(count):
            # Use research-based state distribution
            state_info = ALL_STATES_WEIGHTED[i % len(ALL_STATES_WEIGHTED)]
            
            # Realistic name
            name = INDIAN_NAMES[i % len(INDIAN_NAMES)]
            
            # Realistic income based on region (research-based)
            if state_info["region"] == "urban_tier1":
                if random.random() < 0.6:
                    family_income = int(random.gauss(2900000, 700000))  # Mean ₹29L
                elif random.random() < 0.8:
                    family_income = random.randint(1800000, 4000000)
                else:
                    family_income = random.randint(1200000, 1800000)
            elif state_info["region"] == "rural_tier2":
                if random.random() < 0.5:
                    family_income = int(random.gauss(1750000, 450000))  # Mean ₹17.5L
                else:
                    family_income = random.randint(800000, 2500000)
            else:  # rural_tier3
                if random.random() < 0.55:
                    family_income = int(random.gauss(1000000, 300000))  # Mean ₹10L
                else:
                    family_income = random.randint(500000, 1500000)
            
            family_income = max(400000, min(6000000, family_income))
            
            # Realistic loan amount (research-based: average ₹8-9L)
            course_roll = random.random()
            if course_roll < 0.6:  # Engineering (most common)
                base_loan = int(random.gauss(1000000, 200000))  # ₹8-12L
            elif course_roll < 0.85:  # MBA/Business
                base_loan = int(random.gauss(1200000, 300000))  # ₹9-15L
            else:  # General courses
                base_loan = int(random.gauss(900000, 250000))  # ₹6.5-11.5L
            
            # Adjust based on income (50-120% of income for education loans)
            if family_income < 1000000:
                income_ratio = random.uniform(0.8, 1.2)  # Higher ratio for low income (aspirational)
            elif family_income < 2500000:
                income_ratio = random.uniform(0.5, 0.9)
            else:
                income_ratio = random.uniform(0.4, 0.7)
            
            income_based_loan = int(family_income * income_ratio)
            requested_loan_amount = min(int(0.6 * base_loan + 0.4 * income_based_loan), 3000000)  # Max ₹30L
            requested_loan_amount = max(300000, requested_loan_amount)  # Min ₹3L
            
            # Realistic CIBIL score distribution (research-based)
            cibil_roll = random.random()
            if cibil_roll < 0.15:  # 15% poor credit
                cibil_score = int(random.gauss(500, 100))
            elif cibil_roll < 0.60:  # 45% average credit (600-750)
                cibil_score = int(random.gauss(675, 50))
            elif cibil_roll < 0.90:  # 30% good credit (750-850)
                cibil_score = int(random.gauss(800, 50))
            else:  # 10% excellent credit
                cibil_score = int(random.gauss(875, 25))
            cibil_score = max(300, min(900, cibil_score))
            
            # Course selection with distribution
            course_choice = random.random()
            if course_choice < 0.52:  # Engineering 52%
                course = random.choice(courses_engineering)
                educational_background = "Engineering"
                gpa = max(5.0, min(10.0, round(random.gauss(7.5, 1.2), 2)))
            elif course_choice < 0.66:  # Commerce/MBA 14%
                course = random.choice(courses_commerce)
                educational_background = "Commerce"
                gpa = max(5.0, min(10.0, round(random.gauss(7.8, 1.1), 2)))
            elif course_choice < 0.86:  # Science 20%
                course = random.choice(courses_science)
                educational_background = "Science"
                gpa = max(5.0, min(10.0, round(random.gauss(7.3, 1.2), 2)))
            else:  # Arts 14%
                course = random.choice(courses_arts)
                educational_background = "Arts"
                gpa = max(5.0, min(10.0, round(random.gauss(7.0, 1.3), 2)))
            
            # Assign college tier and university based on GPA and course (realistic correlation)
            # Higher GPA = higher chance of tier-1 college (better admission letter)
            college_tier_roll = random.random()
            if gpa >= 8.5 and college_tier_roll < 0.35:  # 35% chance of tier-1 with high GPA
                college_tier = "tier1"
                university_name = random.choice(tier1_colleges)
            elif gpa >= 7.5 and college_tier_roll < 0.25:  # 25% chance with good GPA
                college_tier = "tier1"
                university_name = random.choice(tier1_colleges)
            elif gpa >= 7.0 and college_tier_roll < 0.55:  # 55% chance of tier-2 with decent GPA
                college_tier = "tier2"
                university_name = random.choice(tier2_colleges)
            elif gpa >= 6.0 and college_tier_roll < 0.40:  # 40% chance of tier-2
                college_tier = "tier2"
                university_name = random.choice(tier2_colleges)
            else:  # Tier-3 or unknown
                if college_tier_roll < 0.70:  # 70% explicitly tier-3
                    college_tier = "tier3"
                    university_name = random.choice(tier3_colleges)
                else:  # 30% unknown/other
                    college_tier = "tier3"
                    university_name = random.choice(tier3_colleges)
            
            # Profile ID will be assigned sequentially when saved to DB
            # Using temporary format for now - will be updated during save
            profile = {
                "profile_id": f"stud_temp_{uuid.uuid4().hex[:6]}",  # Temporary, will be reassigned
                "name": name,  # Realistic Indian name (no numbers)
                "postcode": state_info["postcode"],
                "region": state_info["region"],
                "state": state_info["state"],  # Research-based distribution
                "family_income": family_income,  # Research-based income distribution
                "cibil_score": cibil_score,  # Research-based CIBIL distribution
                "requested_loan_amount": requested_loan_amount,  # Research-based loan amount
                "gpa": gpa,  # Course-specific GPA distribution
                "course": course,
                "educational_background": educational_background,
                "college_tier": college_tier,  # tier1, tier2, tier3
                "university_name": university_name,  # Name of college/university
                "co_applicant": weighted_choice(co_applicant_weights),
                "employment_type": weighted_choice(employment_weights),
                "family_structure": weighted_choice(family_structure_weights),
                "test_dimension": random.choice(["geographic", "income", "credit", "edge_cases"])
            }
            profiles.append(profile)
        return json.dumps(profiles)
    
    def _generate_mock_scoring(self, profile: Dict, scoring_type: str, loan_amount: int) -> str:
        """Generate mock scoring for demo."""
        # Use 10-point GPA scale
        gpa_val = profile.get("gpa", 7.0)
        if gpa_val <= 4.0:
            # Convert 4-point to 10-point if needed
            gpa_val = gpa_val * 2.5
        
        base_score = 5.0 + (profile.get("cibil_score", 650) - 650) / 100
        base_score += (gpa_val - 5.0) * 0.3  # GPA contribution (5.0-10.0 scale)
        
        if scoring_type == "biased":
            # Apply bias
            if "rural" in profile.get("region", ""):
                base_score -= 2.0
            if profile.get("family_income", 0) < 2000000:
                base_score -= 1.0
        
        score = max(1.0, min(10.0, base_score))
        approval = "approve" if score >= 7 else "conditional" if score >= 5 else "reject"
        interest_rate = 9.0 if score >= 9 else 11.0 if score >= 7 else 13.0 if score >= 5 else 15.0
        
        result = {
            "score": round(score, 2),
            "approval_decision": approval,
            "interest_rate": interest_rate,
            "collateral_required": score < 7,
            "reasoning": f"Mock scoring: {scoring_type} model"
        }
        return json.dumps(result)
    
    @retry(stop=stop_after_attempt(3) if TENACITY_AVAILABLE else lambda x: x, wait=wait_exponential(multiplier=1, min=4, max=10) if TENACITY_AVAILABLE else lambda x: x)
    async def generate_profiles(
        self,
        count: int,
        dimensions: List[str],
        batch_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic student profiles using GenAI.
        
        Args:
            count: Number of profiles to generate
            dimensions: List of test dimensions to cover
            batch_size: Number of profiles to generate per batch
            
        Returns:
            List of profile dictionaries
        """
        try:
            logger.info(f"Generating {count} profiles with dimensions: {dimensions}")
            
            prompt = format_profile_generation_prompt(count, dimensions)
            
            # Generate in batches
            all_profiles = []
            batches = (count + batch_size - 1) // batch_size
            
            for batch_num in range(batches):
                batch_count = min(batch_size, count - len(all_profiles))
                logger.info(f"Generating batch {batch_num + 1}/{batches} ({batch_count} profiles)")
                
                batch_prompt = format_profile_generation_prompt(batch_count, dimensions)
                # Call GenAI (async) or use mock
                if self.model and LANGCHAIN_AVAILABLE:
                    try:
                        messages = [
                            SystemMessage(content="You are a data scientist generating realistic Indian student loan applications. Always return valid JSON arrays."),
                            HumanMessage(content=batch_prompt)
                        ]
                        response = await asyncio.to_thread(self.model.invoke, messages)
                        content = response.content
                    except Exception as e:
                        logger.warning(f"GenAI call failed: {e}, using mock")
                        content = self._generate_mock_profiles(batch_count)
                else:
                    # Mock response for demo
                    content = self._generate_mock_profiles(batch_count)
                
                # Parse JSON response
                try:
                    # Extract JSON from markdown code blocks if present
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    
                    profiles = json.loads(content)
                    if not isinstance(profiles, list):
                        profiles = [profiles]
                    
                    all_profiles.extend(profiles)
                    logger.info(f"Generated {len(profiles)} profiles in batch {batch_num + 1}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    logger.error(f"Response content: {content[:500]}")
                    raise ValueError(f"Invalid JSON response from GenAI: {e}")
                
                # Rate limiting
                await asyncio.sleep(1)
            
            logger.info(f"Successfully generated {len(all_profiles)} profiles")
            return all_profiles
            
        except Exception as e:
            logger.error(f"Error generating profiles: {e}", exc_info=True)
            raise
    
    @retry(stop=stop_after_attempt(3) if TENACITY_AVAILABLE else lambda x: x, wait=wait_exponential(multiplier=1, min=4, max=10) if TENACITY_AVAILABLE else lambda x: x)
    async def score_profile(
        self,
        profile: Dict[str, Any],
        scoring_type: str,
        loan_amount: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Score a single profile using GenAI.
        
        Args:
            profile: Profile dictionary
            scoring_type: "fair" or "biased"
            loan_amount: Requested loan amount (defaults to profile's requested_loan_amount)
            
        Returns:
            Scoring result dictionary
        """
        try:
            loan_amount = loan_amount or profile.get("requested_loan_amount", settings.DEFAULT_LOAN_AMOUNT)
            profile_json = json.dumps(profile, indent=2)
            
            if scoring_type == "fair":
                prompt = format_fair_scoring_prompt(profile_json, loan_amount)
            elif scoring_type == "biased":
                prompt = format_biased_scoring_prompt(profile_json, loan_amount)
            else:
                raise ValueError(f"Invalid scoring_type: {scoring_type}")
            
            # Call GenAI (async) or use mock
            if self.model and LANGCHAIN_AVAILABLE:
                try:
                    messages = [
                        SystemMessage(content="You are a loan approval AI system. Always return valid JSON only, no additional text."),
                        HumanMessage(content=prompt)
                    ]
                    response = await asyncio.to_thread(self.model.invoke, messages)
                    content = response.content.strip()
                except Exception as e:
                    logger.warning(f"GenAI call failed: {e}, using mock")
                    content = self._generate_mock_scoring(profile, scoring_type, loan_amount)
            else:
                content = self._generate_mock_scoring(profile, scoring_type, loan_amount)
            
            # Parse JSON response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                
                # Validate result
                if "score" not in result:
                    raise ValueError("Missing 'score' in response")
                if "approval_decision" not in result:
                    raise ValueError("Missing 'approval_decision' in response")
                if "interest_rate" not in result:
                    raise ValueError("Missing 'interest_rate' in response")
                if "collateral_required" not in result:
                    raise ValueError("Missing 'collateral_required' in response")
                
                # Validate ranges
                result["score"] = max(1.0, min(10.0, float(result["score"])))
                result["interest_rate"] = max(8.0, min(15.0, float(result["interest_rate"])))
                
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response content: {content[:500]}")
                raise ValueError(f"Invalid JSON response from GenAI: {e}")
                
        except Exception as e:
            logger.error(f"Error scoring profile: {e}", exc_info=True)
            raise
    
    async def score_profiles_batch(
        self,
        profiles: List[Dict[str, Any]],
        scoring_type: str,
        batch_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Score multiple profiles in parallel batches.
        
        Args:
            profiles: List of profile dictionaries
            scoring_type: "fair" or "biased"
            batch_size: Number of profiles to score concurrently
            
        Returns:
            List of scoring results
        """
        try:
            logger.info(f"Scoring {len(profiles)} profiles with type: {scoring_type}")
            
            results = []
            batches = [profiles[i:i + batch_size] for i in range(0, len(profiles), batch_size)]
            
            for batch_num, batch in enumerate(batches):
                logger.info(f"Scoring batch {batch_num + 1}/{len(batches)} ({len(batch)} profiles)")
                
                # Score profiles in parallel
                tasks = [self.score_profile(profile, scoring_type) for profile in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Handle results and errors
                for i, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        logger.error(f"Error scoring profile {batch[i].get('profile_id')}: {result}")
                        results.append({
                            "profile": batch[i],
                            "error": str(result),
                            "success": False
                        })
                    else:
                        results.append({
                            "profile": batch[i],
                            "result": result,
                            "success": True
                        })
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            logger.info(f"Successfully scored {len([r for r in results if r.get('success')])} profiles")
            return results
            
        except Exception as e:
            logger.error(f"Error scoring profiles batch: {e}", exc_info=True)
            raise
    
    async def generate_mitigation_prompt(
        self,
        feedback_summary: str,
        finding_description: str,
        root_cause: str,
        severity: str,
        group1_name: str,
        group2_name: str,
        approval_parity: float,
        interest_gap: float,
        collateral_gap: float,
        fairness_score: float,
        human_suggestions: str,
        iteration_number: int = 1
    ) -> Dict[str, Any]:
        """
        Generate a refined prompt for bias mitigation.
        
        Args:
            feedback_summary: Summary of human feedback
            finding_description: Description of the bias finding
            root_cause: Root cause analysis
            severity: Severity level
            group1_name: Name of first group
            group2_name: Name of second group
            approval_parity: Approval parity metric
            interest_gap: Interest rate gap
            collateral_gap: Collateral gap
            fairness_score: Current fairness score
            human_suggestions: Human-suggested mitigations
            
        Returns:
            Dictionary with refined prompt and reasoning
        """
        try:
            prompt = format_mitigation_prompt(
                feedback_summary=feedback_summary,
                finding_description=finding_description,
                root_cause=root_cause,
                severity=severity,
                group1_name=group1_name,
                group2_name=group2_name,
                approval_parity=approval_parity,
                interest_gap=interest_gap,
                collateral_gap=collateral_gap,
                fairness_score=fairness_score,
                human_suggestions=human_suggestions,
                iteration_number=iteration_number
            )
            
            # Call GenAI (async) or use mock
            if self.model and LANGCHAIN_AVAILABLE and self.model != "quota_exceeded":
                try:
                    messages = [
                        SystemMessage(content="You are a bias mitigation expert. Always return valid JSON only."),
                        HumanMessage(content=prompt)
                    ]
                    response = await asyncio.to_thread(self.model.invoke, messages)
                    content = response.content.strip()
                except Exception as e:
                    error_str = str(e)
                    # Check for quota exceeded (429)
                    if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
                        logger.warning("GenAI quota exceeded for mitigation prompt generation, using deterministic-based refinement")
                        self.model = "quota_exceeded"  # Mark as quota exceeded
                        # Generate a refined prompt based on feedback without GenAI
                        content = self._generate_refined_prompt_from_feedback(
                            feedback_summary, finding_description, root_cause, severity,
                            group1_name, group2_name, approval_parity, interest_gap,
                            collateral_gap, fairness_score, human_suggestions, iteration_number
                        )
                    else:
                        logger.warning(f"GenAI call failed: {e}, using mock")
                        content = json.dumps({
                            "refined_prompt": prompt,
                            "reasoning": "Mock mitigation response",
                            "changes_made": "Mock changes",
                            "expected_improvement": 10.0
                        })
            else:
                content = json.dumps({
                    "refined_prompt": prompt,
                    "reasoning": "Mock mitigation response - no GenAI API key configured",
                    "changes_made": "Mock changes for demo",
                    "expected_improvement": 10.0
                })
            
            # Parse JSON response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response content: {content[:500]}")
                raise ValueError(f"Invalid JSON response from GenAI: {e}")
                
        except Exception as e:
            logger.error(f"Error generating mitigation prompt: {e}", exc_info=True)
            raise
    
    async def suggest_mitigation(
        self,
        group1_name: str,
        group2_name: str,
        dimension: str,
        approval_parity: float,
        interest_gap: float,
        collateral_gap: float,
        fairness_score: float,
        severity: str
    ) -> Dict[str, Any]:
        """
        Generate AI-powered mitigation suggestions for a bias finding.
        
        Returns:
            Dictionary with suggestions list and priority order
        """
        try:
            prompt = format_mitigation_suggestions_prompt(
                group1_name=group1_name,
                group2_name=group2_name,
                dimension=dimension,
                approval_parity=approval_parity,
                interest_gap=interest_gap,
                collateral_gap=collateral_gap,
                fairness_score=fairness_score,
                severity=severity
            )
            
            # Call GenAI or use mock
            if self.model and LANGCHAIN_AVAILABLE and self.model != "quota_exceeded":
                try:
                    messages = [{"role": "user", "content": prompt}]
                    response = await asyncio.to_thread(self.model.invoke, messages)
                    content = response.content.strip()
                except Exception as e:
                    error_str = str(e)
                    # Check for quota exceeded (429)
                    if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
                        logger.warning("GenAI quota exceeded for suggestions, using mock")
                        self.model = "quota_exceeded"  # Mark as quota exceeded
                    else:
                        logger.warning(f"GenAI call failed: {e}, using mock")
                    # Generate tailored mock suggestions based on dimension
                    suggestions = self._generate_tailored_mock_suggestions(
                        dimension, group1_name, group2_name, approval_parity, 
                        interest_gap, collateral_gap, fairness_score, severity
                    )
                    content = json.dumps(suggestions)
            else:
                # Generate tailored mock suggestions when GenAI not available
                suggestions = self._generate_tailored_mock_suggestions(
                    dimension, group1_name, group2_name, approval_parity,
                    interest_gap, collateral_gap, fairness_score, severity
                )
                content = json.dumps(suggestions)
            
            # Parse JSON response
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(content)
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Response content: {content[:500]}")
                # Return fallback suggestions
                return {
                    "suggestions": [
                        {
                            "title": "Review Scoring Criteria",
                            "description": "Review and adjust scoring criteria to remove bias factors.",
                            "expected_impact": "Improved fairness",
                            "implementation_complexity": "medium"
                        }
                    ],
                    "priority_order": ["Review Scoring Criteria"]
                }
                
        except Exception as e:
            logger.error(f"Error generating mitigation suggestions: {e}", exc_info=True)
            raise
    
    def _generate_refined_prompt_from_feedback(
        self,
        feedback_summary: str,
        finding_description: str,
        root_cause: str,
        severity: str,
        group1_name: str,
        group2_name: str,
        approval_parity: float,
        interest_gap: float,
        collateral_gap: float,
        fairness_score: float,
        human_suggestions: str,
        iteration_number: int
    ) -> str:
        """Generate a refined prompt based on feedback without GenAI (when quota exceeded)."""
        from genai.prompts import FAIR_SCORING_PROMPT
        
        # Start with base fair scoring prompt
        refined_prompt = FAIR_SCORING_PROMPT
        
        # Apply conservative changes based on feedback
        changes = []
        
        # If root cause mentions geographic bias, add explicit exclusion
        if "geographic" in root_cause.lower() or "region" in root_cause.lower() or "postcode" in root_cause.lower():
            refined_prompt += "\n\nCRITICAL FAIRNESS REQUIREMENT: Do not consider geographic location (postcode, region, state, tier) in scoring. These factors must be completely ignored."
            changes.append("Added explicit exclusion of geographic factors")
        
        # If root cause mentions income bias, normalize income
        if "income" in root_cause.lower() and "absolute" in root_cause.lower():
            refined_prompt += "\n\nINCOME NORMALIZATION: Use income-to-loan ratio instead of absolute income. Calculate ITL ratio = Annual Income / Loan Amount. Set approval threshold at ITL > 0.25."
            changes.append("Added income-to-loan ratio normalization")
        
        # If root cause mentions employment type bias
        if "employment" in root_cause.lower() or "self-employed" in root_cause.lower():
            refined_prompt += "\n\nEMPLOYMENT TYPE: Do not penalize self-employed applicants. Evaluate income stability using documented income (tax returns, bank statements) regardless of employment type."
            changes.append("Removed employment type bias")
        
        # If root cause mentions family structure
        if "family" in root_cause.lower() or "single parent" in root_cause.lower():
            refined_prompt += "\n\nFAMILY STRUCTURE: Do not consider family structure (single-parent, nuclear, joint) in scoring. Focus only on financial indicators."
            changes.append("Removed family structure bias")
        
        # Add human suggestions as explicit instructions
        if human_suggestions:
            refined_prompt += f"\n\nHUMAN FEEDBACK GUIDANCE:\n{human_suggestions}"
            changes.append("Incorporated human feedback suggestions")
        
        # Create response
        result = {
            "refined_prompt": refined_prompt,
            "reasoning": f"Generated refined prompt based on feedback analysis. Iteration {iteration_number} focuses on addressing {root_cause[:100]}",
            "changes_made": "; ".join(changes) if changes else "Conservative adjustments based on feedback",
            "expected_improvement": f"{5 + (iteration_number * 2)}%",  # Conservative 5-15% improvement
            "risk_assessment": "Low risk - conservative changes maintain scoring integrity"
        }
        
        return json.dumps(result)
    
    def _generate_tailored_mock_suggestions(
        self,
        dimension: str,
        group1_name: str,
        group2_name: str,
        approval_parity: float,
        interest_gap: float,
        collateral_gap: float,
        fairness_score: float,
        severity: str
    ) -> Dict[str, Any]:
        """Generate tailored mock suggestions based on the specific bias metric."""
        suggestions = []
        
        # Dimension-specific suggestions
        if dimension.lower() == "geographic":
            suggestions.extend([
                {
                    "title": f"Remove Geographic Location from Scoring",
                    "description": f"Eliminate all geographic indicators (region, postcode, state, tier classification) from scoring calculations for {group1_name} vs {group2_name}. Use only merit-based factors: GPA, CIBIL score, income-to-loan ratio, and academic credentials.",
                    "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                    "implementation_complexity": "medium"
                },
                {
                    "title": "Normalize for Regional Cost Differences",
                    "description": f"Use income-to-loan ratio instead of absolute income to account for regional cost-of-living differences. This ensures {group1_name} and {group2_name} applicants with equivalent repayment capacity receive similar scores.",
                    "expected_impact": "Reduce interest rate disparity and improve fairness score",
                    "implementation_complexity": "low"
                },
                {
                    "title": "Add Geographic Bias Monitoring",
                    "description": f"Implement real-time monitoring of approval rates by geographic groups. Set automated alerts when approval parity between {group1_name} and {group2_name} deviates beyond 0.95-1.05 range.",
                    "expected_impact": "Early detection and prevention of geographic bias",
                    "implementation_complexity": "medium"
                }
            ])
        elif dimension.lower() == "income":
            suggestions.extend([
                {
                    "title": f"Replace Absolute Income with Income-to-Loan Ratio",
                    "description": f"Use income-to-loan ratio (ITL) instead of absolute income thresholds. Set fair ITL thresholds (>0.25 for approval) that apply equally to {group1_name} and {group2_name} applicants.",
                    "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                    "implementation_complexity": "low"
                },
                {
                    "title": "Add Compensating Factors for Lower Income",
                    "description": f"Allow strong academic merit (GPA >9.0) or excellent credit scores (CIBIL >750) to compensate for lower family income. This ensures {group2_name} applicants with strong credentials aren't penalized.",
                    "expected_impact": "Reduce income-based discrimination while maintaining risk assessment",
                    "implementation_complexity": "medium"
                },
                {
                    "title": "Standardize Interest Rate Calculation",
                    "description": f"Base interest rates solely on credit score and loan amount, removing income-based pricing adjustments. This reduces interest rate disparity between {group1_name} and {group2_name}.",
                    "expected_impact": f"Reduce interest rate gap from {interest_gap:.2f}%",
                    "implementation_complexity": "low"
                }
            ])
        elif dimension.lower() == "credit":
            suggestions.extend([
                {
                    "title": f"Distinguish Credit History from Credit Score",
                    "description": f"For {group2_name} applicants with limited credit history (first-time borrowers), rely more heavily on academic merit and co-applicant credit scores rather than penalizing for low scores.",
                    "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                    "implementation_complexity": "medium"
                },
                {
                    "title": "Implement Tiered Interest Rates Instead of Rejection",
                    "description": f"Use credit scores for interest rate determination rather than binary approval/rejection. {group2_name} applicants with fair credit (650-750) should receive conditional approval with slightly higher rates.",
                    "expected_impact": "Reduce approval disparity while maintaining risk management",
                    "implementation_complexity": "low"
                },
                {
                    "title": "Consider Co-Applicant Credit for Students",
                    "description": f"For student loans, prioritize parent/spouse co-applicant credit scores over student's limited credit history. This provides fair assessment for {group2_name} applicants.",
                    "expected_impact": "Improve fairness for first-time borrowers",
                    "implementation_complexity": "low"
                }
            ])
        elif "edge" in dimension.lower():
            if "self-employed" in group1_name.lower() or "self-employed" in group2_name.lower():
                suggestions.extend([
                    {
                        "title": f"Remove Employment Type Penalty",
                        "description": f"Eliminate employment type (self-employed vs salaried) as a direct penalty factor. Instead, evaluate income stability using 2-3 years of tax returns and bank statements for {group1_name} applicants.",
                        "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                        "implementation_complexity": "medium"
                    },
                    {
                        "title": "Use Income Volatility Instead of Employment Type",
                        "description": f"Replace employment type bias with income volatility metrics (month-to-month variation). Stable self-employed applicants with consistent income should be treated like salaried employees.",
                        "expected_impact": "Fair assessment based on actual financial stability",
                        "implementation_complexity": "medium"
                    }
                ])
            elif "single" in group1_name.lower() or "single" in group2_name.lower() or "nuclear" in group1_name.lower() or "nuclear" in group2_name.lower():
                suggestions.extend([
                    {
                        "title": f"Remove Family Structure from Scoring",
                        "description": f"Completely eliminate family structure (single-parent, nuclear, joint family) from all scoring calculations. Family structure has no correlation with loan repayment ability.",
                        "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                        "implementation_complexity": "low"
                    },
                    {
                        "title": "Focus on Actual Financial Indicators",
                        "description": f"Use only financial metrics: income, credit score, employment stability. {group1_name} and {group2_name} applicants with equivalent financials should receive identical scores.",
                        "expected_impact": "Eliminate family structure discrimination",
                        "implementation_complexity": "low"
                    }
                ])
            else:
                suggestions.extend([
                    {
                        "title": f"Review Edge Case Handling",
                        "description": f"Ensure {group1_name} and {group2_name} edge cases are evaluated using the same merit-based criteria as standard applicants. Remove any special penalties or bonuses for edge case categories.",
                        "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                        "implementation_complexity": "medium"
                    }
                ])
        else:
            # Generic suggestions for unknown dimensions
            suggestions.extend([
                {
                    "title": f"Remove {dimension.title()} Bias Factors",
                    "description": f"Identify and eliminate variables that create bias between {group1_name} and {group2_name}. Focus scoring on merit-based factors only: academic credentials, creditworthiness, and repayment capacity.",
                    "expected_impact": f"Improve approval parity from {approval_parity:.2f} towards 1.0",
                    "implementation_complexity": "medium"
                },
                {
                    "title": "Standardize Scoring Criteria",
                    "description": f"Ensure {group1_name} and {group2_name} applicants with equivalent merit receive identical scores. Remove any demographic or categorical factors from scoring.",
                    "expected_impact": "Improve overall fairness score",
                    "implementation_complexity": "medium"
                }
            ])
        
        # Add monitoring suggestion if severity is high
        if severity.lower() in ["critical", "high"]:
            suggestions.append({
                "title": "Implement Continuous Bias Monitoring",
                "description": f"Set up automated monitoring for {dimension} bias with alerts when approval parity deviates beyond acceptable range (0.95-1.05). Track {group1_name} vs {group2_name} metrics in real-time.",
                "expected_impact": "Early detection and prevention of bias recurrence",
                "implementation_complexity": "medium"
            })
        
        return {
            "suggestions": suggestions[:5],  # Limit to 5 suggestions
            "priority_order": [s["title"] for s in suggestions[:5]]
        }


# Global service instance
genai_service = GenAIService()

