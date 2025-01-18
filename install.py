import subprocess
import sys

# 설치가 필요한 패키지 목록
required_packages = [
    Flask==2.2.5
    mutagen==1.46.0
    Pillow==10.0.0
    flask-compress==1.13
]

def install_packages(packages):
    for package in packages:
        try:
            # pip 명령어를 실행하여 패키지 설치
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                print(f"'{package}' 설치 성공!")
            else:
                print(f"'{package}' 설치 실패: {result.stderr}")
        except Exception as e:
            print(f"'{package}' 설치 중 에러 발생: {e}")

if __name__ == "__main__":
    # 패키지 설치 실행
    print("필요한 패키지 설치를 시작합니다...")
    install_packages(required_packages)
    print("모든 패키지 설치가 완료되었습니다!")
