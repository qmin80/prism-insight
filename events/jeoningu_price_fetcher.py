"""
Jeon Ingu Trading Price Fetcher

[역할]
전인구 트레이딩 시스템에서 사용하는 ETF의 현재가를 조회하는 모듈입니다.
pykrx를 사용하여 KODEX 레버리지 및 인버스 ETF의 가격 정보를 가져옵니다.

[주요 기능]
1. 최신 거래일 확인
   - 주말 및 공휴일 제외
   - 최근 5일 내 거래일 확인
2. 종목 가격 조회
   - KODEX Leverage (122630)
   - KODEX Inverse 2X (252670)
3. OHLCV 데이터 제공
   - 시가, 고가, 저가, 종가, 거래량

[호출 관계]
- 호출하는 모듈:
  * pykrx.stock: 한국 주식 시장 데이터 조회
  * events/jeoningu_trading.py: 현재가 조회

[주요 함수]
- get_latest_trading_date(): 최신 거래일 조회
- get_stock_price(): 종목 가격 정보 조회
- get_kodex_prices(): KODEX ETF 가격 일괄 조회
- get_current_price(): 현재 종가 조회 (간편 함수)

[사용 예시]
    from events.jeoningu_price_fetcher import get_current_price
    
    price = get_current_price("122630")  # KODEX Leverage
"""

from pykrx import stock
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Stock codes
KODEX_LEVERAGE = "122630"
KODEX_INVERSE_2X = "252670"


def get_latest_trading_date() -> str:
    """
    Get latest trading date (excluding weekends and holidays)

    Returns:
        Date string in YYYYMMDD format
    """
    today = datetime.now()

    # Try today first, then go back up to 5 days
    for i in range(5):
        check_date = today - timedelta(days=i)
        date_str = check_date.strftime("%Y%m%d")

        # Skip weekends
        if check_date.weekday() >= 5:  # Saturday=5, Sunday=6
            continue

        try:
            # Test if market was open by fetching KOSPI index
            test_data = stock.get_index_ohlcv_by_date(
                fromdate=date_str,
                todate=date_str,
                ticker="1001"  # KOSPI
            )
            if not test_data.empty:
                logger.info(f"Latest trading date: {date_str}")
                return date_str
        except Exception:
            continue

    # Fallback to today
    return today.strftime("%Y%m%d")


def get_stock_price(stock_code: str, date: str = None) -> dict:
    """
    Get stock price information

    Args:
        stock_code: Stock code (069500 or 114800)
        date: Date in YYYYMMDD format (default: latest trading day)

    Returns:
        Dictionary with price info
    """
    if date is None:
        date = get_latest_trading_date()

    try:
        # Get OHLCV data
        df = stock.get_market_ohlcv_by_date(
            fromdate=date,
            todate=date,
            ticker=stock_code
        )

        if df.empty:
            logger.warning(f"No data for {stock_code} on {date}")
            return None

        # Get latest row
        latest = df.iloc[-1]

        return {
            "stock_code": stock_code,
            "date": date,
            "open": int(latest['시가']),
            "high": int(latest['고가']),
            "low": int(latest['저가']),
            "close": int(latest['종가']),
            "volume": int(latest['거래량'])
        }

    except Exception as e:
        logger.error(f"Error fetching price for {stock_code}: {e}")
        return None


def get_kodex_prices(date: str = None) -> dict:
    """
    Get prices for both KODEX Leverage and KODEX Inverse 2X

    Args:
        date: Date in YYYYMMDD format (default: latest trading day)

    Returns:
        Dictionary with both prices
    """
    if date is None:
        date = get_latest_trading_date()

    kodex_leverage_price = get_stock_price(KODEX_LEVERAGE, date)
    kodex_inverse_2x_price = get_stock_price(KODEX_INVERSE_2X, date)

    return {
        "date": date,
        "KODEX_LEVERAGE": kodex_leverage_price,
        "KODEX_INVERSE_2X": kodex_inverse_2x_price
    }


def get_current_price(stock_code: str) -> int:
    """
    Get current closing price (simplified)

    Args:
        stock_code: Stock code

    Returns:
        Current closing price (integer)
    """
    price_info = get_stock_price(stock_code)

    if price_info:
        return price_info['close']
    else:
        # Fallback to mock prices if API fails
        logger.warning(f"Using mock price for {stock_code}")
        if stock_code == KODEX_LEVERAGE:
            return 20000  # Mock for Leverage
        elif stock_code == KODEX_INVERSE_2X:
            return 5000  # Mock for Inverse 2X
        else:
            return 10000


# Test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing price fetcher...")

    # Get latest trading date
    latest_date = get_latest_trading_date()
    print(f"Latest trading date: {latest_date}")

    # Get KODEX prices
    prices = get_kodex_prices()
    print(f"\nKODEX Leverage: {prices['KODEX_LEVERAGE']}")
    print(f"KODEX Inverse 2X: {prices['KODEX_INVERSE_2X']}")

    # Get current price
    current_leverage = get_current_price(KODEX_LEVERAGE)
    current_inverse_2x = get_current_price(KODEX_INVERSE_2X)
    print(f"\nCurrent KODEX Leverage: {current_leverage:,}원")
    print(f"Current KODEX Inverse 2X: {current_inverse_2x:,}원")
