# PowerShell launcher for Jia Assistant
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyExe = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"

if (Test-Path $pyExe) {
    & $pyExe "$scriptDir\jia.py" @args
} else {
    python "$scriptDir\jia.py" @args
}
