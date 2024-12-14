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
            # 앨범 이름을 추출하는 방법
            album = None
            artist = None

            if 'TALB' in audio.tags: # TALB이라는 태그가 있는 경우
                album = audio.tags['TALB'].text[0] # 앨범 이름을 가져옵니다
            elif 'ALBUM' in audio: # ALBUM이라는 태그가 있는 경우
                album = audio.tags['ALBUM'][0] # 앨범 이름을 가져옵니다
            elif '©alb' in audio: # ©alb이라는 태그가 있는 경우
                album = audio.tags['©alb'][0] # 앨범 이름을 가져옵니다
            elif 'IARL' in audio: # IARL이라는 태그가 있는 경우
                album = audio.tags['IARL'][0] # 앨범 이름을 가져옵니다

            if 'TPE1' in audio.tags: # TPE1이라는 태그가 있는 경우
                artist = audio.tags['TPE1'].text[0]  # 아티스트 이름을 가져

            # 앨범 정보와 아티스트 정보를 함께 반환 #
            audio_album_list.append((album, artist)) # 앨범 정보와 아티스트 정보를 리스트에 추가
            continue # 다음 파일로 넘어갑니다
        except:
            audio_album_list.append(("Unknown", "Unknown")) # 앨범 정보와 아티스트 정보를 리스트에 추가
            continue # 다음 파일로 넘어갑니다
    return audio_album_list # 앨범 정보와 아티스트 정보를 반환

def album_list(file_list_path):
    name_list = extract_audio_files(file_list_path) # 파일 경로를 가져옵니다
    name_list = [(item['name'], item['path']) for item in name_list]  # 파일의 메타데이터에서 이름과 경로를 가져옵니다
    album_dict = dict(zip(name_list, audio_album(file_list_path))) # # 파일 이름과 경로를 키로, 앨범 정보와 아티스트 정보를 값으로 하는 딕셔너리를 만듭니다
    merged_album_dict = {} #빈 딕셔너리를 만듭니다
    for song, (album, artist) in album_dict.items(): # 앨범과 아티스트 정보를 가져옵니다
        album_info = f"{album} - {artist}"  # 앨범과 아티스트 이름이 합쳐진 문자열을 만듭니다
        if album_info not in merged_album_dict: # 앨범이 없으면
            merged_album_dict[album_info] = []  # 앨범이 없으면 리스트 초기화
        merged_album_dict[album_info].append(song) # 앨범이 있으면 리스트에 추가
    return merged_album_dict # 앨범 정보를 반환


def json_album_list(file_list_path):
        album_json = album_list(file_list_path)  # 앨범 정보를 가져옵니다
        print("DEBUG: album_list output =", album_json)  # 디버깅을 위한 출력

        converted_album_json = {}
        idx = 1  # 전역 인덱스 변수 초기화

        for album, songs in album_json.items(): # 앨범 정보를 가져옵니다
            converted_album_json[album] = [] # 앨범 정보를 키로 하는 빈 리스트를 만듭니다   
            for song in songs:
                converted_album_json[album].append({
                    'index': idx,           # 전역 인덱스 할당
                    'name': song[0],   # 트랙 이름
                    'path': song[1]    # 트랙 경로
                })
                idx += 1  # 인덱스 증가

        # UTF-8로 강제 설정
        return json.dumps(converted_album_json, ensure_ascii=False, indent=4).encode('utf-8').decode('utf-8')  # JSON 데이터를 반환

def save_json_to_file(file_list_path, output_json_path):
    # json_album_list로 변환된 JSON 데이터를 파일로 저장
    album_json = json_album_list(file_list_path)
    
    # JSON 데이터를 파일로 저장
    with open(output_json_path, 'w', encoding='utf-8') as json_file: # JSON 파일을 쓰기 모드로 엽니다
        json_file.write(album_json) # JSON 데이터를 파일에 씁니다

    print(f"JSON 파일이 {output_json_path}에 저장되었습니다.") # 저장 완료 메시지 출력
