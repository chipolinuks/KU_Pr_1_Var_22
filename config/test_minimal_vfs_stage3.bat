@echo off
chcp 65001 >nul
echo Тест: Минимальная VFS
python -m src.main --vfs data/vfs_minimal.json --script config/commands_minimal_stage3.txt
pause