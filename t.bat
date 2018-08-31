@echo on
    echo %1
    set env=%1
    echo %env%
    echo curl -d env=%env% http://localhost:8001/dq/vrfy/tasks_aurora/