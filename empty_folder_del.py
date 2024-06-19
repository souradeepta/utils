import os
import shutil
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FindEmptyFoldersCommand:
    """
    Command to find empty folders.
    """
    def __init__(self, path: str):
        self.path = path

    def execute(self) -> List[str]:
        empty_folders: List[str] = []
        try:
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self._check_empty_folder, root, dir): (root, dir)
                           for root, _, dirs in os.walk(self.path) for dir in dirs}
                for future in as_completed(futures):
                    root, dir = futures[future]
                    try:
                        if future.result():
                            empty_folders.append(os.path.join(root, dir))
                    except Exception as e:
                        logger.error(f"Error checking {os.path.join(root, dir)}: {e}")
        except Exception as e:
            logger.error(f"Error finding empty folders in {self.path}: {e}")
        return empty_folders

    def _check_empty_folder(self, root: str, folder_name: str) -> bool:
        """
        Helper function to check if a folder is empty.
        """
        dir_path = os.path.join(root, folder_name)
        try:
            return not os.listdir(dir_path)
        except PermissionError as e:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logger.error(f"Permission denied: {dir_path}. Error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error accessing {dir_path}: {e}")
        return False

class DeleteFoldersCommand:
    """
    Command to delete folders and save the list with timestamp.
    """
    def __init__(self, folders: List[str], output_file: str):
        self.folders = folders
        self.output_file = output_file

    def execute(self) -> None:
        deleted_folders: List[str] = []
        try:
            with ThreadPoolExecutor() as executor:
                for folder in self.folders:
                    executor.submit(self._delete_folder, folder)
        except Exception as e:
            logger.error(f"Error deleting folders: {e}")

    def _delete_folder(self, folder_path: str) -> None:
        """
        Helper function to delete a folder.
        """
        try:
            shutil.rmtree(folder_path)
            logger.info(f"Deleted: {folder_path}")
        except PermissionError as e:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logger.error(f"Permission denied: {folder_path}. Error: {e}")
        except FileNotFoundError as e:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logger.error(f"Folder not found: {folder_path}. Error: {e}")
        except Exception as e:
            logger.error(f"Error deleting {folder_path}: {e}")

class FolderProcessor:
    """
    Class to manage folder operations.
    """
    def __init__(self, path: str, output_file: str):
        self.path = path
        self.output_file = output_file

    def find_empty_folders(self) -> List[str]:
        """
        Find empty folders in the specified path using multithreading.
        """
        command = FindEmptyFoldersCommand(self.path)
        return command.execute()

    def delete_folders(self, folders: List[str]) -> None:
        """
        Delete specified folders and save the list with timestamp.
        """
        command = DeleteFoldersCommand(folders, self.output_file)
        command.execute()

    def save_deleted_folders(self, deleted_folders: List[str]) -> None:
        """
        Save the list of deleted folders with a timestamp.
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename, extension = os.path.splitext(self.output_file)
            timestamped_output_file = f"{filename}_{timestamp}{extension}"

            with open(timestamped_output_file, 'w') as f:
                f.write(f"Deleted folders on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")
                f.write("\n".join(deleted_folders))
            logger.info(f"Deleted folders list saved to: {timestamped_output_file}")
        except Exception as e:
            logger.error(f"Error saving deleted folders: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Find and list empty folders.")
    parser.add_argument("path", help="Directory path to search for empty folders.")
    parser.add_argument("-o", "--output", default="output/deleted_folders.txt", help="Output file path for deleted folders.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    # Configure logging based on debug mode
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    path = args.path
    output_file = args.output

    if not os.path.exists(path):
        logger.error(f"The specified path does not exist: {path}")
        return

    folder_processor = FolderProcessor(path, output_file)
    empty_folders = folder_processor.find_empty_folders()

    if empty_folders:
        logger.info("Empty folders found:")
        for folder in empty_folders:
            logger.info(folder)

        confirm = input("Do you want to delete these folders? (yes/no): ")
        if confirm.lower() == 'yes':
            folder_processor.delete_folders(empty_folders)
            folder_processor.save_deleted_folders(empty_folders)
        else:
            logger.info("Deletion aborted.")
    else:
        logger.info("No empty folders found.")

if __name__ == "__main__":
    main()
