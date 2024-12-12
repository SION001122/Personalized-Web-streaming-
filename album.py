from unit import extract_audio_files
from mutagen import File
import os
import json

def audio_list(file_path):
    absolute_file_path = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "*file*" in line:
                file_path = line.split("*file*")[1]
                file_path = file_path.strip()
                absolute_file_path.append(os.path.abspath(file_path))
    return absolute_file_path

def audio_album(file_path):
    audio_album_list = []
    for line in audio_list(file_path):
        try:
            audio = File(line)
            if 'TALB' in audio.tags:
                audio_album_list.append(audio.tags['TALB'].text[0])
                continue
            if 'ALBUM' in audio:
                audio_album_list.append(audio.tags['ALBUM'][0])
                continue
            if '©alb' in audio:
                audio_album_list.append(audio.tags['©alb'][0])
                continue
            if 'IARL' in audio:
                audio_album_list.append(audio.tags['IARL'][0])
                continue
        except:
            audio_album_list.append("Unknown")
            continue
    return audio_album_list

def album_list(file_list_path):
    name_list = extract_audio_files(file_list_path)
    # name과 path를 각각 추출해서 튜플 형태로 저장
    name_list = [(item['name'], item['path']) for item in name_list]
    album_dict = dict(zip(name_list, audio_album(file_list_path)))
    merged_album_dict = {}
    for song, album in album_dict.items():
        if album not in merged_album_dict:
            merged_album_dict[album] = []  # 앨범이 없으면 리스트 초기화
        merged_album_dict[album].append(song)
    return merged_album_dict

def json_album_list(file_list_path):
    album_json = album_list(file_list_path)
    print("DEBUG: album_list output =", album_json)

    converted_album_json = {
        album: [{'name': song[0], 'path': song[1]} for song in songs]
        for album, songs in album_json.items()
    }
    
    # UTF-8로 강제 설정
    return json.dumps(converted_album_json, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8')

def save_json_to_file(file_list_path, output_json_path):
    # json_album_list로 변환된 JSON 데이터를 파일로 저장
    album_json = json_album_list(file_list_path)
    
    # JSON 데이터를 파일로 저장
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(album_json)

    print(f"JSON 파일이 {output_json_path}에 저장되었습니다.")
