#!/bin/bash

# Open terminal for Python app
osascript -e 'tell application "Terminal"
    do script "cd Downloads/clipbook-main/ && source venv/bin/activate  && python3 server.py"
end tell'

# Wait 1 second
sleep 5

# Open terminal for ngrok
osascript -e 'tell application "Terminal"
    do script "ngrok http 8000"
end tell'

