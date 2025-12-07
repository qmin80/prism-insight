"""
Email Sender Module for Streamlit App

[역할]
분석 리포트를 이메일로 전송하는 모듈입니다.
마크다운 리포트를 HTML로 변환하여 이메일 본문으로 사용하고, 원본 마크다운과 HTML 파일을 첨부합니다.

[주요 기능]
1. 마크다운 → HTML 변환
   - GitHub 스타일 CSS 적용
   - 코드 블록, 테이블 등 마크다운 확장 지원
2. 이메일 전송
   - HTML 본문
   - 마크다운 파일 첨부
   - HTML 파일 첨부
3. SMTP 서버 연동
   - TLS 암호화 지원
   - Gmail, Outlook 등 주요 이메일 서비스 지원

[호출 관계]
- 호출하는 모듈:
  * smtplib: SMTP 서버 통신
  * markdown: 마크다운 파싱
  * config: SMTP 설정 (SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)

- 호출되는 모듈:
  * app_modern.py: 분석 완료 후 이메일 전송

[주요 함수]
- send_email(): 이메일 전송 메인 함수
- convert_md_to_html(): 마크다운을 HTML로 변환

[사용 예시]
    from email_sender import send_email
    
    success = send_email(
        to_email="user@example.com",
        report_content="# 분석 리포트\n\n내용..."
    )

[설정 요구사항]
- config.py 파일에 다음 변수 정의 필요:
  * SMTP_SERVER: SMTP 서버 주소 (예: "smtp.gmail.com")
  * SMTP_PORT: SMTP 포트 (예: 587)
  * SENDER_EMAIL: 발신자 이메일 주소
  * SENDER_PASSWORD: 발신자 이메일 비밀번호 (앱 비밀번호 권장)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.tables
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD

def convert_md_to_html(md_content: str) -> str:
    """마크다운을 HTML로 변환"""
    # GitHub 스타일의 CSS
    css = """
    <style>
        body { 
            font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 { color: #24292e; border-bottom: 1px solid #eaecef; }
        h2 { color: #24292e; border-bottom: 1px solid #eaecef; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
        th { background-color: #f6f8fa; }
        code { background-color: #f6f8fa; padding: 2px 4px; border-radius: 3px; }
        pre { background-color: #f6f8fa; padding: 16px; overflow: auto; border-radius: 3px; }
    </style>
    """

    # 마크다운을 HTML로 변환
    html = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc'
        ]
    )

    # 완성된 HTML 문서
    complete_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {css}
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    return complete_html

def send_email(to_email: str, report_content: str) -> bool:
    """이메일 전송 함수"""
    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = "주식 종목 분석 보고서"

        # 1. HTML 버전 (메인 컨텐츠)
        html_content = convert_md_to_html(report_content)
        msg.attach(MIMEText(html_content, 'html'))

        # 2. 마크다운 파일 첨부
        md_attachment = MIMEText(report_content, 'plain')
        md_attachment.add_header('Content-Disposition', 'attachment', filename='analysis_report.md')
        msg.attach(md_attachment)

        # 3. HTML 파일 첨부
        html_attachment = MIMEText(html_content, 'html')
        html_attachment.add_header('Content-Disposition', 'attachment', filename='analysis_report.html')
        msg.attach(html_attachment)

        # SMTP 서버 연결 및 로그인
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # 이메일 발송
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {str(e)}")
        return False