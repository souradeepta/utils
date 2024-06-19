import os
import sys
from typing import Callable, Union

# List of common file extensions for reference
COMMON_EXTENSIONS = ['.mkv', '.txt', '.jpg', '.png', '.pdf', '.doc', '.docx', '.xls', '.xlsx',
                     '.mp3', '.mp4', '.avi', '.ppt', '.pptx', '.msi', '.exe', '.zip', '.jpeg',
                     '.part', '.py', '.java', '.gif', '.bmp', '.tif', '.tiff', '.wav', '.mov',
                     '.rar', '.tar', '.gz', '.iso', '.html', '.css', '.js', '.json', '.xml',
                     '.sql', '.csv', '.log', '.svg', '.ico', '.ini', '.cfg', '.md', '.bat',
                     '.dll', '.class', '.jar', '.rpm', '.deb', '.sh', '.bin', '.key', '.pem']

# Target extension to append if a file has no known extension
TARGET_EXTENSION = ".mp4"


class ExtensionStrategy:
    """
    Abstract base class for extension handling strategies.
    """

    def __init__(self, target_extension: str):
        self.target_extension = target_extension

    def handle_file(self, file_path: str) -> None:
        """
        Handle the file based on the strategy.

        Args:
            file_path (str): Full path to the file.
        """
        raise NotImplementedError("Subclasses should implement this method")


class KnownExtensionStrategy(ExtensionStrategy):
    """
    Strategy for handling files with known extensions.
    """

    def handle_file(self, file_path: str) -> None:
        """
        Handle the file with a known extension.

        Args:
            file_path (str): Full path to the file.
        """
        print(f"{file_path} has a known extension: {os.path.splitext(file_path)[1]}")


class UnknownExtensionStrategy(ExtensionStrategy):
    """
    Strategy for handling files with unknown extensions.
    """

    def handle_file(self, file_path: str) -> None:
        """
        Handle the file with an unknown extension by appending `target_extension`.

        Args:
            file_path (str): Full path to the file.
        """
        new_file_path = f"{file_path}{self.target_extension}"
        try:
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} -> {new_file_path}")
        except OSError as e:
            print(f"Failed to rename {file_path} to {new_file_path}: {e}")


def has_known_extension(filename: str) -> bool:
    """
    Check if the filename has a known extension.

    Args:
        filename (str): Name of the file.

    Returns:
        bool: True if the extension is in COMMON_EXTENSIONS, False otherwise.
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() in COMMON_EXTENSIONS


def append_extension_to_files(directory_path: str, strategy: ExtensionStrategy) -> None:
    """
    Append `TARGET_EXTENSION` to files in `directory_path` based on `strategy`.

    Args:
        directory_path (str): Path to the directory containing files.
        strategy (ExtensionStrategy): Strategy object defining how to handle files.
    """
    try:
        # Check if the provided path is a valid directory
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"The path {directory_path} is not a valid directory.")

        # Iterate over the files in the directory
        for filename in os.listdir(directory_path):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)

            # Debug: Print the current file being checked
            print(f"Checking file: {file_path}")

            # Check if it's a file
            if os.path.isfile(file_path):
                if not has_known_extension(filename):
                    strategy.handle_file(file_path)
                else:
                    strategy.handle_file(file_path)
            else:
                # Debug: Print if it's not a file (e.g., directory)
                print(f"  {file_path} is not a file")

    except NotADirectoryError as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Check if the directory path is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python extension_util.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    # Choose strategy based on conditions
    if not has_known_extension(directory_path):
        strategy = KnownExtensionStrategy(TARGET_EXTENSION)
    else:
        strategy = UnknownExtensionStrategy(TARGET_EXTENSION)

    append_extension_to_files(directory_path, strategy)
