from classificator_base import ClassificatorBase


class KNN(ClassificatorBase):
    def __init__(self):
        super().__init__()
        # 1 Argument parsing
        self.parser.add_argument('-k', type=int,
                                 required=True,
                                 help='number of neighbours (if k is 0 the code may decide about proper K by itself)')
        self.args = self.parser.parse_args()

    def classificator_train(self, train_data):
        # Implement KNN training here
        pass

    def classificator_test(self, test_data):
        # Implement KNN testing here
        return []


if __name__ == "__main__":
    knn_classifier = KNN()
    knn_classifier.run()
