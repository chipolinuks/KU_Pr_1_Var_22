@echo off
chcp 65001 >nul
echo Тест: Глубокая структура VFS
python -m src.main --vfs data/deep_structure.json --script config/commands_deep_stage3.txt
pause