Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

uv run pyinstaller `
  --onefile `
  --noconsole `
  --name keysound `
  --add-data "sounds;sounds" `
  main.py

Write-Host ""
Write-Host "Built: dist/keysound.exe"
