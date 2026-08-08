"""
Reusable visualizations for exploratory data analysis.
"""

import matplotlib.pyplot as plt
import pandas as pd

from src.dataset.builder import FEATURE_COLUMNS, LABEL_COLUMN


def plot_class_balance(dataset: pd.DataFrame) -> None:
    """
    Plot the distribution of the binary target variable.
    """
    counts = dataset[LABEL_COLUMN].value_counts().sort_index()

    counts.plot(kind="bar")

    plt.title("Class Balance")
    plt.xlabel("Outperformed QQQ")
    plt.ylabel("Observations")
    plt.tight_layout()
    plt.show()


def plot_feature_distributions(dataset: pd.DataFrame) -> None:
    """
    Plot a histogram for each model feature.
    """
    for feature in FEATURE_COLUMNS:
        dataset[feature].hist(bins=30)

        plt.title(f"Distribution of {feature}")
        plt.xlabel(feature)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def plot_feature_correlations(dataset: pd.DataFrame) -> None:
    """
    Plot correlations between model features and the target.
    """
    columns = FEATURE_COLUMNS + [LABEL_COLUMN]

    correlations = dataset[columns].corr()

    figure, axis = plt.subplots()

    image = axis.imshow(correlations)

    axis.set_xticks(range(len(columns)))
    axis.set_yticks(range(len(columns)))

    axis.set_xticklabels(columns, rotation=90)
    axis.set_yticklabels(columns)

    figure.colorbar(image)

    axis.set_title("Feature Correlations")

    plt.tight_layout()
    plt.show()