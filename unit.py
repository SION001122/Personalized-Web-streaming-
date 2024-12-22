import os
import threading
import time
from mutagen import File
from PIL import Image
import io
# 오디오 파일 목록을 추출하는 함수
def extract_audio_files(file_list_path):
    audio_files = []
    with open(file_list_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if "*file*" in line:
                file_path = line.split("*file*")[1]
                absolute_file_path = os.path.abspath(file_path)

                # UTF-8로 인코딩된 경로를 사용하여 처리
                encoded_path = absolute_file_path.encode('utf-8').decode('utf-8')

                # 다양한 확장자에 따른 처리
                if encoded_path.endswith(".flac"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-5]  # '.flac' 제거
                elif encoded_path.endswith(".wav"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.wav' 제거
                elif encoded_path.endswith(".mp3"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.mp3' 제거
                elif encoded_path.endswith(".aiff"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-5]  # '.aiff' 제거
                elif encoded_path.endswith(".dsf") or encoded_path.endswith(".dff"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.dsf' 또는 '.dff' 제거
                elif encoded_path.endswith(".aac"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.aac' 제거
                elif encoded_path.endswith(".ogg"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.ogg' 제거
                elif encoded_path.endswith(".opus"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-5]  # '.opus' 제거
                elif encoded_path.endswith(".wma"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.wma' 제거
                elif encoded_path.endswith(".ape"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.ape' 제거
                elif encoded_path.endswith(".mpc"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.mpc' 제거
                elif encoded_path.endswith(".m4a") or encoded_path.endswith(".m4b") or encoded_path.endswith(".m4r"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.m4a', '.m4b', '.m4r' 제거
                elif encoded_path.endswith(".aa"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-3]  # '.aa' 제거
                elif encoded_path.endswith(".aax"):
                    cleaned_file_name = os.path.basename(encoded_path)[:-4]  # '.aax' 제거
                else:
                    cleaned_file_name = os.path.basename(encoded_path)  # 다른 확장자 또는 확장자 없는 파일은 그대로 유지

                # 파일 정보를 추가
                audio_files.append({"path": encoded_path, "name": cleaned_file_name})
    
    return audio_files

def is_safe_path(base_path, user_path):
    """
    주어진 경로가 허용된 디렉토리 내부에 있는지 확인합니다.
    """
    abs_base = os.path.abspath(base_path)
    abs_path = os.path.abspath(os.path.join(base_path, user_path))
    return abs_path.startswith(abs_base)
        
        # 앨범 커버 추출 함수
def extract_album_cover(file_path):
    try:
        audio = File(file_path)
        if audio is None:
            print(f"지원되지 않는 파일 형식: {file_path}")
            return None
        
        if "APIC:" in audio.tags:
            album_cover = audio.tags["APIC:"].data
        elif "covr" in audio:
            album_cover = audio["covr"][0]
        elif hasattr(audio, "pictures") and len(audio.pictures) > 0:
            album_cover = audio.pictures[0].data
        else:
            print("앨범 커버를 찾을 수 없습니다2.")
            image = Image.open(r".\none.png")
            image_byte_array = image.save(io.BytesIO(), format="PNG")
            image.save(image_byte_array, format="PNG")
            image_byte_array.seek(0)
            return image_byte_array

        image = Image.open(io.BytesIO(album_cover))
        image_byte_array = io.BytesIO()
        image.save(image_byte_array, format="PNG")
        image_byte_array.seek(0)
        return image_byte_array

    except Exception as e:
        print(f"앨범 커버를 추출할 수 없습니다: {e}")
        return None

def get_audio_duration(file_path):
    """
    주어진 음원 파일의 재생 시간을 초 단위로 반환.
    """
    try:
        audio = File(file_path)
        if audio and audio.info:
            return audio.info.length
    except Exception as e:
        print(f"오류 발생: {e}")
    return audio.info.length
