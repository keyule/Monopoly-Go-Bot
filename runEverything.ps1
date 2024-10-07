param(
    [Alias("v")]
    [int[]]$vLevels = @(0, 1),  # Default is both levels 0 and 1, but you can specify others like 2, 3, etc.
    [Alias("u")]
    [int]$startUserId = $null   # Default is null, meaning process all users
)

# Mapping from verbosity levels to ports
$verbosityPortMap = @{
    0 = 16384
    1 = 16416
    # Add more mappings if needed
}

# Function to run the emulator and bot for a given verbosity level
function Run-EmulatorAndBot {
    param(
        [int]$vLevel,
        [int]$startUserId
    )
    
    # Get the corresponding port for the verbosity level
    if ($verbosityPortMap.ContainsKey($vLevel)) {
        $port = $verbosityPortMap[$vLevel]
    } else {
        Write-Host "No port mapping found for verbosity level $vLevel. Using default port 7555."
        $port = 7555  # Default port
    }
    
    # Start MuMuPlayer Emulator with the specified -v level
    Write-Host "Starting MuMuPlayer Emulator with -v $vLevel..."
    $Process = Start-Process "C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuPlayer.exe" -ArgumentList '-v', "$vLevel" -PassThru

    # Wait for the emulator to launch with a countdown
    Write-Host "Waiting for emulator to launch..."
    For ($i = 30; $i -gt 0; $i--) {
        Write-Host "$i seconds remaining..."
        Start-Sleep -Seconds 1
    }

    # Connect ADB using the specified port
    Write-Host "Connecting ADB to the emulator on port $port..."
    adb connect localhost:$port

    # Get all users
    Write-Host "Retrieving all users..."
    $usersOutput = adb -s localhost:$port shell pm list users

    # Extract user IDs from the output
    Write-Host "Extracting user IDs..."
    $pattern = 'UserInfo{(\d+):'
    $userIds = @()
    foreach ($line in $usersOutput) {
        if ($line -match $pattern) {
            $userIds += $Matches[1]
        }
    }

    # Display all user IDs
    Write-Host "User IDs found: $($userIds -join ', ')"

    # If a start user ID is specified, adjust the list to start from that user
    if ($startUserId -ne $null) {
        if ($userIds -contains $startUserId.ToString()) {
            $startIndex = $userIds.IndexOf($startUserId.ToString())
            $userIds = $userIds[$startIndex..($userIds.Count - 1)]
            Write-Host "Processing users starting from User ID $startUserId."
        } else {
            Write-Host "Specified start User ID $startUserId not found. Processing all users."
        }
    } else {
        Write-Host "No start User ID specified. Processing all users."
    }

    # Activate the virtual environment
    Write-Host "Activating the virtual environment..."
    . .\env\Scripts\Activate.ps1

    # Loop through each user
    foreach ($userId in $userIds) {
        Write-Host "------------------------------------"
        Write-Host "Switching to user $userId..."

        # Switch to the current user
        adb -s localhost:$port shell am switch-user $userId

        Start-Sleep -Seconds 5

        # Start the game for the current user
        Write-Host "Starting the game for user $userId..."
        adb -s localhost:$port shell am start -n com.scopely.monopolygo/com.scopely.unity.ScopelyUnityActivity

        # Wait before starting the bot
        Write-Host "Waiting for the game to load..."
        Start-Sleep -Seconds 5

        # Run the bot script and pass the verbosity level as an argument
        Write-Host "Running bot.py for user $userId with verbosity level $vLevel..."
        python .\bot.py -v $vLevel

        Write-Host "bot.py execution for user $userId with verbosity level $vLevel completed."

        Start-Sleep -Seconds 1

        # Close the game
        Write-Host "Closing the game for user $userId..."
        adb -s localhost:$port shell am force-stop com.scopely.monopolygo

        # Wait time between users
        Write-Host "Waiting before processing next user..."
        Start-Sleep -Seconds 5

        # Ensure the game is closed
        adb -s localhost:$port shell am force-stop com.scopely.monopolygo
    }

    # Deactivate the virtual environment
    Write-Host "Deactivating the virtual environment..."
    Deactivate

    # Disconnect ADB
    adb disconnect localhost:$port

    # Stop MuMuPlayer if it's running
    if ($Process -ne $null) {
        Write-Host "Closing MuMuPlayer Emulator..."
        Stop-Process -Id $Process.Id -Force
    }

    # Stop MuMuVMM if it's running
    Write-Host "Closing MuMuVMM process..."
    $vmProcess = Get-Process -Name "MuMuVMM" -ErrorAction SilentlyContinue
    if ($vmProcess) {
        Stop-Process -Id $vmProcess.Id -Force
        Write-Host "Process MuMuVMM has been terminated."
    } else {
        Write-Host "Process MuMuVMM was not found."
    }
}

# Run the emulator and bot for each specified verbosity level
foreach ($level in $vLevels) {
    Write-Host "Running with -v $level..."
    Run-EmulatorAndBot -vLevel $level -startUserId $startUserId
    Start-Sleep -Seconds 90
}

Write-Host "Script execution completed."
