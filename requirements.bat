@echo off

echo Installing dependencies...
pip install --upgrade pip
pip install Flask==2.2.5 mutagen==1.46.0 Pillow==10.0.0 flask-compress==1.13

echo Installation completed!
pause
