@echo off
REM Activate the Anaconda environment
call C:\ProgramData\anaconda3\Scripts\activate.bat S:\anaconda_envs\omero-py_env

REM Change directory to where your script is located
cd C:\Tools\omero-downloader

REM Run the Python application
echo Starting Omero Downloader application
python omero_downloader_gui.py

REM If "pause", the command prompt remains open after the Python app is closed.
REM pause
