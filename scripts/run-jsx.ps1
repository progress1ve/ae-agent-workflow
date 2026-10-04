param(
 [Parameter(Mandatory=$true)][string]$ScriptPath,
 [Parameter(Mandatory=$true)][string]$AfterEffectsExe
)
$aeScript=(Resolve-Path -LiteralPath $ScriptPath -ErrorAction Stop).Path
$aeExe=(Resolve-Path -LiteralPath $AfterEffectsExe -ErrorAction Stop).Path
if([IO.Path]::GetExtension($aeScript) -ne '.jsx'){throw 'Expected a reviewed .jsx script'}
if(-not (Get-Process AfterFX -ErrorAction SilentlyContinue)){throw 'Open a normal After Effects instance and the target project first'}
Start-Process -FilePath $aeExe -ArgumentList '-r',('"'+$aeScript+'"') -WindowStyle Hidden
Write-Output 'Dispatched script. Inspect AE and its completion marker; dispatch is not proof of success.'
