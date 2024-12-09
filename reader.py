import os
base_path = os.path.dirname(os.path.abspath(__file__))
audio_format = ['.aiff', '.wav', '.flac', '.mp3', '.dsf', '.aac', '.ogg', '.wma', '.alac', '.m4a', '.opus']
audio_folder = os.path.join(base_path, 'audio')
output_file = os.path.join(base_path, 'audio_file_list.txt')

try:
    audio_folder = os.path.join(base_path, 'audio')
except FileNotFoundError:
    os.makedirs(audio_folder)
except Exception as e:
    print(f"오류 발생: {e}")
    
try:
    files = os.listdir(audio_folder)
    lines = []

    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(audio_folder, filename)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in audio_format:
            formatted_line = f"{index}*file*{file_path}"
            lines.append(formatted_line)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"파일 경로가 성공적으로 저장되었습니다: {output_file}")

except Exception as e:
    print(f"오류 발생: {e}")
