@echo off
if "%1" == "" (
    echo ====================================================
    echo = USAGE : %0 dev  # ����ȯ�����  
    echo = USAGE : %0 tst  # �׽�Ʈȯ����� 
    echo = USAGE : %0 prd  # �ȯ����� 
    echo ====================================================

) else (
    set env=%1
    curl -d env=%env% http://localhost:8001/dq/vrfy/tasks_aurora/
)
