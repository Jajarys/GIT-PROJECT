@echo off
chcp 65001 >nul 2>&1
title Система Управління Складом
cd /d "%~dp0"
python app.py
