
#register commit hook
echo "bash shell/pre-commit.sh" > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

if test -f shell/pre-commit.sh ; then
    echo "pre-commit script exists"
else 
   ( echo "#Test and format code" ; echo "bash shell/test.sh && venv/bin/isort --sl src && venv/bin/black src && git add src" )> shell/pre-commit.sh && git add .git/hooks/pre-commit pre-commit.sh
fi

python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt -r requirements.dev.txt

echo "Congratulations!!!! Project Initialized Successfully!!!!"
