@echo off
rmdir /s /q ".\dist"

pyinstaller --clean --workpath=".\build" --distpath=".\dist" GameOfLife.spec

rmdir /s /q ".\build"