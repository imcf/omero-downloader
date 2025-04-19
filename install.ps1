$repoUrl = "https://git.scicore.unibas.ch/imcf/omero/omero-downloader.git"
$envName = "S:\anaconda_envs\omero-py_env"
$appDir = "C:\Tools\omero-downloader"
$ymlFile = "omero_downloader_environment.yml"
$ymlPath = Join-Path $appDir $ymlFile

if (-not (Test-Path $appDir)) {
    git clone $repoUrl $appDir
}

if (-not (Test-Path $envName)) {
    New-Item -Path $envName -ItemType Directory
    conda.bat env create --prefix=$envName --file=$ymlPath -y
}

