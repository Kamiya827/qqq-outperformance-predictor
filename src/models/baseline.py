"""
Baseline machine learning models.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier


def build_logistic_regression() -> LogisticRegression:
    """
    Create a baseline Logistic Regression classifier.
    """
    return LogisticRegression(
        max_iter=1000,
        random_state=42,
    )

def build_decision_tree() -> DecisionTreeClassifier:
    """
    Create a baseline Decision Tree classifier.
    """
    return DecisionTreeClassifier(
        random_state=42,
    )

def build_random_forest() -> RandomForestClassifier:
    """
    Create a baseline Random Forest classifier.
    """
    return RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )

def build_gradient_boosting() -> GradientBoostingClassifier:
    """
    Create a baseline Gradient Boosting classifier.
    """
    return GradientBoostingClassifier(
        random_state=42,
    )