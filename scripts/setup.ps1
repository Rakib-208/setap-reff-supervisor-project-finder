param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$virtualPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

Push-Location -LiteralPath $projectRoot
try {
    if (-not (Test-Path -LiteralPath $virtualPython)) {
        python -m venv .venv
    }

    & $virtualPython -m pip install --upgrade pip
    & $virtualPython -m pip install -r requirements.txt
    & $virtualPython manage.py migrate --noinput
    & $virtualPython manage.py seed_demo
    & $virtualPython manage.py check

    Write-Host ""
    Write-Host "ProjectFinder is ready."
    Write-Host "Start it with: .\.venv\Scripts\python.exe manage.py runserver"
} finally {
    Pop-Location
}
