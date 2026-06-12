@echo off
setlocal

set GIT_PATH=C:\Program Files\Git\bin\git.exe
set REPO_URL=https://github.com/LuoHong2000/1111.git

echo 配置Git...
"%GIT_PATH%" config user.name "LuoHong2000"
"%GIT_PATH%" config user.email "your_email@example.com"

REM 检查是否已经初始化
if not exist ".git" (
    echo 初始化仓库...
    "%GIT_PATH%" init
)

REM 检查是否已添加远程仓库，更新或添加
set "remote_exists="
for /f "tokens=*" %%i in ('"%GIT_PATH%" remote') do (
    if "%%i"=="origin" (
        set "remote_exists=1"
        echo 更新远程仓库URL...
        "%GIT_PATH%" remote set-url origin %REPO_URL%
        goto :git_add
    )
)

if not defined remote_exists (
    echo 添加远程仓库...
    "%GIT_PATH%" remote add origin %REPO_URL%
)

:git_add
echo 添加文件...
"%GIT_PATH%" add .

echo 提交...
"%GIT_PATH%" commit -m "Initial commit: RAG智能问答系统" || echo 没有新文件需要提交

echo 推送到GitHub...
"%GIT_PATH%" push -u origin main || (
    echo 推送失败，尝试强制推送...
    "%GIT_PATH%" push -f -u origin main
)

echo 完成！
pause

endlocal