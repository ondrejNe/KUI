import argparse
import os
from abc import ABC, abstractmethod


class ClassificatorBase(ABC):  # Abstract Base Class
    def __init__(self):
        # 1 Argument parsing
        self.args = None
        self.parser = argparse.ArgumentParser(description="Learn and classify image data.")
        self.parser.add_argument('train_path', type=str, help='path to the training data directory')
        self.parser.add_argument('test_path', type=str, help='path to the testing data directory')
        self.parser.add_argument('-o', '--output', type=str,
                                 help='path (including the filename) of the output .dsv file with the results',
                                 default='classification.dsv')

    @abstractmethod
    def classificator_train(self, train_data):
        """Train the classifier using the provided training data."""
        pass

    @abstractmethod
    def classificator_test(self, test_data):
        """Test the classifier using the provided test data."""
        pass

    def load_data(self, directory):
        """Load data from a directory (stub, to be customized or overridden as necessary)."""
        data = []
        # Example: Load data from .png files as numerical vectors using numpy
        # This is a placeholder; specific loading logic will depend on the data format and requirements
        return data

    def run(self):
        """Main method to run the training and testing of the classifier."""
        train_data = self.load_data(self.args.train_path)
        test_data = self.load_data(self.args.test_path)
        self.classificator_train(train_data)
        results = self.classificator_test(test_data)
        if self.args.output:
            self.save_results(results, self.args.output)

    def save_results(self, results, filepath):
        """Save the classification results to a .dsv file."""
        with open(filepath, 'w') as file:
            for result in results:
                file.write(f"{result}\n")
