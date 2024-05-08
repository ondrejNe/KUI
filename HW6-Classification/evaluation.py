import pandas as pd
import numpy as np


def is_new_classifier_better(file_path: str, ground_truth_path='GT.dsv', reference_fpr=0.0, reference_tpr=0.46):
    """
    Evaluate if the new classifier is better than the existing one based on a reference metric.

    Args:
    - file_path (str): Path to the classifier results file, e.g., 'C6.dsv'.
    - ground_truth_path (str): Path to the ground truth data.
    - reference_fpr (float): Reference false positive rate.
    - reference_tpr (float): Reference true positive rate.

    Returns:
    - bool: True if the new classifier is better, False otherwise.
    """
    # Load classifier results and ground truth data
    classifier_outputs = pd.read_csv(file_path, delimiter=',', header=None)
    ground_truth = pd.read_csv(ground_truth_path, delimiter=',', header=None).to_numpy().flatten()

    # Prepare to calculate metrics
    tpr_list = []  # True positive rate list
    fpr_list = []  # False positive rate list

    # Calculate metrics for each alpha
    for i in range(classifier_outputs.shape[1]):
        predictions = classifier_outputs[i]
        TP = np.sum((predictions == 1) & (ground_truth == 1))
        FP = np.sum((predictions == 1) & (ground_truth == 0))
        TN = np.sum((predictions == 0) & (ground_truth == 0))
        FN = np.sum((predictions == 0) & (ground_truth == 1))

        TPR = TP / (TP + FN) if TP + FN != 0 else 0
        FPR = FP / (FP + TN) if FP + TN != 0 else 0

        tpr_list.append(TPR)
        fpr_list.append(FPR)

    # Check if there is at least one alpha where FPR is lower than the reference and TPR is higher than the reference
    better_classifier_exists = any(
        fpr <= reference_fpr and tpr > reference_tpr for fpr, tpr in zip(fpr_list, tpr_list)
    )

    return better_classifier_exists

# Example usage
# result = is_new_classifier_better('path_to_C6.dsv', 'GT.dsv', reference_fpr=0.1, reference_tpr=0.46)
# print(f'Is the new classifier better? {result}')
