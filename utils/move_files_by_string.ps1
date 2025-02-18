<#

    This script finds all files in the specified directory that contain a given string in their name.
    It then moves them into a folder named after the search string.
    If the folder does not exist, it is created.

    How It Works:

        Ensures a search string is provided.
        Checks if the provided folder exists.
        Gets all files and verifies that every file contains the search string.
        If all files match, it creates a folder with the search string name only if it doesn’t already exist.
        Moves the files into that folder.

        - usage: .\move_files_by_string.ps1 -SearchString "example"
        - usage: .\move_files_by_string.ps1 -SearchString "example" -Path "C:\path\to\your\folder"

#>

# Check if search string is provided
if (-not $SearchString) {
    Write-Host "Error: Please provide a search string."
    Write-Host "SearchString: '$SearchString', Path: '$Path'"
    exit
}

# Check if the directory exists
if (-Not (Test-Path -Path $Path -PathType Container)) {
    Write-Host "Error: The specified path '$Path' does not exist or is not a directory."
    exit
}

# Get all files in the directory that contain the search string (using -like with wildcards)
$matchingFiles = Get-ChildItem -Path $Path -File | Where-Object { $_.Name -like "*$SearchString*" }

if ($matchingFiles.Count -eq 0) {
    Write-Host "No files found containing '$SearchString'."
    exit
}

# Define the new folder path
$NewFolderPath = Join-Path -Path $Path -ChildPath $SearchString

# Create the folder if it does not exist
if (-Not (Test-Path -Path $NewFolderPath)) {
    New-Item -Path $NewFolderPath -ItemType Directory | Out-Null
    Write-Host "Created folder: $NewFolderPath"
} else {
    Write-Host "Folder already exists: $NewFolderPath"
}

# Move matching files into the folder
$matchingFiles | ForEach-Object { Move-Item -Path $_.FullName -Destination $NewFolderPath }

Write-Host "Moved $($matchingFiles.Count) files into '$NewFolderPath'."