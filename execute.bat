@echo off
cd %~dp0
call .\venv\Scripts\activate
call python src\main.py topics\prop.json
call python src\main.py topics\skate.json
call python src\main.py topics\misc.json