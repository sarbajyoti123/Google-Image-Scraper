REM Batch file to run test

ECHO Running test
ECHO.

python imscraper.py -f test/keywords.txt -l 10 -outdir test

ECHO Done
PAUSE