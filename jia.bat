@echo off
set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PY_EXE%" (
    "%PY_EXE%" "%~dp0jia.py" %*
) else (
    python "%~dp0jia.py" %*
)
