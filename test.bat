@echo off

echo "Output 1"
timeout /t 1
1>&2 echo "Error 1"
timeout /t 1
echo "Output 2"
timeout /t 1
1>&2 echo "Error 2"
