# Environment
Windows 11

Python 3.13

Pip 24.3


# Prepare Development Environment
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```


# Build Distributable Executable
```
.\.venv\Scripts\Activate.ps1
pyinstaller -F .\EqSmartFire.py
```


# Update requirements.txt
```
pip freeze > requirements.txt
```
