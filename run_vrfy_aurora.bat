@echo off
if "%1" == "" (
    set env=dev
) else (
    set env=%1
)
@echo on 
curl -d env=%env% http://localhost:8001/dq/vrfy/tasks_aurora/