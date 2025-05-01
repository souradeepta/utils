import os
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
Below is a Python script that performs a light overview of the folder structure of your hard drive (or a specified root directory). It:

    Recursively traverses directories starting from a root path.

    Logs only directory names (and optionally top-level file names).

    Limits recursion depth to avoid excessively deep scans.

    Writes the result to a neatly formatted text file.

✅ Features:

    Traverses using os.walk() for efficiency.

    Allows user to set max depth.

    Cleanly indents subdirectories.

    Outputs results to a user-defined .txt file.

    Example usage:
    > python folder_summary.py "C:\\" -d 2 -o c_drive_overview.txt
    > python folder_summary.py /home/user -d 3 -o home_structure.txt
    > python folder_summary.py /mnt/bigdata -d 4 -o output.txt --max-chars 10000
    > python folder_summary.py /mnt/bigdata -d 4 -o output.txt --max-lines 500
    > python folder_summary.py /mnt/data -d 3 -o summary.txt --max-chars 10000 --compact




"""

def get_dir_size_fast(path):
    """ Fast directory size calculation using os.scandir and avoiding recursion """
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_dir_size_fast(entry.path)
            except Exception:
                continue
    except Exception:
        return 0
    return total

def scan_directory(path, depth, max_depth, output, lock, collect_file_details=False):
    """ Recursive scan with depth control """
    if depth > max_depth:
        return

    indent = "    " * depth
    folder_name = os.path.basename(path) or path

    try:
        size_mb = get_dir_size_fast(path) / (1024 * 1024)
    except Exception:
        size_mb = 0

    with lock:
        output.append(f"{indent}[DIR] {folder_name} - {size_mb:.2f} MB\n")

    file_types = Counter()

    try:
        entries = list(os.scandir(path))
    except Exception:
        return

    for entry in entries:
        if entry.is_file(follow_symlinks=False):
            try:
                if collect_file_details:
                    size_kb = entry.stat().st_size / 1024
                    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.stat().st_mtime))
                    ext = os.path.splitext(entry.name)[1].lower()
                    file_types[ext] += 1
                    with lock:
                        output.append(f"{indent}    [FILE] {entry.name} ({size_kb:.1f} KB, modified {mtime})\n")
                else:
                    ext = os.path.splitext(entry.name)[1].lower()
                    file_types[ext] += 1
            except Exception:
                continue

    if file_types:
        with lock:
            output.append(f"{indent}    File types: {dict(file_types)}\n\n")

    # Recursively scan subdirectories
    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                futures.append(
                    executor.submit(scan_directory, entry.path, depth + 1, max_depth, output, lock, collect_file_details)
                )
        for future in as_completed(futures):
            future.result()

def list_directory_structure_parallel(root_path: str, max_depth: int = 3, output_file: str = "folder_structure.txt",
                                      collect_file_details=False, max_lines=None, max_chars=None,
                                      readable=True):
    from threading import Lock
    output = []
    lock = Lock()
    scan_directory(root_path, 0, max_depth, output, lock, collect_file_details)

    final_output = []
    total_chars = 0
    total_lines = 0

    for line in output:
        out_line = line if readable else line.strip().replace("\n", "").replace("    ", "")
        new_char_count = len(out_line) + (1 if readable else 0)  # +1 for newline if kept

        if (max_lines is not None and total_lines >= max_lines) or \
           (max_chars is not None and total_chars + new_char_count > max_chars):
            break

        final_output.append(out_line + ("\n" if readable else " "))
        total_chars += new_char_count
        total_lines += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(final_output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a fast overview of a folder structure.")
    parser.add_argument("path", help="Root directory to scan (e.g., C:\\, /home/user/)")
    parser.add_argument("-d", "--depth", type=int, default=3, help="Maximum folder depth to scan")
    parser.add_argument("-o", "--output", default="folder_structure.txt", help="Output text file path")
    parser.add_argument("--details", action="store_true", help="Collect detailed file info (slower)")
    parser.add_argument("--max-lines", type=int, help="Maximum number of lines to write to output")
    parser.add_argument("--max-chars", type=int, help="Maximum number of characters to write to output")
    parser.add_argument("--readable", dest="readable", action="store_true", help="Preserve indentation and line breaks (default)")
    parser.add_argument("--compact", dest="readable", action="store_false", help="Remove all extra spaces and line breaks")



    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path '{args.path}' does not exist.")
    else:
        start_time = time.time()
        list_directory_structure_parallel(
            args.path,
            max_depth=args.depth,
            output_file=args.output,
            collect_file_details=args.details,
            max_lines=args.max_lines,
            max_chars=args.max_chars,
            readable=args.readable
        )

        elapsed = time.time() - start_time
        print(f"Folder structure written to: {args.output}")
        print(f"Scan completed in {elapsed:.2f} seconds.")
