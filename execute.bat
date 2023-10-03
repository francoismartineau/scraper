@echo off
cd %~dp0
call .\venv\Scripts\activate
@REM call python src\main.py topics\prop.json
call python src\main.py topics\skate.json
@REM call python src\main.py topics\misc.json