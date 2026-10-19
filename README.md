# 🎵 Youtube2Mp3 (유튜브 MP3 추출기)

파이썬(`yt-dlp`)과 `FFmpeg`를 활용하여 유튜브 영상에서 최고 음질의 오디오를 추출하고 `.mp3` 파일로 변환해 주는 CLI 프로그램입니다.

---

## ⚠️ 주의사항
* 본 프로그램은 개인 학습 및 테스트 목적으로 제작되었습니다.
* 저작권이 있는 음원을 무단으로 배포하거나 상업적 용도로 사용할 경우 발생하는 법적 책임은 사용자 본인에게 있습니다.

---

## 🛠️ 사전 요구사항 (Prerequisites)

1. **Python 3.10 이상** 및 **`uv`** 패키지 매니저
2. **`FFmpeg` 설치 필수**
   * 유튜브의 원본 오디오 스트림(`.webm`, `.m4a`)을 `.mp3`로 변환하기 위해 시스템 환경변수(`PATH`)에 `ffmpeg`가 등록되어 있어야 합니다.
   * 설치 확인 (PowerShell):
     ```powershell
     ffmpeg -version
     ```

---

## 🚀 설치 방법 (Windows PowerShell)

```powershell
# 1. 저장소 클론 및 폴더 이동
git clone https://github.com/사용자아이디/Youtube2Mp3.git
cd Youtube2Mp3

# 2. uv 가상환경(.venv) 생성
uv venv .venv

# 3. 필수 패키지 설치
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

---

## 💻 사용 방법

### 1. 대화형 모드 실행 (연속 다운로드)
```powershell
.\.venv\Scripts\python.exe main.py
```
실행 후 콘솔 창에 유튜브 URL을 입력하면 `downloads/` 폴더에 자동으로 MP3 파일이 저장됩니다. 종료하려면 `q` 또는 `exit`를 입력하세요.

### 2. 단일 URL 즉시 다운로드
```powershell
.\.venv\Scripts\python.exe main.py "https://www.youtube.com/watch?v=영상ID"
```
