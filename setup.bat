@echo off
:: Initialisation Git
if not exist .git (
    git init
    git add .
    git commit -m "Initialisation du projet Porte-vue"
)

:: Environnement virtuel
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Projet initialise et environnement pret.