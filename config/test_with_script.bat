@echo off
chcp 65001 >nul
echo Тест 2: Запуск со стартовым скриптом
python -m src.main --script config/commands.txt
pause