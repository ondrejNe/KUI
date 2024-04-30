from classificator_base import ClassificatorBase


class NaiveBayes(ClassificatorBase):
    def __init__(self):
        super().__init__()
        # 1 Argument parsing
        self.args = self.parser.parse_args()

    def classificator_train(self, train_data):
        # Implement KNN training here
        pass

    def classificator_test(self, test_data):
        # Implement KNN testing here
        return []


if __name__ == "__main__":
    knn_classifier = NaiveBayes()
    knn_classifier.run()
