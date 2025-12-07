# PRISM-INSIGHT 코드 구조 및 호출 관계

> **작성일**: 2025-12-05  
> **목적**: 프로젝트의 모든 파일 설명 및 호출 관계 정리

---

## 목차

1. [파일 구조 개요](#파일-구조-개요)
2. [호출 관계 다이어그램](#호출-관계-다이어그램)
3. [파일별 상세 설명](#파일별-상세-설명)
4. [모듈 간 의존성](#모듈-간-의존성)

---

## 파일 구조 개요

```
prism-insight/
├── 📂 메인 엔트리 포인트
│   ├── stock_analysis_orchestrator.py    # 전체 파이프라인 오케스트레이터
│   ├── trigger_batch.py                   # 급등주 포착 배치
│   ├── stock_tracking_agent.py           # 매매 시뮬레이션 (기본)
│   ├── stock_tracking_enhanced_agent.py  # 매매 시뮬레이션 (향상)
│   ├── telegram_ai_bot.py                # 텔레그램 AI 봇
│   └── run_telegram_pipeline.py          # 텔레그램 파이프라인 실행
│
├── 📂 cores/ (핵심 분석 엔진)
│   ├── analysis.py                        # 종합 분석 오케스트레이션
│   ├── main.py                            # 분석 실행 진입점
│   ├── report_generation.py               # 리포트 생성 및 템플릿
│   ├── stock_chart.py                     # 차트 생성
│   ├── language_config.py                 # 다국어 설정
│   ├── utils.py                           # 유틸리티 함수
│   └── 📂 agents/                         # AI 에이전트 정의
│       ├── __init__.py                    # 에이전트 디렉토리 팩토리
│       ├── company_info_agents.py         # 재무/사업 분석 에이전트
│       ├── stock_price_agents.py          # 기술적 분석 에이전트
│       ├── news_strategy_agents.py       # 뉴스/전략 에이전트
│       ├── market_index_agents.py         # 시장 분석 에이전트
│       ├── trading_agents.py               # 매매 의사결정 에이전트
│       ├── telegram_summary_optimizer_agent.py   # 요약 최적화
│       ├── telegram_summary_evaluator_agent.py    # 품질 평가
│       └── telegram_translator_agent.py          # 번역 에이전트
│
├── 📂 trading/ (자동매매 시스템)
│   ├── domestic_stock_trading.py          # KIS API 래퍼
│   ├── kis_auth.py                        # KIS 인증 관리
│   └── portfolio_telegram_reporter.py    # 포트폴리오 리포트
│
├── 📂 텔레그램 관련
│   ├── telegram_config.py                # 텔레그램 설정 관리
│   ├── telegram_bot_agent.py             # 봇 메시지 처리
│   └── telegram_summary_agent.py         # 요약 생성 파이프라인
│
├── 📂 유틸리티
│   ├── check_market_day.py               # 장 휴장일 검증
│   ├── pdf_converter.py                  # PDF 변환
│   ├── analysis_manager.py               # 백그라운드 작업 큐
│   └── update_stock_data.py              # 주식 데이터 업데이트
│
└── 📂 events/ (이벤트 처리)
    ├── jeoningu_trading.py                # 전인구 트레이딩
    ├── jeoningu_trading_db.py             # 전인구 DB 관리
    └── jeoningu_price_fetcher.py         # 가격 조회
```

---

## 호출 관계 다이어그램

### 전체 시스템 흐름

```
[trigger_batch.py]
    ↓ (급등주 포착)
[stock_analysis_orchestrator.py]
    ├─→ [trigger_batch.py] (급등주 포착 실행)
    ├─→ [cores/analysis.py] (분석 리포트 생성)
    │   ├─→ [cores/agents/*.py] (각종 에이전트)
    │   ├─→ [cores/report_generation.py] (리포트 생성)
    │   └─→ [cores/stock_chart.py] (차트 생성)
    ├─→ [pdf_converter.py] (PDF 변환)
    ├─→ [telegram_summary_agent.py] (요약 생성)
    │   ├─→ [cores/agents/telegram_summary_optimizer_agent.py]
    │   └─→ [cores/agents/telegram_summary_evaluator_agent.py]
    ├─→ [telegram_bot_agent.py] (텔레그램 전송)
    └─→ [stock_tracking_enhanced_agent.py] (매매 시뮬레이션)
        ├─→ [cores/agents/trading_agents.py] (매매 의사결정)
        └─→ [trading/domestic_stock_trading.py] (실제 매매)
```

### 분석 엔진 상세 흐름

```
[cores/analysis.py]
    ↓
[cores/agents/__init__.py] (에이전트 팩토리)
    ↓
[각 섹션별 에이전트]
    ├─→ [cores/agents/stock_price_agents.py]
    │   ├─→ create_price_volume_analysis_agent()
    │   └─→ create_investor_trading_analysis_agent()
    ├─→ [cores/agents/company_info_agents.py]
    │   ├─→ create_company_status_agent()
    │   └─→ create_company_overview_agent()
    ├─→ [cores/agents/news_strategy_agents.py]
    │   └─→ create_news_analysis_agent()
    ├─→ [cores/agents/market_index_agents.py]
    │   └─→ create_market_index_analysis_agent()
    └─→ [cores/agents/trading_agents.py]
        ├─→ create_trading_scenario_agent()
        └─→ create_sell_decision_agent()
    ↓
[cores/report_generation.py]
    ├─→ generate_report() (각 섹션 리포트 생성)
    ├─→ generate_summary() (요약 생성)
    ├─→ generate_investment_strategy() (투자 전략 생성)
    └─→ generate_market_report() (시장 리포트 생성)
```

### 매매 시뮬레이션 흐름

```
[stock_tracking_enhanced_agent.py]
    ├─→ [cores/agents/trading_agents.py]
    │   └─→ create_trading_scenario_agent() (매수 시나리오 생성)
    ├─→ [stock_holdings 테이블] (보유 종목 조회/업데이트)
    ├─→ [cores/agents/trading_agents.py]
    │   └─→ create_sell_decision_agent() (매도 결정)
    └─→ [trading/domestic_stock_trading.py] (실제 매매 실행)
        └─→ [trading/kis_auth.py] (인증)
```

### 텔레그램 파이프라인 흐름

```
[telegram_summary_agent.py]
    ├─→ [cores/agents/telegram_summary_optimizer_agent.py] (요약 생성)
    └─→ [cores/agents/telegram_summary_evaluator_agent.py] (품질 평가)
        ↓ (반복 개선)
[telegram_bot_agent.py]
    ├─→ [telegram_config.py] (설정 로드)
    └─→ [python-telegram-bot] (실제 전송)
```

---

## 파일별 상세 설명

### 메인 엔트리 포인트

#### `stock_analysis_orchestrator.py`
- **역할**: 전체 파이프라인을 조율하는 메인 오케스트레이터
- **주요 클래스**: `StockAnalysisOrchestrator`
- **주요 메서드**:
  - `run_full_pipeline()`: 전체 파이프라인 실행
  - `run_trigger_batch()`: 급등주 포착 실행
  - `generate_reports()`: 분석 리포트 생성
  - `convert_to_pdf()`: PDF 변환
  - `generate_telegram_messages()`: 텔레그램 메시지 생성
  - `send_telegram_messages()`: 텔레그램 전송
- **호출하는 모듈**:
  - `trigger_batch.py`
  - `cores/analysis.py`
  - `pdf_converter.py`
  - `telegram_summary_agent.py`
  - `telegram_bot_agent.py`
  - `stock_tracking_enhanced_agent.py`

#### `trigger_batch.py`
- **역할**: 거래량 급증, 갭 상승 등을 감지하여 관심종목 선별
- **주요 함수**:
  - `get_snapshot()`: 특정 거래일의 전체 종목 OHLCV 스냅샷
  - `detect_volume_surge()`: 거래량 급증 감지
  - `detect_gap_up()`: 갭 상승 감지
- **호출하는 모듈**:
  - `pykrx.stock.stock_api` (외부 라이브러리)

#### `stock_tracking_agent.py`
- **역할**: 기본 매매 시뮬레이션 에이전트
- **주요 클래스**: `StockTrackingAgent`
- **주요 메서드**:
  - `initialize()`: 데이터베이스 초기화
  - `run()`: 매매 시뮬레이션 실행
  - `_evaluate_buy_decision()`: 매수 결정 평가
- **호출하는 모듈**:
  - `cores/agents/trading_agents.py`
  - SQLite 데이터베이스

#### `stock_tracking_enhanced_agent.py`
- **역할**: 향상된 매매 시뮬레이션 에이전트 (기본 에이전트 확장)
- **주요 클래스**: `EnhancedStockTrackingAgent`
- **추가 기능**:
  - 시장 상황 분석
  - 관심종목 이력 추적
  - 보유 종목 매도 결정
- **호출하는 모듈**:
  - `cores/agents/trading_agents.py` (매수/매도 에이전트)
  - SQLite 데이터베이스

### 핵심 분석 엔진

#### `cores/analysis.py`
- **역할**: 13개 AI 에이전트를 조율하여 종합 분석 리포트 생성
- **주요 함수**: `analyze_stock()`
- **처리 흐름**:
  1. MCPApp 초기화
  2. 에이전트 디렉토리 가져오기
  3. 순차적으로 각 섹션 분석 (rate limit 고려)
  4. 투자 전략 생성 (모든 분석 통합)
  5. 최종 리포트 생성
- **호출하는 모듈**:
  - `cores/agents/__init__.py`
  - `cores/report_generation.py`
  - `cores/stock_chart.py`

#### `cores/main.py`
- **역할**: 분석 실행 진입점 (테스트/개별 실행용)
- **주요 함수**: `analyze_stock()` 직접 호출
- **호출하는 모듈**:
  - `cores/analysis.py`

#### `cores/report_generation.py`
- **역할**: 리포트 템플릿 및 생성 로직
- **주요 함수**:
  - `generate_report()`: 각 섹션 리포트 생성 (재시도 로직 포함)
  - `generate_summary()`: 요약 생성
  - `generate_investment_strategy()`: 투자 전략 생성
  - `generate_market_report()`: 시장 리포트 생성
- **호출하는 모듈**:
  - `mcp_agent` (LLM 호출)

#### `cores/stock_chart.py`
- **역할**: 주가 차트 생성 (matplotlib 기반)
- **주요 함수**:
  - `create_price_chart()`: 주가 차트
  - `create_trading_volume_chart()`: 거래량 차트
  - `create_market_cap_chart()`: 시가총액 추이
  - `create_fundamentals_chart()`: 재무 지표 차트
  - `get_chart_as_base64_html()`: Base64 인코딩된 HTML 생성
- **호출하는 모듈**:
  - `pykrx.stock.stock_api` (외부 라이브러리)
  - `matplotlib`, `seaborn`, `mplfinance`

#### `cores/agents/__init__.py`
- **역할**: 에이전트 팩토리 - 섹션별 에이전트 생성
- **주요 함수**: `get_agent_directory()`
- **생성하는 에이전트**:
  - `price_volume_analysis`: 기술적 분석
  - `investor_trading_analysis`: 거래동향 분석
  - `company_status`: 재무 분석
  - `company_overview`: 사업 분석
  - `news_analysis`: 뉴스 분석
  - `market_index_analysis`: 시장 분석

#### `cores/agents/stock_price_agents.py`
- **역할**: 주가 및 거래량 분석 에이전트
- **주요 함수**:
  - `create_price_volume_analysis_agent()`: 기술적 분석가
  - `create_investor_trading_analysis_agent()`: 거래동향 분석가
- **사용하는 MCP 서버**: `kospi_kosdaq`, `firecrawl`, `perplexity`

#### `cores/agents/company_info_agents.py`
- **역할**: 기업 정보 분석 에이전트
- **주요 함수**:
  - `create_company_status_agent()`: 재무 분석가
  - `create_company_overview_agent()`: 산업 분석가
- **사용하는 MCP 서버**: `kospi_kosdaq`, `firecrawl`, `perplexity`

#### `cores/agents/news_strategy_agents.py`
- **역할**: 뉴스 및 투자 전략 에이전트
- **주요 함수**:
  - `create_news_analysis_agent()`: 정보 분석가
  - `create_investment_strategy_agent()`: 투자 전략가
- **사용하는 MCP 서버**: `kospi_kosdaq`, `firecrawl`, `perplexity`

#### `cores/agents/market_index_agents.py`
- **역할**: 시장 및 거시경제 분석 에이전트
- **주요 함수**: `create_market_index_analysis_agent()`: 시장 분석가
- **특징**: 결과 캐싱 (동일 날짜 분석 재사용)

#### `cores/agents/trading_agents.py`
- **역할**: 매매 의사결정 에이전트
- **주요 함수**:
  - `create_trading_scenario_agent()`: 매수 전문가 (GPT-5.1)
  - `create_sell_decision_agent()`: 매도 전문가 (GPT-5.1)
- **사용하는 MCP 서버**: `kospi_kosdaq`, `sqlite`, `perplexity`, `time`

#### `cores/agents/telegram_summary_optimizer_agent.py`
- **역할**: 상세 리포트를 텔레그램 메시지로 요약
- **주요 함수**: `telegram_summary_optimizer_agent()`
- **제약**: 400자 내외

#### `cores/agents/telegram_summary_evaluator_agent.py`
- **역할**: 요약 메시지 품질 평가 및 개선 제안
- **주요 함수**: `telegram_summary_evaluator_agent()`
- **프로세스**: EXCELLENT 등급까지 반복 개선

#### `cores/agents/telegram_translator_agent.py`
- **역할**: 다국어 번역 에이전트
- **주요 함수**: `translate_telegram_message()`
- **지원 언어**: en, ja, zh, es, fr, de

### 자동매매 시스템

#### `trading/domestic_stock_trading.py`
- **역할**: 한국투자증권(KIS) API 래퍼
- **주요 클래스**: `AsyncTradingContext`
- **주요 메서드**:
  - `async_buy_stock()`: 매수 주문
  - `async_sell_stock()`: 매도 주문
  - `async_get_portfolio()`: 포트폴리오 조회
- **호출하는 모듈**:
  - `trading/kis_auth.py` (인증)

#### `trading/kis_auth.py`
- **역할**: KIS API 인증 및 토큰 관리
- **주요 함수**:
  - `get_access_token()`: 액세스 토큰 발급
  - `get_hashkey()`: 해시키 생성

#### `trading/portfolio_telegram_reporter.py`
- **역할**: 포트폴리오 상태를 텔레그램으로 리포트
- **주요 함수**: 포트폴리오 리포트 생성 및 전송

### 텔레그램 관련

#### `telegram_config.py`
- **역할**: 텔레그램 설정 관리 클래스
- **주요 클래스**: `TelegramConfig`
- **주요 기능**:
  - 환경 변수 로드
  - 다국어 채널 ID 관리
  - 설정 검증

#### `telegram_bot_agent.py`
- **역할**: 텔레그램 봇 메시지 처리
- **주요 클래스**: `TelegramBotAgent`
- **주요 메서드**:
  - `send_message()`: 메시지 전송
  - `send_document()`: 파일 전송
  - `process_messages_directory()`: 디렉토리 내 메시지 일괄 처리

#### `telegram_summary_agent.py`
- **역할**: 리포트를 텔레그램 요약으로 변환하는 파이프라인
- **주요 클래스**: `TelegramSummaryGenerator`
- **주요 메서드**: `process_report()`
- **호출하는 모듈**:
  - `cores/agents/telegram_summary_optimizer_agent.py`
  - `cores/agents/telegram_summary_evaluator_agent.py`

#### `telegram_ai_bot.py`
- **역할**: 텔레그램 AI 봇 (Claude Sonnet 4.5 기반)
- **주요 기능**: 사용자 포트폴리오 상담

### 유틸리티

#### `check_market_day.py`
- **역할**: 한국 주식시장 영업일 검증
- **주요 함수**: `is_market_day()`
- **검증 항목**: 주말, 공휴일, 특별 휴일

#### `pdf_converter.py`
- **역할**: 마크다운을 PDF로 변환
- **지원 방법**: Playwright (권장), pdfkit, reportlab, mdpdf
- **주요 함수**: `markdown_to_pdf()`

#### `analysis_manager.py`
- **역할**: 백그라운드 작업 큐 관리
- **주요 기능**: 비동기 분석 작업 스케줄링

#### `update_stock_data.py`
- **역할**: 주식 데이터 업데이트 유틸리티

### 이벤트 처리

#### `events/jeoningu_trading.py`
- **역할**: 전인구 유튜브 채널 분석 기반 역추세 매매
- **주요 기능**:
  - RSS 피드 모니터링
  - 오디오 추출 및 전사
  - AI 기반 감정 분석
  - 역추세 매매 시뮬레이션
- **호출하는 모듈**:
  - `events/jeoningu_trading_db.py`
  - `events/jeoningu_price_fetcher.py`

#### `events/jeoningu_trading_db.py`
- **역할**: 전인구 트레이딩 데이터베이스 관리
- **주요 클래스**: `JeoninguTradingDB`
- **테이블**: `jeoningu_trades`

#### `events/jeoningu_price_fetcher.py`
- **역할**: ETF 가격 조회

---

## 모듈 간 의존성

### 핵심 의존성

```
stock_analysis_orchestrator.py
    ├─→ trigger_batch.py
    ├─→ cores/analysis.py
    │   ├─→ cores/agents/__init__.py
    │   │   ├─→ cores/agents/stock_price_agents.py
    │   │   ├─→ cores/agents/company_info_agents.py
    │   │   ├─→ cores/agents/news_strategy_agents.py
    │   │   └─→ cores/agents/market_index_agents.py
    │   ├─→ cores/report_generation.py
    │   └─→ cores/stock_chart.py
    ├─→ pdf_converter.py
    ├─→ telegram_summary_agent.py
    │   ├─→ cores/agents/telegram_summary_optimizer_agent.py
    │   └─→ cores/agents/telegram_summary_evaluator_agent.py
    ├─→ telegram_bot_agent.py
    │   └─→ telegram_config.py
    └─→ stock_tracking_enhanced_agent.py
        ├─→ cores/agents/trading_agents.py
        └─→ trading/domestic_stock_trading.py
            └─→ trading/kis_auth.py
```

### 외부 의존성

- **mcp-agent**: AI 에이전트 프레임워크
- **pykrx**: 한국 주식시장 데이터
- **python-telegram-bot**: 텔레그램 봇
- **playwright**: PDF 변환
- **matplotlib/seaborn/mplfinance**: 차트 생성
- **aiosqlite**: 비동기 SQLite

---

## 데이터 흐름

### 분석 리포트 생성 흐름

```
1. trigger_batch.py
   → 급등주 포착
   → JSON 결과 파일 생성

2. stock_analysis_orchestrator.py
   → trigger_batch.py 실행
   → 결과 파일 읽기
   → 종목 리스트 추출

3. cores/analysis.py
   → 각 종목별로 analyze_stock() 호출
   → 13개 에이전트 순차 실행
   → 섹션별 리포트 생성
   → 투자 전략 생성
   → 최종 리포트 조합

4. pdf_converter.py
   → 마크다운 → PDF 변환

5. telegram_summary_agent.py
   → PDF 읽기
   → 요약 생성 (최적화 + 평가 반복)
   → 텍스트 파일 저장

6. telegram_bot_agent.py
   → 메시지 파일 읽기
   → 텔레그램 전송
   → PDF 파일 전송

7. stock_tracking_enhanced_agent.py
   → PDF 리포트 읽기
   → 매수 결정 평가
   → 포트폴리오 업데이트
   → 매도 결정 평가
```

### 매매 시뮬레이션 흐름

```
1. stock_tracking_enhanced_agent.py
   → PDF 리포트 읽기
   → trading_agents.create_trading_scenario_agent() 호출
   → 매수 점수 평가 (1-10점)
   → 포트폴리오 제약 확인
   → 매수 결정

2. trading/domestic_stock_trading.py
   → KIS API 인증
   → 매수 주문 실행
   → 결과 반환

3. stock_tracking_enhanced_agent.py
   → stock_holdings 테이블 업데이트
   → 보유 종목 모니터링
   → trading_agents.create_sell_decision_agent() 호출
   → 매도 결정

4. trading/domestic_stock_trading.py
   → 매도 주문 실행
   → trading_history 테이블 업데이트
```

---

## 주요 패턴 및 컨벤션

### 1. 비동기 패턴
- 모든 I/O 작업은 `async/await` 사용
- `asyncio.create_subprocess_exec()` 사용 (외부 프로세스 실행)

### 2. 에러 처리
- `tenacity` 라이브러리로 재시도 로직 구현
- Graceful degradation (일부 실패해도 계속 진행)

### 3. 로깅
- 모든 모듈에서 `logging` 사용
- 파일 및 콘솔 동시 출력

### 4. 설정 관리
- `TelegramConfig` 클래스로 텔레그램 설정 중앙화
- 환경 변수 기반 설정

### 5. 데이터베이스
- SQLite 사용 (비동기: `aiosqlite`)
- 테이블 자동 생성 (`CREATE TABLE IF NOT EXISTS`)

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-12-05

