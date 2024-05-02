import numpy as np

from classificator_base import ClassificatorBase


class KNN(ClassificatorBase):
    """K-Nearest Neighbours classifier."""

    def __init__(self):
        super().__init__()
        # 1 Argument parsing with additional parameter
        self.parser.add_argument(
            '-k',
            type=int,
            required=True,
            help='number of neighbours (if k is 0 the code may decide about proper K by itself)'
        )
        self.args = self.parser.parse_args()

        # 2 Train data loading
        self.train_labels = self.load_train_labels(
            folder=self.args.train_path,
            filename='truth.dsv'
        )
        # Feature extractions
        self.train_images = self.load_train_images(
            folder=self.args.train_path,
            filenames=list(self.train_labels.keys())
        )

        # 3 Train the classifier (Determine optimal K)
        self.classificator_train()

        # 4 Test data loading
        self.test_images = self.load_test_images(
            folder=self.args.test_path,
            exclude=['truth.dsv']
        )

        # 5 Test the classifier
        self.results = {}
        self.classificator_test()

        # 6 Save the results
        self.save_test_results(
            filepath=self.args.output,
            results=self.results
        )

    @staticmethod
    def euclidean_distance(x, y) -> float:
        """Distance metric for KNN."""
        return np.linalg.norm(x - y)

    @staticmethod
    def cosine_distance(x, y) -> float:
        """Distance metric for KNN."""
        dot_product = np.dot(x, y)
        norm_x = np.linalg.norm(x)
        norm_y = np.linalg.norm(y)
        if norm_x == 0 or norm_y == 0:
            # Handle the case where one or both vectors are zero vectors.
            return 0
        similarity = dot_product / (norm_x * norm_y)
        return 1 - similarity

    @staticmethod
    def distance(x, y) -> float:
        # return KNN.cosine_distance(x, y)
        return KNN.euclidean_distance(x, y)

    def classificator_train(self) -> None:
        if self.args.k != 0:
            return

        # Determine the number of neighbours through cross validation
        with self.timer("Cross validation"):
            self.args.k = self.classificator_cross_validation()

    def classificator_cross_validation(self, num_folds=10, max_k=10) -> int:
        print(f'Performing cross validation with {num_folds} folds and k up to {max_k}')

        # Predict the label of a test feature helper function
        def predict_label(train_fs, train_ls, test_f, test_k):
            distances = [self.distance(test_f, f) for f in train_fs]
            nearest_indices = np.argsort(distances)[:test_k]
            nearest_labels = [train_ls[i] for i in nearest_indices]
            most_common_label = max(set(nearest_labels), key=nearest_labels.count)
            return most_common_label

        # Get ordered lists of the training data
        ordered_train_labels = []
        ordered_train_features = []
        for filename, feature in self.train_images.items():
            ordered_train_labels.append(self.train_labels[filename])
            ordered_train_features.append(feature)

        # Split the data set into training and validation sets
        fold_size = len(ordered_train_labels) // num_folds
        k_accuracies = []

        # Determine the optimal k through the mean of 1..num_folds results
        for k in range(1, max_k + 1):
            with self.timer(f"Cross validation for k={k} folds=1..{num_folds}"):
                accuracies = []

                for fold in range(num_folds):
                    start, end = fold * fold_size, (fold + 1) * fold_size

                    # Select the validation set
                    val_labels = ordered_train_labels[start:end]
                    val_features = ordered_train_features[start:end]

                    # Select the training set
                    train_labels = ordered_train_labels[:start] + ordered_train_labels[end:]
                    train_features = ordered_train_features[:start] + ordered_train_features[end:]

                    # Test the classifier for 'k' neighbours
                    correct_count = 0
                    for j, val_feature in enumerate(val_features):
                        predicted_label = predict_label(train_features, train_labels, val_feature, k)
                        if predicted_label == val_labels[j]:
                            correct_count += 1

                    accuracy = correct_count / len(val_features)
                    # print(f'k={k}, fold={fold}, accuracy={accuracy}')
                    accuracies.append(accuracy)

                k_accuracies.append(np.mean(accuracies))

        # Return the most accurate k
        print(f'K Accuracies={[f"k={i + 1}: {x:.2f}%" for i, x in enumerate(k_accuracies)]}')
        best_k = np.argmax(k_accuracies) + 1
        return best_k

    def classificator_test(self) -> None:
        with self.timer("Testing"):
            for test_image, test_feature in self.test_images.items():
                # Find the nearest neighbours
                neighbours = []
                for train_image, train_feature in self.train_images.items():
                    distance = self.distance(test_feature, train_feature)
                    neighbours.append((distance, train_image))
                neighbours.sort(key=lambda x: x[0])  # Sort by the closest distance

                # Get the most common label
                k = self.args.k
                labels = {}
                for i in range(k):
                    label = self.train_labels[neighbours[i][1]]
                    if label in labels:
                        labels[label] += 1
                    else:
                        labels[label] = 1
                result = max(labels, key=labels.get)
                self.results[test_image] = result


if __name__ == "__main__":
    KNN()
