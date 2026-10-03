@echo off
chcp 65001 >nul
echo Тест 3: Запуск с VFS и скриптом
python -m src.main --vfs data/my_vfs.json --script config/commands.txt
pause