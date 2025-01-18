# 앱을 켜고 dac 연결 후  권한 확인 후 다른 앱을 사용 해 주세요!!! 이래야 바이패스가 제대로 적용이 됩니다!!!

# Personalized-Web-streaming-
Personalized Web streaming(개인화된 웹 스트리밍)


project_root/
│

├── templates/
│   └── index.html

│

├── app(comment_eng, kr).py   # Python source file with English and Korean comments

├── audio_file_list           # Text file storing audio paths

├── README(eng).md            # README file in English

├── README(kr).md             # README file in Korean



It has a structure like this.

이런 구조를 하고 있습니다.

need the flask library.

flask 라이브러리가 필요합니다.

pip install flask

python app.py

pip install flask를 한 후

python app.py를 하면 실행됩니다.

audio_file_list <-- 이 파일에 오디오의 경로를 넣어야 하는데, 

You need to add audio paths to the audio_file_list.

`1*file*C:\A\B\C\D\x_sound1.mp3`
형식은 `숫자*file*경로` 입니다. 

the format should be `number*file*path`. On the web

웹에서는 x_sound1이라는 이름만 표시됩니다. 

On the web, only x_sound1 will be displayed as the name.

audio_file_list에 예시도 하나 넣어놓았습니다. 

An example has been included in audio_file_list.

어떻게 쓰는지 알 것 같다면, 지우고 사용하시면 됩니다.

If you understand how to use it, feel free to delete the example and start using it.

activity_main.xml, AndroidManifest.xml, MainActivity.java 파일은 오디오 bypass의 예제를 보여줍니다. 원한다면 jflac 라이브러리를 안드로이드 스튜디오 프로젝트에 포함시켜 앱 형태로 이용할 수 있습니다.

The activity_main.xml, AndroidManifest.xml, and MainActivity.java files show examples of audio bypass. If you wish, you can include the jflac library in your Android Studio project and use it as an app.

reader.py 를 실행하면 해당 디렉토리가 생성되고, 그 디렉토리에 음원파일을 넣은 후 다시 reader.py를 실행하면 쉽게 오디오 파일 리스트를 추가할 수 있습니다.

그리고 여러분의 기여도 받고 있습니다¡ 기여자가 되어보세요¡

ａｏｕｄｉｏ（오타지만 그냥 두기로 함。）앱의 사용지침입니다。
"도메인이 HTTPS를 지원하고 그렇게 설정되어 있다면, **https://**로 시작하는 주소 형식(예: https://example.com)을 사용하세요. 그렇지 않은 경우 프로토콜 없이 주소만 입력하셔도 됩니다(예: example.com). Aoudio 앱이 자동으로 ｈｔｔｐ로 처리합니다."

# -----------2025-01-18-23:02🕥 기준 -------------
(기존 사용자 기준)

0.audio_file_list.txt를 백업 후 프로젝트를 다운받아 덮어씌워주세요 (audio_file_list.txt을 꼭 백업해야 편리합니다!!!!)

1.requstment.bat 다시 실행 후 Runapp.bat을 실행 시키면 정상 작동합니다.

(신규 사용자 기준은 아래의 설치 내용을 따라주세요.)

reader.bat 업데이트. 바로가기 파일 대응

# 신규 사용자 설치 가이드라인.

0.모든 플랫폼에서 사용하기를 바라기 때문에 ffmpeg은 첨부하지 않았습니다. 따라서 ffmpeg를 아래의 링크에서 설치 후 사용해주시기를 바랍니다.



여기서 다운로드 가능합니다. 여기는 권장하는 파이썬 버전입니다. Add python.exe to PATH 체크박스 체크 하시고 설치 하시면 됩니다.
[python3.10](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe)

윈도우 기준으로 기본 설치경로로 다운 및 설치가 완료 되었다면
이 파일을 다운받습니다.
[https://ffmpeg.org/](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)

내 PC -> C드라이브에 압축을 풀어줍니다. -> 내 PC에 오른쪽 마우스 클릭 -> 속성 -> 고급 시스템 설정 -> 고급 -> 환경 변수 -> 사용자 변수에서 path -> 편집 -> 새로 만들기 -> 설치 경로/bin을 입력 -> 확인 이 순서로 진행됩니다.

1.requirements.bat으로 필요한 패키지를 설치합니다.

2.reader.bat 을 실행해서 폴더를 하나 실행합니다.

3.8000port.bat 으로 방화벽에서 8000번 포트를 허용합니다.

5.Runapp.bat 으로 서버 실행 확인 후 종료

6. 1번에서 reader.bat를 실행했을 떄 나온 audio 디렉토리(폴더)에 음원 파일(바로가기를 만들어서 넣어도 무방)

을 넣고 reader.bat를 실행하면 audio_file_list.txt에 등록됩니다. (수동으로 등록해도 무방합니다.)
  
7. Runapp.bat 으로 서버 실행 후 나온 ip:8000 이렇게 되어있는 주소로 접속해서 테스트
   
8. 안드로이드 기기를 가지고 있는 경우 해당 레포지토리에서 apk파일을 받아다가 설치 후 꼬다리 dac 같은 외부 dac로 즐기면 바이패스가 가능합니다!
    
## Third-Party Libraries

This project uses the following third-party library:

- **[JFLAC](https://sourceforge.net/projects/jflac/)**: A Java library for FLAC decoding, licensed under the Apache License 2.0.  
  For more details, see [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
