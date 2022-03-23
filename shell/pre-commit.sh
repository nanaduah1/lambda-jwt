#Test and format code
bash shell/test.sh && venv/bin/isort --sl src && venv/bin/black src && git add src
