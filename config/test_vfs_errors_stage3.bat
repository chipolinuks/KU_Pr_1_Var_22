@echo off
chcp 65001 >nul
echo Тест 1: Файл VFS не найден
python -m src.main --vfs data/nonexistent.json --script config/commands_error_test_stage3.txt
pause

echo Тест 2: Неверный формат VFS
python -m src.main --vfs data/broken.json --script config/commands_error_test_stage3.txt
pause

echo Тест 3: Путь к VFS не указан
python -m src.main --script config/commands_error_test_stage3.txt
pause