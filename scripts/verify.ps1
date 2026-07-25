param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$virtualPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $virtualPython)) {
    throw "The virtual environment is missing. Run .\scripts\setup.ps1 first."
}

Push-Location -LiteralPath $projectRoot
try {
    & $virtualPython manage.py check
    & $virtualPython manage.py makemigrations --check --dry-run
    & $virtualPython -m coverage erase
    & $virtualPython -m coverage run manage.py test
    & $virtualPython -m coverage report --fail-under=95 -m
} finally {
    Pop-Location
}
