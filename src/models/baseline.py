"""
Baseline machine learning models.
"""

from sklearn.linear_model import LogisticRegression


def build_logistic_regression() -> LogisticRegression:
    """
    Create a baseline Logistic Regression classifier.
    """
    return LogisticRegression(
        max_iter=1000,
        random_state=42,
    )