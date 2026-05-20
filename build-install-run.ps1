Write-Host "Reverting 'pixi.lock' state..."
git checkout -- pixi.lock
$TimeStamp = get-date  -UFormat "%Y%m%d_%H%M%S"
$Target = "pixi_$TimeStamp"
Write-Host "Cleaning up .pixi to $Target..."
Move-Item .pixi $Target
Write-Host "Running 'pixi install'..."
pixi install
Write-Host "Launching application..."
.\.pixi\envs\default\Scripts\omero-downloader-gui.exe
# Write-Host "Removing previous pixi folder..."
# Remove-Item -r -Force old_pixi
