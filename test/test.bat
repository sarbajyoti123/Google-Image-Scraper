@ECHO OFF
REM Batch file to run test on a Windows machine

ECHO Running test
ECHO.

python ../imscraper.py -f ../test/keywords.txt -l 10 -o ../test

ECHO Done
PAUSE