Write-Host "[*] verificando privilegios" -ForegroundColor Yellow

$isAdmin = (
    [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)

if (-not $isAdmin) {
    Write-Host "[!] elevacion con UAC requerida" -ForegroundColor Red
    Start-Process powershell -Verb RunAs -ArgumentList "-NoExit", "-ExecutionPolicy Bypass", "-File `"$PSCommandPath`""
    exit
}


Write-Host "[+] privilegios elevados, ejecutando SIEM-PROTOTYPE" -ForegroundColor Green

$projectPath = Split-Path -Parent $PSCommandPath
Set-Location $projectPath


Write-Host "[*] se activara entorno SIEMENV"
$venvPath = ".\siemenv\Scripts\Activate.ps1"
& $venvPath


Write-Host "[*] Ejecutando SIEM-PROTOTYPE"
python -m src.main