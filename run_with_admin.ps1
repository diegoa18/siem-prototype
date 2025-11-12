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

Write-Host "`n[*] verificando entorno virtual (siemenv)" -ForegroundColor Yellow
$venvPath = ".\siemenv\Scripts\Activate.ps1"
$venvFolder = ".\siemenv"

if (-not (Test-Path $venvFolder)) {
    Write-Host "[!] no existe entorno virtual, este se creara" -ForegroundColor Red

    python -m venv siemenv

    if (-not (Test-Path $venvFolder)) {
        Write-Host "[X] error: no se logro crear el entorno virtual" -ForegroundColor Red
        exit
    }
}


Write-Host "[+] entorno virtual creado" -ForegroundColor Green
Write-Host "[*] activando entorno virtual..."

& $venvPath


#en caso de que falten las dependencias en este y esten en requirements.txt
Write-Host "[*] verificando dependencias" -ForegroundColor Yellow
pip install --upgrade pip > $null --quiet
pip install -r requirements.txt --quiet

Write-Host "[+] dependencias OK" -ForegroundColor Green

Write-Host "[*] Ejecutando SIEM-PROTOTYPE" -ForegroundColor Cyan
python -m src.main