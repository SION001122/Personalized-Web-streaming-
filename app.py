import subprocess
import threading
import random
import time
from flask import Flask, render_template, Response, send_file, request, redirect, url_for, session, flash, jsonify
from mutagen import File
from PIL import Image
import io
import copy
import os
import urllib.parse
from multiprocessing import Queue, Process
import concurrent.futures
import sys
import argparse
from album import json_album_list, save_json_to_file #빼먹은 코드 추가함.
import json
from unit import extract_audio_files, get_audio_duration, extract_album_cover
from flask_compress import Compress
app = Flask(__name__)
Compress(app)
app.secret_key = "qwyueyqwhuidhuwi@#&(*&!&@#*(HNCDLKJNCLK:SS!@#(*&(*!%*!@))))"  # 세션을 사용하기 위한 비밀 키 설정
# 스레드 풀 생성 (최대 10개의 스레드 사용)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
# 현재 접속자 수를 추적하기 위한 변수와 락 설정
current_users = 0
user_lock = threading.Lock()


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 사용자 데이터
users = {
    "user": "12345"  # 사용자 이름과 비밀번호
}

# 차단된 사용자의 접속 시간을 저장하는 딕셔너리
blocked_users = {}
# 로그인 실패 횟수를 저장하는 딕셔너리
failed_login_attempts = {}

# Heartbeat를 위한 마지막 핑 시간을 저장하는 딕셔너리
last_ping_time = {}

# 청크 크기 설정
CHUNK_SIZE = 512# 512kb 단위로 데이터를 전송

# os.path.abspath 함수로 경로를 OS에 맞게 수정
file_list_path = os.path.abspath("./audio_file_list.txt")
audio_files = extract_audio_files(file_list_path)
# 서버에서 재생 목록을 랜덤하게 섞음
shuffled_audio_files = copy.deepcopy(audio_files)
random.shuffle(shuffled_audio_files)

# Heartbeat를 위한 마지막 핑 시간을 저장하는 딕셔너리
last_ping_time = {}

output_json_path = 'albums_list.json'

# Heartbeat 기능을 구현하여 주기적으로 클라이언트 연결 상태를 확인
def heartbeat_checker():
    while True:
        current_time = time.time()
        with user_lock:
            for user, last_ping in list(last_ping_time.items()):
                if current_time - last_ping > 30:  # 30초 동안 응답이 없는 경우 연결 끊김으로 간주
                    print(f"Client {user} disconnected due to inactivity")
                    del last_ping_time[user]
        threading.Event().wait(20)  # 20초마다 체크
        
        
# Heartbeat 엔드포인트
@app.route("/ping", methods=["POST"])
def ping():
    username = session.get("username")
    if username:
        with user_lock:
            last_ping_time[username] = time.time()
        return jsonify({"status": "alive"}), 200
    return jsonify({"status": "unauthorized"}), 401

@app.route("/public/none")
def error_album_cover():
    image = Image.open(r".\none.png")
    image_byte_array = image.save(io.BytesIO(), format="PNG")
    image.save(image_byte_array, format="PNG")
    image_byte_array.seek(0)
    print("앨범 커버를 찾을 수 없습니다.")
    return image_byte_array

# 앨범 커버를 제공하는 라우트
@app.route("/cover/<filename>")
def get_album_cover(filename):
    file_info = next((f for f in shuffled_audio_files if os.path.basename(f["path"]) == filename), None)
    if file_info and os.path.exists(file_info["path"]):
        image = extract_album_cover(file_info["path"])
        if image:
            return send_file(image, mimetype="image/png")
    return "No cover available", 404
    
@app.route("/")
def index():
    global current_users
    with user_lock:
        current_users += 1
        print(f"현재 접속자 수: {current_users}")  # 접속자 수를 터미널에 출력

    # 접속 차단 확인
    username = session.get("username")
    
    # 차단된 사용자 처리
    if username in blocked_users:
        block_time = blocked_users[username]
        if time.time() - block_time < 30:  # 30초 동안 차단
            return "접속이 차단되었습니다. 잠시 후 다시 시도해주세요.", 403  # 403 Forbidden
        else:
            # 30초가 경과하면 차단 해제 및 실패 횟수 초기화
            del blocked_users[username]
            failed_login_attempts[username] = 0  # 초기화

    if "username" in session:
        return render_template("index.html", audio_files=shuffled_audio_files)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # 로그인 실패 횟수 확인 및 업데이트
        if username not in failed_login_attempts:
            failed_login_attempts[username] = 0
        
        if username in users and users[username] == password:
            session["username"] = username  # 세션에 사용자 정보 저장
            flash("로그인 성공!")
            # 실패 횟수 초기화
            failed_login_attempts[username] = 0
            return redirect(url_for("index"))
        else:
            flash("사용자 이름 또는 비밀번호가 잘못되었습니다.")
            # 로그인 실패 시 실패 횟수 증가
            failed_login_attempts[username] += 1
            
            # 5회 실패 시 차단 처리
            if failed_login_attempts[username] >= 5:
                blocked_users[username] = time.time()  # 현재 시간을 차단 시간으로 저장
                flash("5회 로그인 실패로 인해 접속이 차단되었습니다. 30초 후에 다시 시도해 주세요.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)  # 세션에서 사용자 정보 제거
    flash("로그아웃되었습니다.")
    return redirect(url_for("login"))

#def sanitize_path(file_path):
    # 경로 내의 공백이나 특수문자를 URL 인코딩 방식으로 변환
#    return urllib.parse.quote(file_path)
# 오디오 스트리밍
# 현재 실행 중인 ffmpeg 프로세스를 추적하기 위한 전역 변수
current_process = None
max_processes = sys.maxsize # 최대 실행 가능한 프로세스 수
process_list = []  # 프로세스 목록: [(process, last_access_time)]

process_list_lock = threading.Lock()
stop_event = threading.Event()

# 현재 실행 중인 프로세스 관리 함수
def manage_process_list():
    global process_list
    with process_list_lock:  # 락을 사용하여 동시성 문제 방지
        process_list = [(proc, last_access) for proc, last_access in process_list if proc.poll() is None] # 종료되지 않은 프로세스만 남김
        #위 코드의 과정은 다음과 같습니다. process_list의 각 요소를 순회하면서 프로세스의 poll() 메서드를 사용하여 프로세스가 종료되었는지 확인합니다. 종료되지 않은 프로세스만 남기고 나머지는 제거합니다.
        #proces_list에 프로세스가 들어가는 내용은 어떤 함수인지 
    print(f"현재 실행 중인 프로세스 수: {len(process_list)}")

def terminate_inactive_processes_with_duration():
    """
    비활성 프로세스 종료 스레드 함수 (재생 시간 기준 추가).
    """
    global process_list
    with app.app_context():  # Flask 애플리케이션 컨텍스트 설정
        while not stop_event.is_set():  # stop_event가 설정되지 않은 동안 반복
            current_time = time.time()
            with process_list_lock:
                for proc, last_access in process_list[:]:
                    try:
                        # 프로세스 파일의 경로를 찾음
                        proc_info = next((f for f in shuffled_audio_files if proc.args and f["path"] in proc.args), None)
                        if not proc_info:
                            continue

                        file_duration = get_audio_duration(proc_info["path"])
                        # file_duration 값 검증
                        if file_duration is None or not isinstance(file_duration, (float, int)):

                            continue

                        # 프로세스가 재생 시간 + 0.5초를 초과했는지 확인
                        if current_time - last_access >= file_duration + 0.5 and proc.poll() is None:
                            proc.terminate()
                            try:
                                proc.wait(timeout=1)  # 1초 대기 후 종료 확인
                                if proc.poll() is None:  # 여전히 종료되지 않았다면
                                    proc.kill()  # 강제 종료
                                    proc.wait()  # 강제 종료 후 대기
                                print(f"프로세스 종료됨. PID: {proc.pid}, 종료 코드: {proc.returncode}")
                            except subprocess.TimeoutExpired:
                                print(f"프로세스 {proc.pid} 종료 대기 시간 초과. 강제 종료 시도.")
                                proc.kill()  # 강제 종료 시도
                                proc.wait()  # 강제 종료 후 대기
                            finally:
                                # 정상적으로 종료된 경우 리스트에서 제거
                                process_list.remove((proc, last_access))
                    except Exception as e:
                        print(f"프로세스 {proc.pid} 종료 중 오류 발생: {e}")
            time.sleep(0.5)  # 0.5초마다 반복


# 오디오 재생 시간 엔드포인트 추가
@app.route("/audio/duration", methods=["POST"])
def post_audio_duration():
    file_path = request.form.get("file_path")
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    file_duration = get_audio_duration(file_path)
    if file_duration is None:
        return jsonify({"error": "Could not retrieve duration"}), 500
    print(f"File duration: {file_duration} seconds")
    return jsonify({"duration": file_duration})



# 비활성 프로세스 종료 스레드 시작
cleanup_thread = threading.Thread(target=terminate_inactive_processes_with_duration, daemon=True)
cleanup_thread.start()


@app.route("/audio/<filename>")
def stream_audio(filename):
    filter_string = ''  # 필터가 없을 때 기본값은 빈 문자열

    selected_effects = request.args.get('effects', '')

    # 음장 효과 필터 설정
    filter_string = ''  # 필터가 없을 때 기본값은 빈 문자열
    
    if 'echo' in selected_effects:
        filter_string += 'aecho=0.8:0.9:1000:0.3'  # 에코 필터 추가


    manage_process_list()  # 현재 실행 중인 프로세스 관리
    if len(process_list) >= max_processes:
        return "Maximum number of processes running. Try again later.", 429  # Too many requests
    
    # 파일 정보 찾기
    file_info = next((f for f in shuffled_audio_files if os.path.basename(f["path"]) == filename), None)
    if file_info and os.path.exists(file_info["path"]):
        print(f"Streaming file: {file_info['path']}")
        if not os.path.basename(file_info["path"]) == filename:
                return "Invalid file request", 400
        # 파일의 길이 출력
        print(f"File duration: {get_audio_duration(file_info['path'])} seconds")
        def generate():
            file_path = os.path.abspath(file_info["path"])
            # 파일 확장자 추출
            file_extension = os.path.splitext(file_path)[1].lower()
            cpu_count = os.cpu_count()
            threads = str(max(1, cpu_count // 2))  # 최소 1개의 쓰레드 보장
            # 확장자에 따른 FFmpeg 명령어 설정
            if file_extension == '.aiff':
                #command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-sample_fmt', 's32', '-threads', str(threads)]
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension in ['.dsf', '.dff']:
                command = [
                    'ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac',
                    '-sample_fmt', 's32',  # 32비트 PCM
                    '-threads', str(threads)
                ]
            elif file_extension == '.wav':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.flac':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.mp3':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.m4a':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.ogg':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.opus':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.wma':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.mka':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.mpc':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.ape':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.m4b':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.m4p':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.m4r':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.aac':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.aa':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            elif file_extension == '.aax':
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            else:
                command = ['ffmpeg', '-i', file_path, '-map', '0:a', '-f', 'flac', '-c:a', 'flac', '-threads', str(threads)]
            # 음장 효과 필터가 있을 경우 명령어에 필터 추가
            if filter_string:
                command.extend(['-af', filter_string])

            
            command.append('-')  # FFmpeg 출력 설정을 파이프로 처리
                
            # FFmpeg 프로세스를 stdout으로 실행
            current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process_list.append((current_process, time.time()))  # 프로세스 추가 및 시간 기록
            try:
                while True: # 데이터를 전송할 때마다 last_access 갱신
                    chunk = current_process.stdout.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk

                    # 데이터를 전송할 때마다 last_access 갱신
                    for i, (proc, last_access) in enumerate(process_list):
                        if proc == current_process:
                            process_list[i] = (proc, time.time())  # 데이터 전송 중이므로 갱신

                remaining_data = current_process.stdout.read()
                while remaining_data:
                    yield remaining_data
                    remaining_data = current_process.stdout.read()

            except Exception as e:
                print(f"Error while streaming: {e}")

            finally:
                current_process.stdout.close()
                current_process.wait()

                error = current_process.stderr.read().decode(errors="ignore")
                if current_process.returncode != 0:
                    print(f"FFmpeg error (Exit Code {current_process.returncode}): {error}")
                manage_process_list()
        # Cache-Control과 Gzip/Brotli 압축 활성화
        response = Response(generate(), mimetype="audio/flac")
        response.headers['Cache-Control'] = 'public, max-age=3600'

        return response

@app.route("/albums_list", methods=["GET"])
def albums_list():
    # albums_list.json 파일을 읽어서 반환
    try:
        with open(output_json_path, 'r', encoding='utf-8') as json_file:
            album_json = json.load(json_file)  # JSON 파일 읽기
        return jsonify(album_json)  # JSON 형식으로 반환
    except FileNotFoundError:
        return jsonify({"error": "Albums list not found"}), 404 #에러시 404 표시

@app.route("/audio/duration/<filename>", methods=["GET"])
def get_duration(filename):
    """
    특정 음원 파일의 총 길이를 반환하는 API.
    """
    # 파일 정보 찾기
    file_info = next((f for f in shuffled_audio_files if os.path.basename(f["path"]) == filename), None)

    if not file_info or not os.path.exists(file_info["path"]):
        return jsonify({"error": "File not found"}), 404

    # 음원 파일 길이 가져오기
    file_duration = get_audio_duration(file_info["path"])
    if file_duration is None:
        return jsonify({"error": "Could not retrieve duration"}), 500

    # 길이를 JSON 형식으로 반환
    return jsonify({"filename": filename, "duration": file_duration})



    return "File not found", 404
app.config['SESSION_COOKIE_SECURE'] = False # HTTPS에서만 세션 쿠키 전송
app.config['SESSION_COOKIE_HTTPONLY'] = False # JavaScript에서 세션 쿠키 접근 불가
#이렇게 설정하면 세션 쿠키가 HTTPS 프로토콜을 사용하는 경우에만 전송되며, JavaScript를 통해 세션 쿠키에 접근할 수 없습니다.
#보안적으로는 좋고, 음악 재생에는 영향을 주지 않습니다.

# see: https://www.geeksforgeeks.org/command-line-arguments-in-python/
parser = argparse.ArgumentParser()

# `--debug` 추가 시 args.debug == True
parser.add_argument("--debug", action='store_true', help = "Debug Mode")

args = parser.parse_args()

initindex = 0
init_lock = threading.Lock()

def initialize():
    global initindex
    with init_lock:
        if initindex == 0:
            save_json_to_file(file_list_path, output_json_path)
            initindex = 1
if __name__ == "__main__":
    heartbeat_thread = threading.Thread(target=heartbeat_checker)
    heartbeat_thread.start()
    init_thread = threading.Thread(target=initialize, daemon=True)
    init_thread.start()
    app.run(host="0.0.0.0", debug=args.debug, threaded=True, port=8000)
