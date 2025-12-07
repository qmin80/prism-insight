"""
GCP Pub/Sub Signal Publisher

[역할]
PRISM-INSIGHT의 매수/매도 신호를 Google Cloud Pub/Sub에 발행하는 모듈입니다.
GCP 인프라를 사용하는 경우 실시간으로 거래 신호를 구독자에게 전달할 수 있습니다.

[주요 기능]
1. 매수 신호 발행
   - 종목 코드, 회사명, 가격, 시나리오 정보 포함
2. 매도 신호 발행
   - 종목 코드, 매도 가격, 수익률 정보 포함
3. Google Cloud Pub/Sub 사용
   - 비동기 컨텍스트 매니저 지원
   - 서비스 계정 인증 지원

[호출 관계]
- 호출하는 모듈:
  * google.cloud.pubsub_v1: GCP Pub/Sub 클라이언트
  * stock_tracking_agent.py: 매수/매도 신호 발행

[주요 클래스]
- SignalPublisher: GCP Pub/Sub 신호 발행 클래스

[주요 메서드]
- publish_buy_signal(): 매수 신호 발행
- publish_sell_signal(): 매도 신호 발행
- connect(): Pub/Sub 연결
- disconnect(): Pub/Sub 연결 해제

[사용 예시]
    from messaging.gcp_pubsub_signal_publisher import SignalPublisher
    
    async with SignalPublisher() as publisher:
        await publisher.publish_buy_signal(
            ticker="005930",
            company_name="삼성전자",
            price=82000,
            scenario={"target_price": 90000, "stop_loss": 78000}
        )

[설정]
- GCP_PROJECT_ID: GCP 프로젝트 ID
- GCP_PUBSUB_TOPIC_ID: Pub/Sub 토픽 ID (기본값: "prism-trading-signals")
- GCP_CREDENTIALS_PATH: 서비스 계정 JSON 키 파일 경로
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Load .env file
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

logger = logging.getLogger(__name__)


class SignalPublisher:
    """GCP Pub/Sub-based trading signal publisher"""

    def __init__(
        self,
        project_id: Optional[str] = None,
        topic_id: Optional[str] = None,
        credentials_path: Optional[str] = None
    ):
        """
        Initialize SignalPublisher

        Args:
            project_id: GCP Project ID
            topic_id: Pub/Sub Topic ID
            credentials_path: Path to service account JSON key file
        """
        self.project_id = project_id or os.environ.get("GCP_PROJECT_ID")
        self.topic_id = topic_id or os.environ.get("GCP_PUBSUB_TOPIC_ID", "prism-trading-signals")
        self.credentials_path = credentials_path or os.environ.get("GCP_CREDENTIALS_PATH")
        self._publisher = None
        self._topic_path = None

        if not self.project_id:
            logger.warning(
                "GCP Project ID not configured. "
                "Set GCP_PROJECT_ID environment variable."
            )

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

    async def connect(self):
        """Connect to GCP Pub/Sub"""
        if not self.project_id:
            logger.warning("GCP not configured, signals will not be published")
            return

        try:
            from google.cloud import pubsub_v1

            # Set credentials if provided
            if self.credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

            self._publisher = pubsub_v1.PublisherClient()
            self._topic_path = self._publisher.topic_path(self.project_id, self.topic_id)
            logger.info(f"GCP Pub/Sub connected: {self._topic_path}")
        except ImportError:
            logger.warning(
                "google-cloud-pubsub package not installed. "
                "Install with: pip install google-cloud-pubsub"
            )
        except Exception as e:
            logger.error(f"GCP Pub/Sub connection failed: {str(e)}")
            self._publisher = None

    async def disconnect(self):
        """Disconnect from GCP Pub/Sub"""
        self._publisher = None
        self._topic_path = None
        logger.info("GCP Pub/Sub disconnected")

    def _is_connected(self) -> bool:
        """Check connection status"""
        return self._publisher is not None

    async def publish_signal(
        self,
        signal_type: str,
        ticker: str,
        company_name: str,
        price: float,
        source: str = "AI Analysis",
        scenario: Optional[Dict[str, Any]] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Publish trading signal

        Args:
            signal_type: Signal type ("BUY", "SELL", "EVENT", etc.)
            ticker: Stock ticker
            company_name: Company name
            price: Current/buy/sell price
            source: Signal source (default: "AI Analysis")
            scenario: Trading scenario information
            extra_data: Additional data

        Returns:
            str: Message ID (None on failure)
        """
        if not self._is_connected():
            logger.debug(f"GCP Pub/Sub not connected, skipping signal publish: {signal_type} {ticker}")
            return None

        try:
            # Build signal data
            signal_data = {
                "type": signal_type,
                "ticker": ticker,
                "company_name": company_name,
                "price": price,
                "source": source,
                "timestamp": datetime.now().isoformat(),
            }

            # Add scenario information (key fields only)
            if scenario:
                signal_data["target_price"] = scenario.get("target_price", 0)
                signal_data["stop_loss"] = scenario.get("stop_loss", 0)
                signal_data["investment_period"] = scenario.get("investment_period", "")
                signal_data["sector"] = scenario.get("sector", "")
                signal_data["rationale"] = scenario.get("rationale", "")
                signal_data["buy_score"] = scenario.get("buy_score", 0)

            # Merge additional data
            if extra_data:
                signal_data.update(extra_data)

            # Publish to GCP Pub/Sub
            message_json = json.dumps(signal_data, ensure_ascii=False)
            message_bytes = message_json.encode("utf-8")

            future = self._publisher.publish(self._topic_path, message_bytes)
            message_id = future.result()

            logger.info(
                f"Signal published: {signal_type} {company_name}({ticker}) "
                f"@ {price:,.0f} KRW [ID: {message_id}]"
            )
            return message_id

        except Exception as e:
            logger.error(f"Signal publish failed: {str(e)}")
            return None

    async def publish_buy_signal(
        self,
        ticker: str,
        company_name: str,
        price: float,
        scenario: Optional[Dict[str, Any]] = None,
        source: str = "AI Analysis",
        trade_result: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Publish buy signal

        Args:
            ticker: Stock ticker
            company_name: Company name
            price: Buy price
            scenario: Trading scenario
            source: Signal source
            trade_result: Actual trade result (success status, etc.)

        Returns:
            str: Message ID
        """
        extra_data = {}
        if trade_result:
            extra_data["trade_success"] = trade_result.get("success", False)
            extra_data["trade_message"] = trade_result.get("message", "")

        return await self.publish_signal(
            signal_type="BUY",
            ticker=ticker,
            company_name=company_name,
            price=price,
            source=source,
            scenario=scenario,
            extra_data=extra_data
        )

    async def publish_sell_signal(
        self,
        ticker: str,
        company_name: str,
        price: float,
        buy_price: float,
        profit_rate: float,
        sell_reason: str,
        trade_result: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Publish sell signal

        Args:
            ticker: Stock ticker
            company_name: Company name
            price: Sell price
            buy_price: Buy price
            profit_rate: Profit rate
            sell_reason: Sell reason
            trade_result: Actual trade result

        Returns:
            str: Message ID
        """
        extra_data = {
            "buy_price": buy_price,
            "profit_rate": profit_rate,
            "sell_reason": sell_reason,
        }

        if trade_result:
            extra_data["trade_success"] = trade_result.get("success", False)
            extra_data["trade_message"] = trade_result.get("message", "")

        return await self.publish_signal(
            signal_type="SELL",
            ticker=ticker,
            company_name=company_name,
            price=price,
            source="AI Analysis",
            extra_data=extra_data
        )

    async def publish_event_signal(
        self,
        ticker: str,
        company_name: str,
        price: float,
        event_type: str,
        event_source: str,
        event_description: str
    ) -> Optional[str]:
        """
        Publish event-based signal (YouTuber video, news, etc.)

        Args:
            ticker: Stock ticker
            company_name: Company name
            price: Current price
            event_type: Event type (e.g., "YOUTUBE", "NEWS", "DISCLOSURE")
            event_source: Event source (e.g., YouTuber name, news outlet)
            event_description: Event description

        Returns:
            str: Message ID
        """
        return await self.publish_signal(
            signal_type="EVENT",
            ticker=ticker,
            company_name=company_name,
            price=price,
            source=event_source,
            extra_data={
                "event_type": event_type,
                "event_description": event_description
            }
        )


# Global instance for convenience (optional usage)
_global_publisher: Optional[SignalPublisher] = None


async def get_signal_publisher() -> SignalPublisher:
    """Return global SignalPublisher instance"""
    global _global_publisher
    if _global_publisher is None:
        _global_publisher = SignalPublisher()
        await _global_publisher.connect()
    return _global_publisher


async def publish_buy_signal(
    ticker: str,
    company_name: str,
    price: float,
    scenario: Optional[Dict[str, Any]] = None,
    source: str = "AI Analysis",
    trade_result: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """Publish buy signal via global publisher (convenience function)"""
    publisher = await get_signal_publisher()
    return await publisher.publish_buy_signal(
        ticker=ticker,
        company_name=company_name,
        price=price,
        scenario=scenario,
        source=source,
        trade_result=trade_result
    )


async def publish_sell_signal(
    ticker: str,
    company_name: str,
    price: float,
    buy_price: float,
    profit_rate: float,
    sell_reason: str,
    trade_result: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """Publish sell signal via global publisher (convenience function)"""
    publisher = await get_signal_publisher()
    return await publisher.publish_sell_signal(
        ticker=ticker,
        company_name=company_name,
        price=price,
        buy_price=buy_price,
        profit_rate=profit_rate,
        sell_reason=sell_reason,
        trade_result=trade_result
    )
