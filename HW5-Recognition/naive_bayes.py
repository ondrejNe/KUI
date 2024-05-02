import numpy as np

from classificator_base import ClassificatorBase


class NaiveBayes(ClassificatorBase):
    """Naive Bayes classifier."""

    def __init__(self):
        super().__init__()
        # 1 Argument parsing
        self.args = self.parser.parse_args()

        # 2 Train data loading
        self.train_labels = self.load_train_labels(
            folder=self.args.train_path,
            filename='truth.dsv'
        )
        self.train_labels_set = sorted(set(self.train_labels.values()))
        self.train_index_by_label = {label: index for index, label in enumerate(self.train_labels_set)}
        self.train_label_by_index = {index: label for label, index in self.train_index_by_label.items()}

        # Feature extractions
        self.tone_reduction = 32
        self.train_images = self.load_train_images(
            folder=self.args.train_path,
            filenames=list(self.train_labels.keys())
        )
        for filename, feature_vector in self.train_images.items():
            self.train_images[filename] = feature_vector // self.tone_reduction * self.tone_reduction

        # 3 Train the classifier
        self.log_probabilities = None
        self.log_label_probabilities = {}
        self.classificator_train()

        # 4 Test data loading
        # Feature extractions
        self.test_images = self.load_test_images(
            folder=self.args.test_path,
            exclude=['truth.dsv']
        )
        for filename, feature_vector in self.test_images.items():
            self.test_images[filename] = feature_vector // self.tone_reduction * self.tone_reduction

        # 5 Test the classifier
        self.results = {}
        self.classificator_test()

        # 6 Save the results
        self.save_test_results(
            filepath=self.args.output,
            results=self.results
        )

    def classificator_train(self) -> None:
        with self.timer("Training"):
            # Space size resolution
            train_set_size = len(self.train_labels.keys())
            label_space_size = len(self.train_labels_set)
            feature_vector_size = len(next(iter(self.train_images.items()))[1])

            # Initialize counts
            label_occurrence = {label_index: 0 for label_index in self.train_label_by_index.keys()}
            for label in self.train_labels.values():
                label_index = self.train_index_by_label[label]
                label_occurrence[label_index] += 1

            # Initialize probability counts
            probabilities = np.zeros([label_space_size, feature_vector_size, 256 // self.tone_reduction])
            for filename, feature_vector in self.train_images.items():
                label = self.train_labels[filename]
                label_index = self.train_index_by_label[label]
                for pixel_index, tone_index in enumerate(feature_vector):
                    probabilities[label_index, pixel_index, tone_index // self.tone_reduction] += 1

            # Laplace smoothing
            k = 3
            probabilities += k

            # Calculate the probabilities with laplace
            for (label_index, pixel_index, tone_index), value in np.ndenumerate(probabilities):
                probabilities[label_index, pixel_index, tone_index] = (
                    np.log(
                        probabilities[label_index, pixel_index, tone_index] / (label_occurrence[label_index] + (256 // self.tone_reduction)*k)
                    )
                )

            self.log_probabilities = probabilities

            # Calculate the apriori label probabilities
            self.log_label_probabilities = {
                label_index: np.log(
                    occurrence / train_set_size
                ) for label_index, occurrence in label_occurrence.items()
            }

    def classificator_test(self) -> None:
        with self.timer("Testing"):
            for filename, feature in self.test_images.items():
                self.results[filename] = self.classificator_test_single_image(feature)

    def classificator_test_single_image(self, feature: np.array) -> str:
        label_probability = []
        for label, label_index in self.train_index_by_label.items():
            # Compute the sum of log probabilities for the current label.
            label_apriori = self.log_label_probabilities[label_index]
            label_tone_p = sum(
                self.log_probabilities[label_index, pixel_index, tone_index // self.tone_reduction]
                for pixel_index, tone_index in enumerate(feature)
            )
            label_probability.append((label, label_apriori + label_tone_p))
        return sorted(label_probability, key=lambda x: x[1], reverse=True)[0][0]


if __name__ == "__main__":
    NaiveBayes()
