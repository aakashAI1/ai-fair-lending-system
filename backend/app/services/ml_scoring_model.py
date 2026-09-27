"""
Machine Learning scoring models for loan approval.
Can be trained on real datasets to learn patterns.
"""

import logging
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

logger = logging.getLogger(__name__)


class MLScoringModel:
    """
    Machine Learning model for loan approval scoring.
    Can be trained on real datasets to learn patterns.
    """
    
    def __init__(self, model_type: str = "random_forest"):
        """
        Initialize ML model.
        
        Args:
            model_type: Type of model to use
                - "random_forest": Random Forest (recommended, handles non-linearity)
                - "gradient_boosting": Gradient Boosting (better accuracy, slower)
                - "logistic_regression": Logistic Regression (fast, interpretable)
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.is_trained = False
        self.model_path = Path(__file__).parent.parent.parent / "models" / "scoring_model.pkl"
        self.model_path.parent.mkdir(exist_ok=True)
    
    def _create_model(self):
        """Create the ML model based on type."""
        if self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=20,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "gradient_boosting":
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        elif self.model_type == "logistic_regression":
            self.model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                solver='lbfgs'
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def _prepare_features(self, df: pd.DataFrame, is_training: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features for ML model.
        Converts categorical to numeric and scales features.
        """
        # During training, determine features from data
        # During prediction, use stored feature_names from model if available
        if is_training:
            # Select features (college_tier is optional - only include if present)
            base_feature_cols = [
                'gpa', 'cibil_score', 'family_income', 'requested_loan_amount',
                'educational_background', 'employment_type', 'co_applicant',
                'family_structure', 'region', 'state'
            ]
            
            # Add college_tier only if it exists in the dataframe
            if 'college_tier' in df.columns:
                feature_cols = base_feature_cols + ['college_tier']
            else:
                feature_cols = base_feature_cols
        else:
            # During prediction, use stored feature names from model
            if hasattr(self, 'feature_names') and self.feature_names:
                feature_cols = list(self.feature_names)
            else:
                # Fallback: determine from data
                base_feature_cols = [
                    'gpa', 'cibil_score', 'family_income', 'requested_loan_amount',
                    'educational_background', 'employment_type', 'co_applicant',
                    'family_structure', 'region', 'state'
                ]
                if 'college_tier' in df.columns:
                    feature_cols = base_feature_cols + ['college_tier']
                else:
                    feature_cols = base_feature_cols
        
        # Filter to available columns and add missing ones with defaults
        available_cols = []
        df_features = df.copy()
        for col in feature_cols:
            if col in df.columns:
                available_cols.append(col)
            else:
                # Add missing column with default value
                if col == 'college_tier':
                    df_features[col] = 'tier3'
                    available_cols.append(col)
                else:
                    df_features[col] = 0
                    available_cols.append(col)
        
        df_features = df_features[available_cols].copy()
        
        # Fill missing college_tier if present
        if 'college_tier' in df_features.columns:
            df_features['college_tier'] = df_features['college_tier'].fillna('tier3')
        
        # Encode categorical variables (only include college_tier if present)
        base_categorical_cols = ['educational_background', 'employment_type', 
                          'co_applicant', 'family_structure', 'region', 'state']
        categorical_cols = base_categorical_cols + (['college_tier'] if 'college_tier' in df_features.columns else [])
        
        for col in categorical_cols:
            if col in df_features.columns:
                if is_training:
                    le = LabelEncoder()
                    df_features[col] = le.fit_transform(df_features[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        le = self.label_encoders[col]
                        df_features[col] = df_features[col].astype(str).apply(
                            lambda x: x if x in le.classes_ else le.classes_[0]
                        )
                        df_features[col] = le.transform(df_features[col])
                    else:
                        # Default encoding
                        df_features[col] = 0
        
        # Fill missing values
        df_features = df_features.fillna(df_features.median() if is_training else 0)
        
        # Scale features
        if is_training:
            X_scaled = self.scaler.fit_transform(df_features)
        else:
            X_scaled = self.scaler.transform(df_features)
        
        self.feature_names = available_cols
        
        return X_scaled, df_features.values
    
    def train(self, profiles_df: pd.DataFrame, target_column: str = "approval_decision", 
              test_size: float = 0.2) -> Dict[str, Any]:
        """
        Train the ML model on dataset.
        
        Args:
            profiles_df: DataFrame with profiles and target labels
            target_column: Column name with approval decisions ('approve', 'reject', 'conditional')
            test_size: Fraction of data for testing
            
        Returns:
            Training metrics
        """
        try:
            logger.info(f"Training {self.model_type} model on {len(profiles_df)} profiles")
            
            # Create model
            self._create_model()
            
            # Prepare features
            X, _ = self._prepare_features(profiles_df, is_training=True)
            
            # Prepare target (convert to binary: approve=1, reject/conditional=0)
            y = profiles_df[target_column].apply(
                lambda x: 1 if str(x).lower() == 'approve' else 0
            )
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Train model
            logger.info(f"Training on {len(X_train)} samples...")
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Model accuracy: {accuracy:.3f}")
            
            # Save model
            self._save_model()
            self.is_trained = True
            
            return {
                "accuracy": float(accuracy),
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "model_type": self.model_type,
                "features": self.feature_names
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}", exc_info=True)
            raise
    
    def predict_score(self, profile: Dict[str, Any], apply_bias: bool = False) -> Dict[str, Any]:
        """
        Predict loan approval score for a profile.
        
        Args:
            profile: Profile dictionary
            apply_bias: Whether to apply bias penalties (for biased model)
            
        Returns:
            Scoring result dictionary
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        try:
            # Convert profile to DataFrame
            profile_df = pd.DataFrame([profile])
            
            # Prepare features (will handle missing features automatically)
            X, _ = self._prepare_features(profile_df, is_training=False)
            
            # Predict probability
            prob = self.model.predict_proba(X)[0]
            # Model is trained with binary labels: 0=reject, 1=approve
            # sklearn's predict_proba returns probabilities in class order [prob_class_0, prob_class_1]
            # So prob[0] = P(reject), prob[1] = P(approve)
            if len(prob) == 1:
                # Model only predicts one class (edge case - shouldn't happen with proper training)
                # Check if the single class is approve (1) or reject (0)
                if hasattr(self.model, 'classes_') and len(self.model.classes_) > 0:
                    if self.model.classes_[0] == 1:
                        approval_prob = prob[0]  # Only approve class
                    else:
                        approval_prob = 0.0  # Only reject class
                else:
                    approval_prob = 0.0
            elif len(prob) == 2:
                # Standard binary case: prob[0] = reject, prob[1] = approve
                approval_prob = prob[1]  # Probability of class 1 (approve)
            else:
                # Multi-class case (shouldn't happen, but handle gracefully)
                # Find index of approve class (1) in classes_
                try:
                    if 1 in self.model.classes_:
                        approve_idx = list(self.model.classes_).index(1)
                        approval_prob = prob[approve_idx]
                    else:
                        approval_prob = 0.0
                except (ValueError, IndexError):
                    approval_prob = 0.0
            
            # Convert probability to score (1-10 scale)
            base_score = approval_prob * 9 + 1  # Maps [0,1] to [1,10]
            
            # Apply bias if requested
            if apply_bias:
                # Apply same bias penalties as deterministic model
                region = profile.get("region", "").lower()
                state = profile.get("state", "").lower()
                family_income = profile.get("family_income", 2000000)
                employment_type = profile.get("employment_type", "").lower()
                family_structure = profile.get("family_structure", "").lower()
                college_tier = profile.get("college_tier", "").lower() if profile.get("college_tier") else ""
                
                if "rural" in region:
                    base_score -= 2.0
                if family_income < 2000000:
                    base_score -= 1.0
                if employment_type == "self-employed":
                    base_score -= 1.5
                if "tier2" in region or "tier3" in region:
                    base_score -= 1.0
                if any(s in state for s in ["bihar", "up", "mp"]):
                    base_score -= 0.5
                if "single_parent" in family_structure or "widow" in family_structure:
                    base_score -= 1.0
                # College tier bias: penalize lower-tier colleges
                if college_tier == "tier3" or (not college_tier and not any(x in profile.get("university_name", "").lower() for x in ["iit", "iim", "nit", "bits", "vit"])):
                    base_score -= 1.5
                elif college_tier == "tier2":
                    base_score -= 0.8
                
                base_score = max(1.0, min(10.0, base_score))
            
            # Determine approval decision
            if base_score >= 9.0:
                approval_decision = "approve"
                interest_rate = 9.0
                collateral_required = False
            elif base_score >= 7.0:
                approval_decision = "approve"
                interest_rate = 11.0
                collateral_required = False
            elif base_score >= 5.0:
                approval_decision = "conditional"
                interest_rate = 13.0
                collateral_required = True
            else:
                approval_decision = "reject"
                interest_rate = 15.0
                collateral_required = True
            
            return {
                "score": round(base_score, 2),
                "approval_decision": approval_decision,
                "interest_rate": round(interest_rate, 2),
                "collateral_required": collateral_required,
                "reasoning": f"ML model prediction (probability: {approval_prob:.2%})"
            }
            
        except Exception as e:
            logger.error(f"Error predicting score: {e}", exc_info=True)
            raise
    
    def _save_model(self):
        """Save trained model to disk."""
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "label_encoders": self.label_encoders,
            "feature_names": self.feature_names,
            "model_type": self.model_type
        }
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        with open(self.model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.label_encoders = model_data["label_encoders"]
        self.feature_names = model_data["feature_names"]
        self.model_type = model_data["model_type"]
        self.is_trained = True
        
        logger.info(f"Model loaded from {self.model_path}")


# Global instances for fair and biased models
fair_ml_model = MLScoringModel(model_type="random_forest")
biased_ml_model = MLScoringModel(model_type="random_forest")

