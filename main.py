import os
import sys
import yt_dlp


def progress_hook(d: dict) -> None:
    """다운로드 및 변환 진행 상황을 실시간으로 콘솔에 출력하는 콜백 함수입니다."""
    status = d.get("status")

    if status == "downloading":
        # 진행률 문자열, 다운로드 속도, 남은 시간(ETA) 추출
        percent = d.get("_percent_str", "0.0%").strip()
        speed = d.get("_speed_str", "알 수 없음").strip()
        eta = d.get("_eta_str", "알 수 없음").strip()
        sys.stdout.write(f"\r[다운로드 중] 진행률: {percent} | 속도: {speed} | 남은 시간: {eta}   ")
        sys.stdout.flush()

    elif status == "finished":
        print("\n[다운로드 완료] 원본 오디오 추출 완료! FFmpeg를 사용하여 MP3로 변환을 시작합니다...")


def download_youtube_to_mp3(url: str, output_dir: str = "downloads", audio_quality: str = "192") -> bool:
    """
    유튜브 영상 URL에서 최고 음질 오디오를 추출하여 MP3 파일로 저장합니다.

    매개변수:
        url (str): 다운로드할 유튜브 영상 URL
        output_dir (str): MP3 파일이 저장될 폴더 경로 (기본값: 'downloads')
        audio_quality (str): MP3 비트레이트 품질 kbps (기본값: '192', 최대 '320' 권장)

    반환값:
        bool: 다운로드 및 변환 성공 여부
    """
    # 저장할 폴더가 존재하지 않으면 생성합니다.
    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp 옵션 설정
    ydl_opts = {
        # 최고 음질의 오디오 스트림만 선택
        "format": "bestaudio/best",
        # 저장될 파일 경로 및 이름 템플릿 (영상 제목.확장자)
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        # 재생목록이 포함된 링크라도 단일 영상만 다운로드하도록 설정 (실수로 전체 목록 다운로드 방지)
        "noplaylist": True,
        # 윈도우 파일명에 사용할 수 없는 특수문자 자동 치환
        "windowsfilenames": True,
        # 다운로드 진행률 표시 훅 등록
        "progress_hooks": [progress_hook],
        # FFmpeg를 이용한 MP3 변환 후처리기 설정
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality,
            }
        ],
        # 불필요한 경고 출력 최소화
        "quiet": True,
        "no_warnings": True,
    }

    try:
        print(f"\n[분석 중] 영상 정보를 가져오고 있습니다: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 영상 메타데이터 먼저 확인
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "알 수 없는 제목")
            duration = info.get("duration", 0)

            minutes, seconds = divmod(duration, 60)
            print(f"[변환 완료] 제목: {title} ({minutes}분 {seconds}초)")
            print(f"[저장 위치] {os.path.abspath(output_dir)} 폴더 내 '.mp3' 파일로 저장되었습니다.\n")
            return True

    except yt_dlp.utils.DownloadError as e:
        print(f"\n[오류] 유튜브 다운로드 중 문제가 발생했습니다. URL을 확인하거나 yt-dlp를 업데이트해 주세요.\n상세 내용: {e}\n")
        return False
    except Exception as e:
        print(f"\n[예기치 않은 오류] {e}\n")
        return False


def main() -> None:
    """프로그램 메인 실행 루프입니다."""
    print("=" * 60)
    print(" 🎵 유튜브 MP3 추출기 (YouTube to MP3 Downloader)")
    print("=" * 60)

    # 명령줄 인자(CLI Argument)로 URL이 전달된 경우 즉시 처리 후 종료
    if len(sys.argv) > 1:
        target_url = sys.argv[1].strip()
        download_youtube_to_mp3(target_url)
        return

    # 대화형 입력 루프
    while True:
        try:
            user_input = input("유튜브 URL을 입력하세요 (종료하려면 'q' 또는 'exit' 입력): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n프로그램을 종료합니다.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("q", "exit", "quit", "종료"):
            print("프로그램을 종료합니다.")
            break

        download_youtube_to_mp3(user_input)


if __name__ == "__main__":
    main()
