# Define the path to the log file
$logFile = "..\output\ip_tracker.txt"

## Get the current public IP address
$currentIP = (Invoke-WebRequest -uri "http://ifconfig.me").Content.Trim()

# Check if the log file exists
if (Test-Path $logFile) {
    # Get the last logged entry
    $lastLoggedEntry = Get-Content $logFile | Select-Object -Last 1
    # Extract the IP address from the last logged entry
    $lastLoggedIP = $lastLoggedEntry -replace ".*IP: ", "" -replace " -.*", ""

    # Check if the current IP is different from the last logged IP
    if ($currentIP -ne $lastLoggedIP) {
        # Get the current timestamp
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

        # Get the hostname
        $hostname = $env:COMPUTERNAME

        # Get the operating system version
        $osVersion = (Get-WmiObject -Class Win32_OperatingSystem).Version

        # Get the network adapter information
        $networkAdapters = Get-NetAdapter | Select-Object -Property Name, Status, MACAddress, LinkSpeed

        # Format the log entry with the timestamp, IP address, hostname, OS version, and network adapter details
        $logEntry = "$timestamp - IP: $currentIP - Hostname: $hostname - OS Version: $osVersion"

        # Append network adapter details to the log entry
        foreach ($adapter in $networkAdapters) {
            $logEntry += " - Adapter: $($adapter.Name), Status: $($adapter.Status), MAC: $($adapter.MACAddress), Speed: $($adapter.LinkSpeed)"
        }

        # Append the log entry to the log file
        Add-Content -Path $logFile -Value $logEntry
    }
} else {
    # Create the log file and add the first log entry
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $hostname = $env:COMPUTERNAME
    $osVersion = (Get-WmiObject -Class Win32_OperatingSystem).Version
    $networkAdapters = Get-NetAdapter | Select-Object -Property Name, Status, MACAddress, LinkSpeed
    $logEntry = "$timestamp - IP: $currentIP - Hostname: $hostname - OS Version: $osVersion"

    foreach ($adapter in $networkAdapters) {
        $logEntry += " - Adapter: $($adapter.Name), Status: $($adapter.Status), MAC: $($adapter.MACAddress), Speed: $($adapter.LinkSpeed)"
    }

    $logEntry | Out-File $logFile
}