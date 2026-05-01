@echo off
chcp 65001 >nul
echo ========================================
echo   暗黑破坏神助手 - 打包工具
echo ========================================
echo.

REM Install dependencies
echo [1/3] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖安装失败，请检查 Python 和 pip 是否已安装
    pause
    exit /b 1
)

echo.
echo [2/3] 清理旧构建...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo [3/3] 打包为单文件 exe...
pyinstaller --onefile --windowed --name "DiabloAssistant" main.py
if %errorlevel% neq 0 (
    echo 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo   输出文件: dist\DiabloAssistant.exe
echo ========================================
pause
