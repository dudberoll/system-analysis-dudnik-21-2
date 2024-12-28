import pandas as pd
import numpy as np
from typing import List


def load_csv(file_path: str) -> pd.DataFrame:
    """Loads data from a CSV file."""
    return pd.read_csv(file_path)


def compute_joint_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates joint probabilities from the DataFrame."""
    total = df.iloc[:, 1:].values.sum()
    return df.iloc[:, 1:] / total


def compute_marginal_probabilities(joint_probs: pd.DataFrame) -> (np.ndarray, np.ndarray):
    """Calculates marginal probabilities for variables A and B."""
    marginal_A = joint_probs.sum(axis=1).values
    marginal_B = joint_probs.sum(axis=0).values
    return marginal_A, marginal_B


def calculate_entropy(probs: np.ndarray) -> float:
    """Calculates entropy for a given set of probabilities."""
    return -np.sum(probs * np.log2(probs, where=(probs > 0)))


def compute_conditional_entropy(joint_probs: pd.DataFrame, marginal_A: np.ndarray) -> float:
    """Calculates the conditional entropy of B given A."""
    conditional_entropy = np.sum([
        p_a * calculate_entropy(joint_probs.iloc[idx, :].values / p_a)
        for idx, p_a in enumerate(marginal_A) if p_a > 0
    ])
    return conditional_entropy


def main() -> List[float]:
    # Load data from the CSV file
    data = load_csv('example.csv')

    # Compute joint and marginal probabilities
    joint_probabilities = compute_joint_probabilities(data)
    marginal_A, marginal_B = compute_marginal_probabilities(joint_probabilities)

    # Calculate entropies
    entropy_joint = calculate_entropy(joint_probabilities.values.flatten())
    entropy_A = calculate_entropy(marginal_A)
    entropy_B = calculate_entropy(marginal_B)

    # Calculate conditional entropy and mutual information
    conditional_entropy = compute_conditional_entropy(joint_probabilities, marginal_A)
    mutual_information = entropy_B - conditional_entropy

    # Return results rounded to two decimal places
    return [
        round(entropy_joint, 2),
        round(entropy_A, 2),
        round(entropy_B, 2),
        round(conditional_entropy, 2),
        round(mutual_information, 2)
    ]


if __name__ == "__main__":
    result = main()
    print(result)
