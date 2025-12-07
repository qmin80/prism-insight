#!/usr/bin/env python3
"""
Stock Data Update Script

[역할]
KOSPI/KOSDAQ 종목 정보를 업데이트하는 스크립트입니다.
종목 코드와 종목명 매핑 정보를 JSON 파일로 저장합니다.

[주요 기능]
1. 종목 정보 수집
   - KOSPI 종목 목록 및 이름
   - KOSDAQ 종목 목록 및 이름
2. 데이터 변환
   - 코드 → 이름 매핑
   - 이름 → 코드 매핑
3. JSON 파일 저장
   - stock_map.json 파일 생성
   - 업데이트 시간 기록

[실행 방법]
    # 기본 실행
    python update_stock_data.py
    
    # 출력 파일 지정
    python update_stock_data.py --output custom_stock_map.json

[크론탭 등록 예시]
    # 매일 오전 9시 실행
    0 9 * * * cd /path/to/prism-insight && python update_stock_data.py

[출력 파일 형식]
    {
        "code_to_name": {
            "005930": "삼성전자",
            "000660": "SK하이닉스",
            ...
        },
        "name_to_code": {
            "삼성전자": "005930",
            "SK하이닉스": "000660",
            ...
        },
        "updated_at": "2025-01-01T09:00:00"
    }

[의존성]
- pykrx: 한국 주식 시장 데이터 조회
"""
import os
import json
import logging
import argparse
from datetime import datetime

try:
    from pykrx import stock
except ImportError:
    print("pykrx 패키지가 설치되어 있지 않습니다. 'pip install pykrx'로 설치하세요.")
    exit(1)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("stock_data_update.log")
    ]
)
logger = logging.getLogger(__name__)

def update_stock_data(output_file="stock_map.json"):
    """
    종목 정보 업데이트

    Args:
        output_file (str): 저장할 파일 경로

    Returns:
        bool: 성공 여부
    """
    try:
        # 오늘 날짜
        today = datetime.now().strftime("%Y%m%d")
        logger.info(f"종목 데이터 업데이트 시작: {today}")

        # KOSPI 종목 정보 가져오기
        kospi_tickers = stock.get_market_ticker_list(market="KOSPI")
        kospi_map = {ticker: stock.get_market_ticker_name(ticker) for ticker in kospi_tickers}
        logger.info(f"KOSPI 종목 {len(kospi_map)}개 로드")

        # KOSDAQ 종목 정보 가져오기
        kosdaq_tickers = stock.get_market_ticker_list(market="KOSDAQ")
        kosdaq_map = {ticker: stock.get_market_ticker_name(ticker) for ticker in kosdaq_tickers}
        logger.info(f"KOSDAQ 종목 {len(kosdaq_map)}개 로드")

        # 결합
        code_to_name = {**kospi_map, **kosdaq_map}
        name_to_code = {name: code for code, name in code_to_name.items()}

        # 데이터 저장
        data = {
            "code_to_name": code_to_name,
            "name_to_code": name_to_code,
            "updated_at": datetime.now().isoformat()
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"종목 데이터 업데이트 완료: {len(code_to_name)}개 종목, 파일: {output_file}")
        return True
    except Exception as e:
        logger.error(f"종목 데이터 업데이트 실패: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="종목 정보 업데이트")
    parser.add_argument("--output", default="stock_map.json", help="저장할 파일 경로")

    args = parser.parse_args()
    update_stock_data(args.output)

if __name__ == "__main__":
    main()