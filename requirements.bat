@echo off

echo Installing dependencies...
pip uninstall -y Flask mutagen Pillow flask-compress pywin32
pip install Flask==2.3.3 mutagen==1.46.0 Pillow==10.1.0 flask-compress==1.14 werkzeug==2.3.7 pywin32==305

echo Installation completed!
pause
