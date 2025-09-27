import subprocess
import threading
import random
import time
from flask import Flask, render_template, Response, send_file, request, redirect, url_for, session, flash, jsonify
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
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
FNAME_INDEX = {}
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


def extract_album_cover(file_path):
    try:
        audio = File(file_path)
        image_data = None

        # MP3 (ID3 태그)
        if file_path.lower().endswith(".mp3"):
            tags = ID3(file_path)
            for tag in tags.values():
                if tag.FrameID == "APIC":  # Album Picture
                    image_data = tag.data
                    break

        # M4A / MP4 (iTunes)
        elif file_path.lower().endswith((".m4a", ".mp4")):
            tags = MP4(file_path).tags
            if "covr" in tags:
                image_data = tags["covr"][0]

        # 이미지가 있으면 BytesIO로 감싸서 반환
        if image_data:
            buf = io.BytesIO(image_data)
            buf.seek(0)
            return buf

    except Exception as e:
        print(f"extract_album_cover error: {e}")

    return None


@app.route("/public/none")
def error_album_cover():
    # 1x1 투명 PNG 생성 (placeholder)
    image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="PNG")
    image_byte_array.seek(0)
    return send_file(image_byte_array, mimetype="image/png")

# 앨범 커버를 제공하는 라우트
@app.route("/cover/<filename>")
def get_album_cover(filename):
    file_info = next((f for f in shuffled_audio_files if os.path.basename(f["path"]) == filename), None)
    if file_info and os.path.exists(file_info["path"]):
        image = extract_album_cover(file_info["path"])
        if image:
            return send_file(image, mimetype="image/png")

    # fallback: 준비된 none.png 반환
    return send_file("static/none.png", mimetype="image/png")

    
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

from flask import Response, request
from urllib.parse import unquote
import unicodedata
import re
import os, subprocess, time

def _norm_name(s: str) -> str:
    # URL 디코드 → 유니코드 NFC 정규화 → 연속 공백 1개로
    s = unquote(s)
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

from flask import request

@app.route("/audio/<path:filename>")
def stream_audio(filename):
    filename_norm = _norm_name(filename).lower()

    selected_effects = request.args.get('effects', '') or ''
    filter_string = ''
    if 'echo' in selected_effects:
        filter_string += 'aecho=0.8:0.9:1000:0.3'

    manage_process_list()
    if len(process_list) >= max_processes:
        return "Maximum number of processes running. Try again later.", 429

    # 1차: 인덱스 조회
    file_info = FNAME_INDEX.get(filename_norm)

    # 2차: 폴백 선형 탐색(인덱스 미구축/미스매치 대비)
    if not file_info:
        for f in shuffled_audio_files:
            base = _norm_name(os.path.basename(f["path"])).lower()
            if base == filename_norm:
                file_info = f
                break

    if not file_info or not os.path.exists(file_info["path"]):
        return "File not found", 404

    # UA 확인 (아이폰/아이패드면 ALAC로)
    ua = request.headers.get("User-Agent", "").lower()
    if "iphone" in ua or "ipad" in ua or "macintosh" in ua:
        mimetype = "audio/wav"
        ffmpeg_cmd = [
            "ffmpeg", "-i", os.path.abspath(file_info["path"]),
            "-c:a", "pcm_s16le", "-f", "wav", "-"
        ]
        print("iOS or macOS device detected, using WAV format", flush=True)
    else:
        mimetype = "audio/flac"
        ffmpeg_cmd = [
            "ffmpeg", "-i", os.path.abspath(file_info["path"]),
            "-map", "0:a", "-c:a", "flac", "-f", "flac", "-"
        ]
        print("Non-iOS device detected, using FLAC format", flush=True)

    # 공통 옵션 추가
    cpu_count = os.cpu_count() or 1
    threads = str(max(1, cpu_count // 2))
    ffmpeg_cmd.extend(["-threads", threads])

    if filter_string:
        ffmpeg_cmd.extend(["-af", filter_string])

    def generate():
        current_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_list.append((current_process, time.time()))
        try:
            while True:
                chunk = current_process.stdout.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
                # last_access 갱신
                for i, (proc, last_access) in enumerate(process_list):
                    if proc == current_process:
                        process_list[i] = (proc, time.time())
            remaining = current_process.stdout.read()
            while remaining:
                yield remaining
                remaining = current_process.stdout.read()
        finally:
            if current_process.stdout:
                current_process.stdout.close()
            current_process.wait()
            if current_process.stderr:
                err = current_process.stderr.read().decode(errors="ignore")
                if current_process.returncode != 0:
                    print(f"FFmpeg error (Exit Code {current_process.returncode}): {err}")
                current_process.stderr.close()
            manage_process_list()

    resp = Response(generate(), mimetype=mimetype)
    resp.headers['Cache-Control'] = 'public, max-age=3600'
    return resp





@app.route("/albums_list", methods=["GET"])
def albums_list():
    # albums_list.json 파일을 읽어서 반환
    try:
        with open(output_json_path, 'r', encoding='utf-8') as json_file:
            album_json = json.load(json_file)  # JSON 파일 읽기
        return jsonify(album_json)  # JSON 형식으로 반환
    except FileNotFoundError:
        return jsonify({"error": "Albums list not found"}), 404 #에러시 404 표시

@app.route("/audio/duration/<path:filename>", methods=["GET"])
def get_duration(filename):
    """
    특정 음원 파일의 총 길이를 반환하는 API.
    stream_audio와 동일한 정규화/매칭 로직을 사용.
    """
    filename_norm = _norm_name(filename).lower()

    # 1차: 인덱스 조회
    file_info = FNAME_INDEX.get(filename_norm)

    # 2차: 폴백 선형 탐색
    if not file_info:
        for f in shuffled_audio_files:
            base = _norm_name(os.path.basename(f["path"])).lower()
            if base == filename_norm:
                file_info = f
                break

    if not file_info or not os.path.exists(file_info["path"]):
        return jsonify({"error": "File not found"}), 404

    file_duration = get_audio_duration(file_info["path"])
    if file_duration is None:
        return jsonify({"error": "Could not retrieve duration"}), 500

    return jsonify({"filename": os.path.basename(file_info["path"]), "duration": file_duration})

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
            for f in shuffled_audio_files:
                base = _norm_name(os.path.basename(f["path"])).lower()
                FNAME_INDEX[base] = f
            initindex = 1
if __name__ == "__main__":
    heartbeat_thread = threading.Thread(target=heartbeat_checker)
    heartbeat_thread.start()
    init_thread = threading.Thread(target=initialize, daemon=True)
    init_thread.start()
    app.run(host="0.0.0.0", debug=args.debug, threaded=True, port=8000)
