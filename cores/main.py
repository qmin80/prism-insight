"""
Stock Analysis Main Entry Point

[역할]
개별 종목 분석을 실행하는 진입점입니다.
테스트 및 개발 목적으로 특정 종목의 분석 리포트를 생성합니다.

[주요 기능]
- 특정 종목 코드와 회사명을 지정하여 분석 실행
- 60분 타임아웃 설정 (무한 실행 방지)
- 실행 시간 및 리포트 길이 출력

[호출 관계]
- 호출하는 모듈:
  * cores/analysis.py: analyze_stock() 함수 호출

[사용 예시]
    cd cores
    python main.py
    
    # 또는 직접 수정하여 다른 종목 분석
    result = asyncio.run(analyze_stock(
        company_code="005930",
        company_name="삼성전자",
        reference_date="20251205"
    ))

[주의사항]
- 하드코딩된 종목 코드를 수정하여 사용
- 프로덕션 환경에서는 stock_analysis_orchestrator.py 사용 권장
"""
import asyncio
import time
import threading
import os
import signal
from datetime import datetime

from cores.analysis import analyze_stock

if __name__ == "__main__":
    # 60분 후에 프로세스를 종료하는 타이머 함수
    def exit_after_timeout():
        time.sleep(3600)  # 60분 대기
        print("60분 타임아웃 도달: 프로세스 강제 종료")
        os.kill(os.getpid(), signal.SIGTERM)

    # 백그라운드 스레드로 타이머 시작
    timer_thread = threading.Thread(target=exit_after_timeout, daemon=True)
    timer_thread.start()

    start = time.time()

    # 특정 날짜를 기준으로 분석 실행
    result = asyncio.run(analyze_stock(company_code="036570", company_name="엔씨소프트", reference_date="20251202"))

    # 결과 저장
    with open(f"엔씨소프트_분석보고서_{datetime.now().strftime('%Y%m%d')}_gpt4_1.md", "w", encoding="utf-8") as f:
        f.write(result)

    end = time.time()
    print(f"총 실행 시간: {end - start:.2f}초")
    print(f"최종 보고서 길이: {len(result):,} 글자")
