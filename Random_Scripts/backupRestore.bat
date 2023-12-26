@echo off
setlocal enabledelayedexpansion

set "wordTemplates=%APPDATA%\Microsoft\Templates"

set "script_dir=%~dp0"

for /f "delims=" %%F in ('dir /b /ad /o-d "!script_dir!USG Backup*"') do (
	set "latest_backup=%%F"
	goto :copy_files
)
goto :ending
:copy_files
if defined latest_backup (
	echo Backup found as "!latest_backup!"
	set /p "choi=Do you want to restore templates to the backup found? (Y/N): "
	if /i "!choi!"=="Y" (
		echo Restore initiated...
	) else (
		echo Restore cancled. Press any key to continue.....
		pause >nul
		goto :proper_ending
	)
	set "source=!script_dir!!latest_backup!"

	rmdir /s /q "%wordTemplates%"

	mkdir "%wordTemplates%"

	xcopy "!source!" "%wordTemplates%" /E/C/H/I /q
	
	echo Files copied successfully 
) else (
	echo No Backup Folders found!!
)

echo .
echo WARNING: Save any work before you restart

set /p "choice=Do you want to restart the computer? (Y/N): "

if /i "%choice%"=="Y" (
	echo Restarting the computer.....
	shutdown /r /t 10 /c "Restarting computer as requested by user"
	goto :proper_ending
) else (
	echo Restart canceled. Restart manually to properly complete backup restore
	echo Press any key to exit......
	pause >nul
	goto :proper_ending
)
:ending
echo No backup found!! Press any key to exit.........
pause >nul
:proper_ending