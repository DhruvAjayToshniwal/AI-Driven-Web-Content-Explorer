@echo off
echo Deleting downloaded files and directory...

if exist websites rmdir /s /q websites
if exist cleaned_websites rmdir /s /q cleaned_websites
if exist __pycache__ rmdir /s /q __pycache__
if exist train.jsonl del /f train.jsonl
if exist urls.txt del /f urls.txt
if exist last_query.txt del /f last_query.txt
if exist output.txt del /f output.txt

echo Cleanup completed.
