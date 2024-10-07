$Process = Start-Process "C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell\MuMuPlayer.exe" -PassThru
Start-Sleep -Seconds 60

if ($Process -ne $null) {
    Write-Host "Closing MuMuPlayer Emulator..."
    Stop-Process -Id $Process.Id -Force
}