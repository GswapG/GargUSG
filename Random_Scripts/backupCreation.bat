@echo off
setlocal enabledelayedexpansion

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do (
	set datetime=%%I
	set datetime=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!
)

set "destination=USG Backup %datetime%"

set "wordTemplates=%APPDATA%\Microsoft\Templates"

set "script_dir=%~dp0"
set "destination_path=%script_dir%!destination!"

if exist "!destination_path!" (
	rmdir /s /q "!destination_path!"
)

mkdir "!destination_path!"
echo Backup Folder Created successfully as "!destination!"

xcopy "%wordTemplates%" "!destination_path!" /E/H/C/I /q
echo Template files copied successfully
echo Press any key to exit

pause >nul
 