@echo off
set env=%1
if "%env%" == "" (
    echo ====================================================
    echo = USAGE : %0 dev  # ����ȯ�����  
    echo = USAGE : %0 tst  # �׽�Ʈȯ����� 
    echo = USAGE : %0 prd  # �ȯ����� 
    echo ====================================================

) else (
@echo on
    curl -d env=%env% http://localhost:8001/dq/vrfy/tasks_aurora/
)
