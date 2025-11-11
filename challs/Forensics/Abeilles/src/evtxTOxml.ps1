# Chemin du fichier .evtx à convertir
$evtxPath = "Microsoft-Windows-Sysmon%4Operational.evtx"

# Chemin du fichier XML de sortie
$outputXmlPath = "SysmonEvents.xml"

# Lire tous les événements du fichier EVTX
$events = Get-WinEvent -Path $evtxPath

# Créer l’en-tête XML
$xmlHeader = "<?xml version=`"1.0`" encoding=`"UTF-8`"?><Events>"

# Créer le pied de page XML
$xmlFooter = "</Events>"

# Convertir chaque événement en XML et concaténer
$eventsXmlContent = $events | ForEach-Object { $_.ToXml() }

# Écrire le fichier XML complet
$xmlHeader | Out-File -FilePath $outputXmlPath -Encoding UTF8
$eventsXmlContent | Out-File -FilePath $outputXmlPath -Encoding UTF8 -Append
$xmlFooter | Out-File -FilePath $outputXmlPath -Encoding UTF8 -Append

Write-Host "Conversion terminée ! Le fichier XML est ici : $outputXmlPath"
