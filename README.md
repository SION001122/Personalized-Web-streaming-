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

모든 플랫폼에서 사용하기를 바라기 때문에 ffmpeg은 첨부하지 않았습니다. 따라서 ffmpeg를 아래의 링크에서 설치 후 사용해주시기를 바랍니다.
https://ffmpeg.org/
여기서 다운로드 가능합니다.
윈도우 기준으로 기본 설치경로로 다운 및 설치가 완료 되었다면
내 PC -> 오른쪽 마우스 클릭 -> 속성 -> 고급 시스템 설정 -> 고급 -> 환경 변수 -> 사용자 변수에서 path -> 편집 -> 새로 만들기 -> 설치 경로/bin을 입력 -> 확인 이 순서로 진행됩니다.
요청이 많다면 조만간 윈도우 전용 브랜치를 하나 만들어 ffmpeg.exe를 추가한 브랜치를 하나 만들도록 하겠습니다.

reader.py 를 실행하면 해당 디렉토리가 생성되고, 그 디렉토리에 음원파일을 넣은 후 다시 reader.py를 실행하면 쉽게 오디오 파일 리스트를 추가할 수 있습니다.

그리고 여러분의 기여도 받고 있습니다¡ 기여자가 되어보세요¡

ａｏｕｄｉｏ（오타지만 그냥 두기로 함。）앱의 사용지침입니다。
"도메인이 HTTPS를 지원하고 그렇게 설정되어 있다면, **https://**로 시작하는 주소 형식(예: https://example.com)을 사용하세요. 그렇지 않은 경우 프로토콜 없이 주소만 입력하셔도 됩니다(예: example.com). Aoudio 앱이 자동으로 ｈｔｔｐ로 처리합니다."

----2024-12-02 apk파일과 index.html파일의 추가사항.
양쪽 다 가져다 써 주시면 자동재생을 지원합니다. 


-----------2024-12-03-------------
apk 파일을 삭제하고 다시 설치하면 자동재생부터 잘 재생됩니다.

-----------2024-12-04-------------
app과 index.html 수정으로 인해 보다 지연시간이 줄어들었음.(대부분의 경우에서 잘 동작)

-----------2024-12-04-20:13 20🕥 기준 -------------
app과 index.html 수정으로 인해 보다 지연시간이 줄어들었음.(대부분의 경우에서 잘 동작)
이제 지연이 거의 없습니다.
app으로 시작하는 파일과 index.html을 덮어씌우고, apk파일 폰에서 업데이트 시키면 잘 됩니다.



8000번 포트를 윈도우상에서 열지 못 하는 분들을 위한 cmd파일이 나왔습니다. 관리자 권한으로 실행을 해서 간편하게 8000번 포트를 열어보세요.

 
추가. app(comment_kr).py와 aoudio.apk파일이 업데이트 되었습니다. index.html파일이까지도 교체 해 주세요. 이제 넘어가지기는 합니다.


bat파일이 추가되었습니다. 이제 윈도우에서 간단하게 실행할 수 있게 되었습니다.
(전부 관리자 권한으로 실행 하면 편합니다.)


1.reader.bat 을 실행해서 폴더를 하나 실행합니다.

2.8000port.bat 으로 방화벽에서 8000번 포트를 허용합니다.

3.requirements.bat으로 필요한 패키지를 설치합니다.

4.Runapp.bat 으로 서버 실행 확인 후 종료

5. 1번에서 reader.bat를 실행했을 떄 나온 audio 디렉토리(폴더)에 음원 파일을 넣고 reader.bat를 실행하면 audio_file_list.txt에 등록됩니다. (수동으로 등록해도 무방합니다.)
   
6. Runapp.bat 으로 서버 실행 후 나온 ip:8000 이렇게 되어있는 주소로 접속해서 테스트
## Third-Party Libraries

This project uses the following third-party library:

- **[JFLAC](https://sourceforge.net/projects/jflac/)**: A Java library for FLAC decoding, licensed under the Apache License 2.0.  
  For more details, see [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
