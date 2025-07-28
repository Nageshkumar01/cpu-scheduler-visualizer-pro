@echo off
cd /d "C:\ptu placement\placement project\CPU-Scheduling-Algorithms"

echo Starting CPU Scheduling GUI...
:: Optional: Compile your C++ code if needed
:: g++ -o main.exe main.cpp

:: Start Python GUI (assumes python is added to PATH)
start "" python gui.py

:: Optional: Run main.exe manually (not needed unless debugging C++ separately)
 main.exe

exit
