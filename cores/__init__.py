"""
Cores Module

[역할]
PRISM-INSIGHT의 핵심 분석 엔진 모듈입니다.
AI 에이전트를 활용한 주식 분석, 보고서 생성, 차트 생성 등의 기능을 제공합니다.

[주요 모듈]
- analysis.py: 핵심 분석 엔진 (analyze_stock 함수)
- report_generation.py: 보고서 생성 모듈
- stock_chart.py: 차트 생성 모듈
- language_config.py: 다국어 설정 모듈
- agents/: AI 에이전트 생성 함수들
- utils.py: 유틸리티 함수

[사용 예시]
    from cores.analysis import analyze_stock
    
    report = await analyze_stock(
        company_code="005930",
        company_name="삼성전자",
        reference_date="20250101",
        language="ko"
    )
"""

