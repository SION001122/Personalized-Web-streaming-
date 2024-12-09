if [ ! -d "venv" ]; then
    python -m venv venv
fi
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
if [ ! -f "audio_file_list.txt" ]; then
    python reader.py
    echo "Created empty audio_file_list.txt file"
fi
    python app.py
else
    echo "venv directory not found"
fi
