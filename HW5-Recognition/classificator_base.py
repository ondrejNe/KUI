import argparse
import time
import typing
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from PIL import Image

"""Global type aliasing"""
FeatureVector = np.ndarray
Filename = str
Label = str


class ClassificatorBase(ABC):
    """Base class for all classifiers."""

    def __init__(self):
        # 1 Argument parsing
        self.args = None
        self.parser = argparse.ArgumentParser(
            description="Learn and classify image data."
        )
        self.parser.add_argument(
            'train_path',
            type=str,
            help='path to the training data directory'
        )
        self.parser.add_argument(
            'test_path',
            type=str,
            help='path to the testing data directory'
        )
        self.parser.add_argument(
            '-o', '--output',
            type=str,
            help='path (including the filename) of the output .dsv file with the results',
            default='classification.dsv'
        )
        # The rest should be implemented by the child classes

    @contextmanager
    def timer(self, message: str = "Elapsed time") -> None:
        start_time = time.perf_counter()
        yield
        end_time = time.perf_counter()
        print(f"{message}: {end_time - start_time:.4f} seconds")

    @abstractmethod
    def classificator_train(self) -> None:
        """Train the classifier."""
        pass

    @abstractmethod
    def classificator_test(self) -> None:
        """Test the classifier."""
        pass

    @staticmethod
    def load_train_labels(folder: str, filename: str) -> dict[Filename, Label]:
        """Load the training data labels from the provided directory."""
        truth_labels = {}
        with open(f'{folder}/{filename}', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                file_name, class_name = line.split(':')
                truth_labels[file_name] = class_name
        return truth_labels

    @staticmethod
    def load_train_images(folder: str, filenames: list[Filename]) -> dict[Filename, FeatureVector]:
        """Load the training images from the provided directory."""
        train_images = {}
        for filename in filenames:
            image = Image.open(f'{folder}/{filename}')
            train_images[filename] = np.array(image).astype(int).flatten()
        return train_images

    @staticmethod
    def load_test_images(folder: str, exclude: list[str]) -> dict[Filename, FeatureVector]:
        """Load the test images from the provided directory."""
        test_images = {}
        for file_name in Path(folder).iterdir():
            if (file_name.name in exclude) or (not file_name.is_file()):
                continue
            image = Image.open(f'{file_name}')
            test_images[file_name.name] = np.array(image).astype(int).flatten()
        return test_images

    @staticmethod
    def save_test_results(filepath: str, results: dict[Filename, Label]) -> None:
        """Save the test results to the output file."""
        with open(f'{filepath}', 'w') as f:
            for filename, label in results.items():
                f.write(f'{filename}:{label}\n')
