#!/bin/sh

read -p "Please Enter chrome.exe Path:" -r r1

parent="$r1" 

cd "$parent"

chrome.exe --remote-debugging-port=9222 --user-data-dir=remote-profile
