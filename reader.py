import os
import win32com.client

# .lnk 파일을 해석하여 실제 파일 경로를 반환하는 함수
def resolve_shortcut(shortcut_path):
    # WScript.Shell을 사용하여 바로가기 파일을 해석
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    target_path = shortcut.TargetPath  # 바로가기가 가리키는 실제 경로
    print(f"해석된 바로가기 경로: {target_path}")  # 디버깅용 출력
    return target_path

base_path = os.path.dirname(os.path.abspath(__file__))
audio_folder = os.path.join(base_path, 'audio')
output_file = os.path.join(base_path, 'audio_file_list.txt')

try:
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
        print(f"폴더가 생성되었습니다: {audio_folder}")
    
    files = os.listdir(audio_folder)
    lines = []

    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(audio_folder, filename)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()

            # 오디오 파일 확장자 리스트
            audio_extensions = ['.aiff', '.wav', '.flac', '.mp3', '.dsf', '.aac', '.ogg', '.wma', '.alac', '.m4a', '.opus']

            # 오디오 파일인 경우
            if ext in audio_extensions:
                formatted_line = f"{index}*file*{file_path}"
                lines.append(formatted_line)

            # 바로가기 파일(.lnk)인 경우
            elif ext == '.lnk':
                try:
                    resolved_path = resolve_shortcut(file_path)  # 바로가기가 가리키는 실제 파일 경로
                    # 실제 경로가 존재하고 오디오 파일이면 리스트에 추가
                    if os.path.isfile(resolved_path) and os.path.splitext(resolved_path)[1].lower() in audio_extensions:
                        formatted_line = f"{index}*file*{resolved_path}"
                        lines.append(formatted_line)
                    else:
                        print(f"바로가기 파일이 오디오 파일을 가리키지 않음: {file_path}")
                except Exception as e:
                    print(f"바로가기 해석 오류: {e}")

    # 리스트를 텍스트 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"파일 경로가 성공적으로 저장되었습니다: {output_file}")

except Exception as e:
    print(f"오류 발생: {e}")
