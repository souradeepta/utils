<#
How It Works:

    If no path is provided, it defaults to the current directory.
    It asks for confirmation (Y/N) before renaming files.
    It checks if the directory exists before proceeding.
    Renames all files in the directory by appending .mp4.

    - usage: .\rename_to_mp4.ps1
    - usage: .\rename_to_mp4.ps1 -Path "C:\path\to\your\folder"

#>

param (
    [string]$Path = $PWD
)

# Confirm with the user before proceeding
$confirmation = Read-Host "Are you sure you want to rename all files in '$Path' to append .mp4? (Y/N)"
if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Host "Operation canceled."
    exit
}

# Check if the directory exists
if (-Not (Test-Path -Path $Path -PathType Container)) {
    Write-Host "Error: The specified path '$Path' does not exist or is not a directory."
    exit
}

# Rename all files
Get-ChildItem -Path $Path -File | Rename-Item -NewName { $_.Name + ".mp4" }

Write-Host "Renaming completed successfully!"

