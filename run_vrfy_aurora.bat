@echo off
set env=%1
if "%env%" == "" (
    echo ====================================================
    echo = USAGE : %0 dev  # 개발환경수행  
    echo = USAGE : %0 tst  # 테스트환경수행 
    echo = USAGE : %0 prd  # 운영환경수행 
    echo ====================================================

) else (
@echo on
    curl -d env=%env% http://localhost:8001/dq/vrfy/tasks_aurora/
)
