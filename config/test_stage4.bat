@echo off
chcp 65001 >nul
echo Тест 4 этапа: основные команды (ls, cd, head, tac, rev)
python -m src.main --vfs data/vfs_deep_structure.json --script config/commands_stage4.txt
pause