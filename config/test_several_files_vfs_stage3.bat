@echo off
chcp 65001 >nul
echo Тест: VFS с несколькими файлами
python -m src.main --vfs data/vfs_several_files.json --script config/commands_several_files_stage3.txt
pause