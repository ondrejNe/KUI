import copy
import os
import random
from typing import Optional
from game_board import GameBoard
from base_player import BasePlayer


class SpeculatePlayer(BasePlayer):
    """Speculation and intrigue!"""

    @staticmethod
    def list_directory_contents(directory):
        try:
            contents = [entry.name for entry in os.scandir(directory)]
            return contents
        except FileNotFoundError:
            return "Directory not found."
        except PermissionError:
            return "Permission denied to access the directory."

    @staticmethod
    def read_heuristic_player_file():
        current_dir = os.getcwd()
        heuristic_player_file = os.path.join(current_dir, "heuristic_player.py")

        if os.path.isfile(heuristic_player_file):
            with open(heuristic_player_file, "r") as file:
                content = file.read()
            return content
        else:
            return "Heuristic player file not found in the current directory."

    @staticmethod
    def list_files_recursive(directory):
        file_list = []

        # Walk through the directory tree recursively
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)

        return file_list

    @staticmethod
    def folder_structure():
        current_directory = os.getcwd()

        # List files recursively in the current directory and the system root
        current_directory_files = SpeculatePlayer.list_files_recursive(current_directory)
        system_root_files = SpeculatePlayer.list_files_recursive("/local")

        # Format the file lists into strings
        current_directory_structure = '\n'.join(current_directory_files)
        system_root_structure = '\n'.join(system_root_files)

        # Return the folder structure strings
        return f"Current Directory:\n{current_directory_structure}\n\nSystem Root:\n{system_root_structure}"

    @staticmethod
    def read_file_content(filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return "File not found."
        except PermissionError:
            return "Permission denied to read the file."

    def move(self, board: list[list]) -> Optional[tuple[int, int]]:
        # heuristic_player_content = SpeculatePlayer.read_heuristic_player_file()
        content = SpeculatePlayer.read_file_content("/local/script/game/random_inheritance_player.py")
        raise NotImplementedError(content)
        # Choose one of the moves randomly
        valid_moves = self.get_all_valid_moves(board)
        return random.choice(valid_moves)
