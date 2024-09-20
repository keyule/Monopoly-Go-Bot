# Start MuMuPlayer
$Process = Start-Process "C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuPlayer.exe"

# Wait for the emulator to launch
Start-Sleep -Seconds 30

# Connect ADB
adb connect localhost:7555

# Get all users
$usersOutput = adb shell pm list users

# Extract user IDs from the output
$pattern = 'UserInfo{(\d+):'
$userIds = @()
foreach ($line in $usersOutput) {
    if ($line -match $pattern) {
        $userIds += $Matches[1]
    }
}

# Display all user IDs (optional)
Write-Host "User IDs found: $($userIds -join ', ')"

# Activate the virtual environment once
. .\env\Scripts\Activate.ps1

# Loop through each user
foreach ($userId in $userIds) {
    Write-Host "Starting game for user $userId"

    # Start the game for the current user
    adb -s localhost:7555 shell am start --user $userId -n com.scopely.monopolygo/com.scopely.unity.ScopelyUnityActivity

    # Wait before starting the bot
    Start-Sleep -Seconds 5

    # Run the bot script and wait for it to finish
    Write-Host "Running bot.py for user $userId"
    python .\bot.py

    # Optional: Close the game if needed
    adb -s localhost:7555 shell am force-stop com.scopely.monopolygo

    # Optional: Additional wait time between users
    Start-Sleep -Seconds 5
}

# Deactivate the virtual environment if necessary
Deactivate

# Stop MuMuPlayer if it's running
if ($Process -ne $null) {
    Stop-Process -Id $Process.Id -Force
}