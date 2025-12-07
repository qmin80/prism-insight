"""
KIS API - 주식 현재가 조회 샘플 코드

[역할]
한국투자증권 Open API를 사용하여 주식 현재가를 조회하는 샘플 코드입니다.
실시간 시세가 필요한 경우 WebSocket API를 사용하는 것을 권장합니다.

[주요 기능]
1. 주식 현재가 조회
   - 종목 코드로 현재가 정보 조회
   - 시가, 고가, 저가, 종가, 거래량 등 포함
2. 시장 분류 지원
   - KRX (J), NXT (NX), 통합 (UN)

[호출 관계]
- 호출하는 모듈:
  * trading/kis_auth.py: KIS API 인증 및 호출

[주요 함수]
- inquire_price(): 주식 현재가 조회

[사용 예시]
    from trading.samples.inquire_price import inquire_price
    
    df = inquire_price(
        env_dv="demo",
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="005930"
    )
    print(df)
"""


import sys
import logging

import pandas as pd

sys.path.extend(['../..', '.'])
import kis_auth as ka

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내주식] 기본시세 > 주식현재가 시세[v1_국내주식-008]
##############################################################################################

# 상수 정의
API_URL = "/uapi/domestic-stock/v1/quotations/inquire-price"

def inquire_price(
    env_dv: str,  # [필수] 실전모의구분 (ex. real:실전, demo:모의)
    fid_cond_mrkt_div_code: str,  # [필수] 조건 시장 분류 코드 (ex. J:KRX, NX:NXT, UN:통합)
    fid_input_iscd: str  # [필수] 입력 종목코드 (ex. 종목코드 (ex 005930 삼성전자), ETN은 종목코드 6자리 앞에 Q 입력 필수)
) -> pd.DataFrame:
    """
    주식 현재가 시세 API입니다. 실시간 시세를 원하신다면 웹소켓 API를 활용하세요.

    ※ 종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
    https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info
    
    Args:
        env_dv (str): [필수] 실전모의구분 (ex. real:실전, demo:모의)
        fid_cond_mrkt_div_code (str): [필수] 조건 시장 분류 코드 (ex. J:KRX, NX:NXT, UN:통합)
        fid_input_iscd (str): [필수] 입력 종목코드 (ex. 종목코드 (ex 005930 삼성전자), ETN은 종목코드 6자리 앞에 Q 입력 필수)

    Returns:
        pd.DataFrame: 주식 현재가 시세 데이터
        
    Example:
        >>> df = inquire_price("real", "J", "005930")
        >>> print(df)
    """

    # 필수 파라미터 검증
    if env_dv == "" or env_dv is None:
        raise ValueError("env_dv is required (e.g. 'real:실전, demo:모의')")
    
    if fid_cond_mrkt_div_code == "" or fid_cond_mrkt_div_code is None:
        raise ValueError("fid_cond_mrkt_div_code is required (e.g. 'J:KRX, NX:NXT, UN:통합')")
    
    if fid_input_iscd == "" or fid_input_iscd is None:
        raise ValueError("fid_input_iscd is required (e.g. '종목코드 (ex 005930 삼성전자), ETN은 종목코드 6자리 앞에 Q 입력 필수')")

    # tr_id 설정
    if env_dv == "real":
        tr_id = "FHKST01010100"
    elif env_dv == "demo":
        tr_id = "FHKST01010100"
    else:
        raise ValueError("env_dv can only be 'real' or 'demo'")

    params = {
        "FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code,
        "FID_INPUT_ISCD": fid_input_iscd
    }
    
    res = ka._url_fetch(API_URL, tr_id, "", params)
    
    if res.isOK():
        current_data = pd.DataFrame(res.getBody().output, index=[0])
        return current_data
    else:
        res.printError(url=API_URL)
        return pd.DataFrame() 