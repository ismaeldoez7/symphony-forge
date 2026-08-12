@echo off
setlocal
set "PYTHONUTF8=1"

:python
where py >nul 2>nul
if errorlevel 1 goto python_fallback
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto python_fallback
set "FORGE_PYTHON=py"
goto discover_shell

:python_fallback
where python >nul 2>nul
if errorlevel 1 goto python3_fallback
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto python3_fallback
set "FORGE_PYTHON=python"
goto discover_shell

:python3_fallback
where python3 >nul 2>nul
if errorlevel 1 goto bootstrap
python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto bootstrap
set "FORGE_PYTHON=python3"
goto discover_shell

:bootstrap
if defined FORGE_PYTHON_BOOTSTRAP_ATTEMPTED goto missing
set "FORGE_PYTHON_BOOTSTRAP_ATTEMPTED=1"
set "FORGE_LOCAL_APP_DATA="
for /f "usebackq delims=" %%I in (`"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -NonInteractive -Command "[Environment]::GetFolderPath('LocalApplicationData')" 2^>nul`) do if not defined FORGE_LOCAL_APP_DATA set "FORGE_LOCAL_APP_DATA=%%I"
if not defined FORGE_LOCAL_APP_DATA goto missing
set "FORGE_WINGET=%FORGE_LOCAL_APP_DATA%\Microsoft\WindowsApps\winget.exe"
if not exist "%FORGE_WINGET%" goto missing
"%FORGE_WINGET%" install --id Python.Python.3.14 --exact --scope user --source winget --silent --accept-package-agreements --accept-source-agreements
if errorlevel 1 goto missing
set "PATH=%FORGE_LOCAL_APP_DATA%\Programs\Python\Python314;%FORGE_LOCAL_APP_DATA%\Programs\Python\Launcher;%FORGE_LOCAL_APP_DATA%\Microsoft\WindowsApps;%PATH%"
"%~f0" %*
exit /b %errorlevel%

:discover_shell
if defined CLAUDE_CODE_GIT_BASH_PATH for %%I in ("%CLAUDE_CODE_GIT_BASH_PATH%") do if /i "%%~xI"==".exe" (
  "%%~I" "%~dp0forge" --help >nul 2>nul
  if not errorlevel 1 set "FORGE_SH=%%~I"
)
if defined FORGE_SH goto run_sh

for /f "delims=" %%I in ('where sh 2^>nul') do if not defined FORGE_SH for %%J in ("%%I") do if /i "%%~xJ"==".exe" (
  "%%~J" "%~dp0forge" --help >nul 2>nul
  if not errorlevel 1 set "FORGE_SH=%%~J"
)
if defined FORGE_SH goto run_sh

for %%I in (
  "%ProgramFiles%\Git\bin\bash.exe"
  "%ProgramFiles%\Git\usr\bin\bash.exe"
  "%ProgramFiles%\Git\usr\bin\sh.exe"
  "%ProgramFiles(x86)%\Git\bin\bash.exe"
  "%ProgramFiles(x86)%\Git\usr\bin\bash.exe"
  "%ProgramFiles(x86)%\Git\usr\bin\sh.exe"
  "%LOCALAPPDATA%\Programs\Git\bin\bash.exe"
  "%LOCALAPPDATA%\Programs\Git\usr\bin\bash.exe"
  "%LOCALAPPDATA%\Programs\Git\usr\bin\sh.exe"
) do if not defined FORGE_SH if exist "%%~I" if /i "%%~xI"==".exe" (
  "%%~I" "%~dp0forge" --help >nul 2>nul
  if not errorlevel 1 set "FORGE_SH=%%~I"
)
if defined FORGE_SH goto run_sh
goto run_python

:run_sh
"%FORGE_SH%" "%~dp0forge" %*
exit /b %errorlevel%

:run_python
if "%FORGE_PYTHON%"=="py" goto run_py
if "%FORGE_PYTHON%"=="python" goto run_python_exe
if "%FORGE_PYTHON%"=="python3" goto run_python3_exe
goto missing

:run_py
py -3 "%~dp0factory\scripts\forge.py" %*
exit /b %errorlevel%

:run_python_exe
python "%~dp0factory\scripts\forge.py" %*
exit /b %errorlevel%

:run_python3_exe
python3 "%~dp0factory\scripts\forge.py" %*
exit /b %errorlevel%

:missing
echo [FAIL] Python 3.10 or newer was not found. Install App Installer/winget or install Python manually from https://www.python.org/downloads/windows/ and rerun forge. 1>&2
exit /b 2
