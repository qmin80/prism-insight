# PRISM-INSIGHT 온보딩 가이드

> **대상**: 주니어 개발자  
> **목적**: PRISM-INSIGHT 프로젝트 전반을 이해하고 개발을 시작할 수 있도록 돕기  
> **작성일**: 2025-12-05

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [시스템 아키텍처 이해](#2-시스템-아키텍처-이해)
3. [개발 환경 설정](#3-개발-환경-설정)
4. [핵심 컴포넌트 이해](#4-핵심-컴포넌트-이해)
5. [개발 워크플로우](#5-개발-워크플로우)
6. [실습 가이드](#6-실습-가이드)
7. [문제 해결 가이드](#7-문제-해결-가이드)
8. [다음 단계](#8-다음-단계)

---

## 1. 프로젝트 개요

### 1.1 PRISM-INSIGHT란?

PRISM-INSIGHT는 **AI 기반 한국 주식시장 분석 및 자동매매 시스템**입니다. 

**핵심 기능:**
- 🤖 **13개의 전문화된 AI 에이전트**가 협업하여 전문가 수준의 주식 분석 리포트 생성
- 📊 **급등주 자동 포착**: 거래량, 갭 상승, 시총 대비 거래대금 등을 분석하여 관심종목 선별
- 📈 **매매 시뮬레이션**: AI 리포트 기반으로 매수/매도 의사결정 및 포트폴리오 관리
- 💱 **자동매매**: 한국투자증권(KIS) API를 통한 실제 매매 실행
- 📱 **텔레그램 통합**: 분석 결과를 실시간으로 텔레그램 채널에 전송
- 🌐 **다국어 지원**: 한국어, 영어, 일본어, 중국어 등 다국어 리포트 생성

### 1.2 기술 스택

```
언어: Python 3.10+
AI 프레임워크: mcp-agent (Multi-Agent Orchestration)
LLM 모델:
  - OpenAI GPT-4.1 (분석 에이전트)
  - OpenAI GPT-5.1 (매매 시뮬레이션)
  - Anthropic Claude Sonnet 4.5 (텔레그램 봇)
데이터 소스:
  - pykrx: 한국 주식시장 데이터
  - MCP Servers: kospi_kosdaq, firecrawl, perplexity
통신: python-telegram-bot (v20+)
매매 API: 한국투자증권 API
데이터베이스: SQLite (aiosqlite)
PDF 생성: Playwright (Chromium 기반)
차트: matplotlib, seaborn, mplfinance
```

### 1.3 프로젝트 규모

- **약 56개의 Python 파일** | **8,400+ 줄의 코드**
- **13개의 전문화된 AI 에이전트**
- **완전한 비동기(async/await) 구조**
- **다국어 지원** (ko, en, ja, zh, es, fr, de)

---

## 2. 시스템 아키텍처 이해

### 2.1 전체 시스템 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    PRISM-INSIGHT 시스템                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌─────────────────┐   ┌─────────────┐ │
│  │   Trigger    │───▶│   Orchestrator  │──▶│   Analysis  │ │
│  │    Batch     │    │     Pipeline    │   │    Engine   │ │
│  └──────────────┘    └─────────────────┘   └─────────────┘ │
│         │                    │                      │        │
│         ▼                    ▼                      ▼        │
│  ┌──────────────┐    ┌─────────────────┐   ┌─────────────┐ │
│  │   Watchlist  │    │  13 AI Agents   │   │   Reports   │ │
│  │  Detection   │    │   Collaborate   │   │  (MD/PDF)   │ │
│  └──────────────┘    └─────────────────┘   └─────────────┘ │
│                              │                      │        │
│                              ▼                      ▼        │
│                      ┌─────────────────┐   ┌─────────────┐ │
│                      │    Trading      │   │  Telegram   │ │
│                      │   Simulation    │   │  Messages   │ │
│                      └─────────────────┘   └─────────────┘ │
│                              │                      │        │
│                              ▼                      ▼        │
│                      ┌─────────────────┐   ┌─────────────┐ │
│                      │   KIS Trading   │   │  Multi-lang │ │
│                      │      API        │   │  Channels   │ │
│                      └─────────────────┘   └─────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 주요 실행 흐름

```
1. 트리거 실행 (09:10 오전 / 15:30 오후)
   ↓
2. trigger_batch.py (급등주 포착)
   ├─ 거래량 급증 감지
   ├─ 갭 상승 감지
   └─ 섹터 성과 분석
   ↓
3. stock_analysis_orchestrator.py (메인 파이프라인)
   ├─ 1. 프리즘 시그널 얼럿 전송 (텔레그램)
   ├─ 2. AI 분석 리포트 생성
   │   ├─ 순차적 에이전트 실행 (rate limit 고려)
   │   └─ 13개 전문화 에이전트 협업
   ├─ 3. 마크다운 → PDF 변환
   │   └─ Playwright (Chromium 기반)
   ├─ 4. 텔레그램 요약 생성
   │   ├─ 요약 최적화 에이전트
   │   └─ 품질 평가 에이전트 (반복 개선)
   ├─ 5. 텔레그램 채널 전송
   │   └─ 다국어 브로드캐스팅 지원
   └─ 6. 매매 시뮬레이션 및 실행
       ├─ 매수/매도 의사결정 에이전트
       ├─ 포트폴리오 관리 (최대 10개 슬롯)
       └─ KIS API 실행 (데모 또는 실전 모드)
```

### 2.3 13개 AI 에이전트 시스템

#### 분석 팀 (6개 에이전트) - GPT-4.1 기반

1. **기술적 분석가** (`stock_price_agents.py`)
   - 주가 및 거래량 기술적 분석
   - 이동평균선, RSI, MACD, 볼린저밴드 등

2. **거래동향 분석가** (`stock_price_agents.py`)
   - 기관/외국인/개인 투자자별 거래 패턴 분석

3. **재무 분석가** (`company_info_agents.py`)
   - PER, PBR, ROE 등 밸류에이션 분석
   - 목표주가 및 증권사 컨센서스

4. **산업 분석가** (`company_info_agents.py`)
   - 사업 구조 및 경쟁력 분석
   - 시장 점유율, 경쟁사 비교

5. **정보 분석가** (`news_strategy_agents.py`)
   - 뉴스 및 공시 분석
   - 주가 변동 원인 규명

6. **시장 분석가** (`market_index_agents.py`)
   - KOSPI/KOSDAQ 지수 분석
   - 거시경제 지표 분석
   - **캐싱됨**: 동일 날짜 분석 결과 재사용

#### 전략 팀 (1개 에이전트) - GPT-4.1 기반

7. **투자 전략가** (`news_strategy_agents.py`)
   - 모든 분석 결과를 통합하여 최종 투자 전략 수립
   - 단기/중기/장기 투자자별 맞춤 전략 제시

#### 커뮤니케이션 팀 (3개 에이전트)

8-1. **요약 전문가** (`telegram_summary_optimizer_agent.py`)
   - 상세 리포트를 400자 내외 텔레그램 메시지로 변환

8-2. **품질 검수자** (`telegram_summary_evaluator_agent.py`)
   - 메시지 품질 평가 및 개선 제안
   - EXCELLENT 등급까지 반복 개선

8-3. **번역 전문가** (`telegram_translator_agent.py`)
   - 다국어 번역 (en, ja, zh, es, fr, de)

#### 매매 시뮬레이션 팀 (2개 에이전트) - GPT-5.1 기반

9-1. **매수 전문가** (`trading_agents.py`)
   - 밸류에이션과 모멘텀 기반 매수 점수 평가 (1~10점)
   - 포트폴리오 제약 조건 고려 (최대 10개 슬롯)

9-2. **매도 전문가** (`trading_agents.py`)
   - 보유 종목 모니터링 및 매도 타이밍 결정
   - 손절/익절 시나리오 실시간 모니터링

#### 사용자 상담 팀 (2개 에이전트) - Claude Sonnet 4.5 기반

10-1. **포트폴리오 상담가** (`telegram_ai_bot.py`)
   - 사용자 보유 종목 평가 및 맞춤형 투자 조언

10-2. **대화 관리자** (`telegram_ai_bot.py`)
   - 대화 맥락 유지 및 후속 질문 처리

---

## 3. 개발 환경 설정

### 3.1 사전 요구사항

- Python 3.10 이상
- Node.js (MCP 서버용)
- Git
- (선택) Docker

### 3.2 초기 설정

```bash
# 1. 저장소 클론
git clone https://github.com/dragon1086/prism-insight.git
cd prism-insight

# 2. Python 의존성 설치
pip install -r requirements.txt

# 3. Playwright 브라우저 설치 (PDF 변환용)
python3 -m playwright install chromium

# 4. 설정 파일 복사
cp .env.example .env
cp mcp_agent.config.yaml.example mcp_agent.config.yaml
cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml
cp ./examples/streamlit/config.py.example ./examples/streamlit/config.py
cp ./trading/config/kis_devlp.yaml.example ./trading/config/kis_devlp.yaml

# 5. Perplexity MCP 서버 설치 (Node.js)
cd perplexity-ask && npm install && cd ..

# 6. 한글 폰트 설치 (Linux만 필요)
# Rocky Linux/CentOS: sudo dnf install google-nanum-fonts
# Ubuntu: python3 cores/ubuntu_font_installer.py
sudo fc-cache -fv
python3 -c "import matplotlib.font_manager as fm; fm.fontManager.rebuild()"
```

### 3.3 필수 API 키 설정

#### `.env` 파일 설정

```bash
# 텔레그램 봇 토큰
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_AI_BOT_TOKEN="987654321:ZYXwvuTSRqponMLKjihgfEDcba"

# 텔레그램 채널 ID
TELEGRAM_CHANNEL_ID="-1001234567890"        # 한국어 (메인)
TELEGRAM_CHANNEL_ID_EN="-1001234567891"     # 영어
TELEGRAM_CHANNEL_ID_JA="-1001234567892"     # 일본어
TELEGRAM_CHANNEL_ID_ZH="-1001234567893"     # 중국어
```

#### `mcp_agent.secrets.yaml` 파일 설정

```yaml
# OpenAI
OPENAI_API_KEY: "sk-..."

# Anthropic
ANTHROPIC_API_KEY: "sk-ant-..."

# Firecrawl
FIRECRAWL_API_KEY: "fc-..."

# Perplexity
PERPLEXITY_API_KEY: "pplx-..."

# WiseReport (한국 금융 데이터)
WISEREPORT_KEY: "..."
```

#### `trading/config/kis_devlp.yaml` 파일 설정 (자동매매 사용 시)

```yaml
# 한국투자증권 API 설정
kis_app_key: "YOUR_APP_KEY"
kis_app_secret: "YOUR_APP_SECRET"
kis_account_number: "12345678-01"
kis_account_code: "01"

# 매매 설정
default_unit_amount: 10000     # 종목당 매수 금액 (원)
auto_trading: true             # 자동매매 활성화
default_mode: demo             # "demo" 또는 "real"
```

### 3.4 개발 환경 검증

```bash
# 1. Python 버전 확인
python3 --version  # 3.10 이상이어야 함

# 2. 의존성 설치 확인
python3 -c "import openai, anthropic, telegram; print('OK')"

# 3. Playwright 설치 확인
python3 -m playwright --version

# 4. 텔레그램 설정 확인 (텔레그램 사용 시)
python3 -c "from telegram_config import TelegramConfig; config = TelegramConfig(); config.validate_or_raise(); print('OK')"

# 5. 간단한 테스트 실행
python3 stock_analysis_orchestrator.py --mode morning --no-telegram
```

---

## 4. 핵심 컴포넌트 이해

### 4.1 주요 파일 구조

```
prism-insight/
├── 📂 cores/                           # 🤖 핵심 AI 분석 엔진
│   ├── 📂 agents/                     # AI 에이전트 정의
│   │   ├── company_info_agents.py     # 재무 및 사업 분석
│   │   ├── stock_price_agents.py      # 기술적 분석 및 거래동향
│   │   ├── news_strategy_agents.py    # 뉴스 및 투자 전략
│   │   ├── market_index_agents.py     # 시장 및 거시경제 분석
│   │   ├── trading_agents.py          # 매매 시나리오 및 매도 결정
│   │   ├── telegram_summary_optimizer_agent.py   # 요약 생성
│   │   ├── telegram_summary_evaluator_agent.py   # 품질 검수
│   │   └── telegram_translator_agent.py          # 다국어 번역
│   ├── analysis.py                    # 핵심 분석 오케스트레이션
│   ├── report_generation.py           # 리포트 템플릿 및 생성
│   ├── stock_chart.py                 # 차트 생성 (matplotlib)
│   ├── language_config.py             # 다국어 템플릿
│   └── utils.py                       # 유틸리티 함수
│
├── 📂 trading/                         # 💱 자동매매 시스템
│   ├── domestic_stock_trading.py      # KIS API 래퍼
│   ├── kis_auth.py                    # 인증 및 토큰 관리
│   ├── portfolio_telegram_reporter.py # 포트폴리오 리포트
│   └── 📂 config/                     # 매매 설정
│
├── stock_analysis_orchestrator.py     # 🎯 메인 오케스트레이터
├── stock_tracking_agent.py            # 매매 시뮬레이션 에이전트
├── stock_tracking_enhanced_agent.py   # 향상된 매매 에이전트
├── telegram_ai_bot.py                 # 텔레그램 봇 (Claude 기반)
├── telegram_bot_agent.py              # 봇 메시지 처리
├── telegram_summary_agent.py          # 요약 생성 파이프라인
├── trigger_batch.py                   # 급등주 포착
├── pdf_converter.py                   # 마크다운 → PDF 변환
├── telegram_config.py                 # TelegramConfig 클래스
└── check_market_day.py                # 장 휴장일 검증
```

### 4.2 핵심 컴포넌트 상세 설명

#### 4.2.1 `stock_analysis_orchestrator.py` - 메인 오케스트레이터

**역할**: 전체 파이프라인을 조율하는 핵심 컴포넌트

**주요 메서드:**
- `run_full_pipeline()`: 전체 파이프라인 실행
- `run_trigger_batch()`: 급등주 포착 실행
- `generate_reports()`: AI 분석 리포트 생성
- `convert_to_pdf()`: PDF 변환
- `generate_telegram_messages()`: 텔레그램 메시지 생성
- `send_telegram_messages()`: 텔레그램 전송

**실행 예시:**
```bash
# 오전 분석 실행
python stock_analysis_orchestrator.py --mode morning

# 텔레그램 없이 로컬 테스트
python stock_analysis_orchestrator.py --mode morning --no-telegram

# 영어 리포트 생성
python stock_analysis_orchestrator.py --mode morning --language en
```

#### 4.2.2 `cores/analysis.py` - 핵심 분석 엔진

**역할**: 13개 AI 에이전트를 조율하여 종합 분석 리포트 생성

**주요 흐름:**
```python
async def analyze_stock(company_code, company_name, reference_date, language="ko"):
    # 1. MCPApp 초기화
    app = MCPApp(name="stock_analysis")
    
    async with app.run() as parallel_app:
        # 2. 에이전트 디렉토리 가져오기
        agents = get_agent_directory(...)
        
        # 3. 순차적으로 각 섹션 분석 (rate limit 고려)
        section_reports = {}
        for section in base_sections:
            agent = agents[section]
            report = await generate_report(agent, section, ...)
            section_reports[section] = report
        
        # 4. 투자 전략 생성 (모든 분석 통합)
        strategy = await generate_investment_strategy(...)
        
        # 5. 최종 리포트 생성
        final_report = compose_final_report(...)
        
        return final_report
```

**중요 포인트:**
- **순차 실행**: API rate limit을 피하기 위해 병렬 실행하지 않음
- **시장 분석 캐싱**: 동일 날짜의 시장 분석 결과는 캐시에서 재사용
- **에러 처리**: 각 섹션 분석 실패 시에도 다음 섹션 계속 진행

#### 4.2.3 `trigger_batch.py` - 급등주 포착

**역할**: 거래량 급증, 갭 상승 등을 감지하여 관심종목 선별

**주요 감지 기준:**
- 거래량 급증: 전일 대비 거래량 증가율
- 갭 상승: 전일 종가 대비 시가 상승률
- 시총 대비 거래대금: 거래대금/시가총액 비율
- 마감 강도: 장 마감 시점의 주가 강도

**실행 예시:**
```bash
# 오전 급등주 포착
python trigger_batch.py morning INFO --output trigger_results.json

# 오후 급등주 포착
python trigger_batch.py afternoon INFO --output trigger_results.json
```

#### 4.2.4 `stock_tracking_agent.py` - 매매 시뮬레이션

**역할**: AI 리포트 기반으로 매수/매도 의사결정 및 포트폴리오 관리

**주요 기능:**
- 매수 점수 평가 (1~10점, 6점 이상 시 매수 고려)
- 포트폴리오 관리 (최대 10개 슬롯)
- 산업군 분산투자 (같은 섹터 최대 3개)
- 손절/익절 시나리오 모니터링

**포트폴리오 제약 조건:**
```python
MAX_SLOTS = 10              # 최대 보유 종목 수
MAX_SAME_SECTOR = 3         # 같은 섹터 최대 보유 수
SECTOR_CONCENTRATION = 0.3  # 한 섹터 최대 30%
```

#### 4.2.5 `trading/domestic_stock_trading.py` - KIS API 래퍼

**역할**: 한국투자증권 API를 통한 실제 매매 실행

**주요 기능:**
- 인증 및 토큰 관리
- 매수/매도 주문 실행
- 포트폴리오 조회
- 실시간 시세 조회

**사용 예시:**
```python
from trading.domestic_stock_trading import AsyncTradingContext

async with AsyncTradingContext(mode="demo", buy_amount=10000) as trader:
    # 매수
    result = await trader.async_buy_stock("005930", quantity=1)
    
    # 매도
    result = await trader.async_sell_stock("005930", quantity=1)
    
    # 포트폴리오 조회
    portfolio = await trader.async_get_portfolio()
```

---

## 5. 개발 워크플로우

### 5.1 일반적인 개발 흐름

```
1. 기능 요구사항 파악
   ↓
2. 관련 코드 탐색 및 이해
   ↓
3. 로컬 환경에서 테스트
   ↓
4. 코드 수정 및 개선
   ↓
5. 테스트 실행
   ↓
6. 커밋 및 PR 생성
```

### 5.2 코드 탐색 가이드

**새로운 기능을 추가하거나 수정할 때:**

1. **어디서 시작할까?**
   - 전체 파이프라인: `stock_analysis_orchestrator.py`
   - 분석 로직: `cores/analysis.py`
   - 에이전트 정의: `cores/agents/*.py`
   - 리포트 생성: `cores/report_generation.py`
   - 매매 로직: `stock_tracking_agent.py`, `trading/domestic_stock_trading.py`

2. **에이전트를 수정하려면?**
   - 에이전트 파일: `cores/agents/` 디렉토리
   - 프롬프트 수정: 각 에이전트의 `instruction` 파라미터
   - MCP 서버 추가: `mcp_servers` 파라미터에 추가

3. **설정을 변경하려면?**
   - 텔레그램: `telegram_config.py`, `.env`
   - MCP: `mcp_agent.config.yaml`, `mcp_agent.secrets.yaml`
   - 매매: `trading/config/kis_devlp.yaml`

### 5.3 테스트 실행

```bash
# 전체 테스트 실행
python -m pytest tests/

# 특정 테스트 파일 실행
python -m pytest tests/test_async_trading.py

# 빠른 통합 테스트
python tests/quick_test.py

# JSON 파싱 테스트
python tests/quick_json_test.py
```

### 5.4 Git 워크플로우

```bash
# 1. 브랜치 생성
git checkout -b feature/your-feature-name

# 2. 변경사항 커밋
git add .
git commit -m "feat: 기능 설명"

# 3. 원격 저장소에 푸시
git push -u origin feature/your-feature-name

# 4. Pull Request 생성
gh pr create --title "PR 제목" --body "설명"
```

**커밋 메시지 컨벤션:**
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 코드 리팩토링
test: 테스트 추가/수정
chore: 기타 작업
perf: 성능 개선
```

---

## 6. 실습 가이드

### 6.1 실습 1: 로컬에서 분석 리포트 생성하기

**목표**: 텔레그램 없이 로컬에서 분석 리포트를 생성해보기

```bash
# 1. 특정 종목 분석 리포트 생성
cd cores
python main.py

# 또는 직접 함수 호출
python -c "
import asyncio
from cores.analysis import analyze_stock

async def test():
    report = await analyze_stock(
        company_code='005930',
        company_name='삼성전자',
        reference_date='20251205',
        language='ko'
    )
    print(report[:500])  # 처음 500자만 출력

asyncio.run(test())
"
```

**예상 결과:**
- `reports/` 디렉토리에 마크다운 리포트 생성
- 리포트에는 기술적 분석, 재무 분석, 뉴스 분석 등이 포함됨

### 6.2 실습 2: 급등주 포착 기능 이해하기

**목표**: `trigger_batch.py`가 어떻게 급등주를 포착하는지 이해하기

```bash
# 1. 급등주 포착 실행
python trigger_batch.py morning INFO --output trigger_results.json

# 2. 결과 확인
cat trigger_results.json | python -m json.tool
```

**확인 사항:**
- 어떤 기준으로 종목이 선별되었는지
- 거래량 증가율, 갭 상승률 등 수치 확인
- `trigger_batch.py`의 필터링 로직 이해

### 6.3 실습 3: 에이전트 프롬프트 수정하기

**목표**: 기술적 분석가의 프롬프트를 수정하여 분석 스타일 변경하기

```python
# 파일: cores/agents/stock_price_agents.py

def create_price_volume_analysis_agent(...):
    if language == "en":
        instruction = """
        You are a technical analyst. 
        
        # 여기에 원하는 분석 스타일 추가
        Focus on:
        1. Short-term momentum (5-day, 10-day)
        2. Volume patterns
        3. Support and resistance levels
        
        Be concise and data-driven.
        """
    else:
        instruction = """
        당신은 기술적 분석가입니다.
        
        # 여기에 원하는 분석 스타일 추가
        다음에 집중하세요:
        1. 단기 모멘텀 (5일, 10일)
        2. 거래량 패턴
        3. 지지선과 저항선
        
        간결하고 데이터 중심으로 작성하세요.
        """
    
    return Agent(instruction=instruction, ...)
```

**테스트:**
```bash
# 수정 후 분석 리포트 생성하여 변경사항 확인
python cores/main.py
```

### 6.4 실습 4: 새로운 섹션 추가하기

**목표**: 분석 리포트에 새로운 섹션 추가하기

**단계:**

1. **에이전트 생성** (`cores/agents/your_agent.py`)
```python
from mcp_agent import Agent

def create_your_agent(company_name, company_code, reference_date, language="ko"):
    if language == "en":
        instruction = "You are a specialized analyst for [YOUR DOMAIN]..."
    else:
        instruction = "당신은 [도메인] 전문 분석가입니다..."
    
    return Agent(
        instruction=instruction,
        description=f"Your Agent for {company_name}",
        mcp_servers=["kospi_kosdaq"],  # 필요한 MCP 서버 추가
    )
```

2. **에이전트 등록** (`cores/agents/__init__.py`)
```python
from .your_agent import create_your_agent

def get_agent_directory(...):
    agents = {
        # ... 기존 에이전트들
        "your_section": lambda: create_your_agent(...),
    }
    return agents
```

3. **섹션 추가** (`cores/analysis.py`)
```python
base_sections = [
    "price_volume_analysis",
    # ... 기존 섹션들
    "your_section",  # 새 섹션 추가
]
```

4. **템플릿 추가** (`cores/report_generation.py`)
```python
section_templates = {
    # ... 기존 템플릿들
    "your_section": """
## Your Section Title

{content}
""",
}
```

### 6.5 실습 5: 매매 시뮬레이션 이해하기

**목표**: 매매 시뮬레이션이 어떻게 동작하는지 이해하기

```bash
# 1. 매매 시뮬레이션 실행 (데모 모드)
python stock_tracking_agent.py

# 또는 향상된 버전
python stock_tracking_enhanced_agent.py
```

**확인 사항:**
- 매수 점수 평가 로직
- 포트폴리오 제약 조건 적용
- 손절/익절 시나리오 생성

---

## 7. 문제 해결 가이드

### 7.1 자주 발생하는 문제들

#### 문제 1: Playwright PDF 생성 실패

**증상:**
```
Error: Browser executable not found
```

**해결:**
```bash
# Chromium 브라우저 설치
python3 -m playwright install chromium

# Ubuntu: 의존성 포함 설치
python3 -m playwright install --with-deps chromium

# 또는 설치 스크립트 사용
cd utils && chmod +x setup_playwright.sh && ./setup_playwright.sh
```

#### 문제 2: 한글 폰트가 차트에 표시되지 않음

**증상**: 차트에서 한글이 사각형으로 표시됨

**해결:**
```bash
# Rocky Linux/CentOS
sudo dnf install google-nanum-fonts

# Ubuntu/Debian
python3 cores/ubuntu_font_installer.py

# 폰트 캐시 재구성
sudo fc-cache -fv
python3 -c "import matplotlib.font_manager as fm; fm.fontManager.rebuild()"
```

#### 문제 3: 텔레그램 봇이 응답하지 않음

**체크리스트:**
1. `.env` 파일 확인
```bash
cat .env | grep TELEGRAM
```

2. 봇 토큰 유효성 확인
3. 봇이 채널에 접근 권한이 있는지 확인
4. 로그 확인
```bash
tail -f log_*.log
```

5. 설정 검증
```python
from telegram_config import TelegramConfig
config = TelegramConfig()
config.validate_or_raise()
config.log_status()
```

#### 문제 4: MCP 서버 연결 실패

**증상:**
```
Error: MCP server 'kospi_kosdaq' not responding
```

**해결:**
```bash
# 1. MCP 서버 설치 확인
python3 -m kospi_kosdaq_stock_server

# 2. mcp_agent.config.yaml 확인
cat mcp_agent.config.yaml | grep kospi_kosdaq

# 3. API 키 확인
cat mcp_agent.secrets.yaml | grep WISEREPORT

# 4. Perplexity 서버 테스트
cd perplexity-ask && npm install && node dist/index.js
```

#### 문제 5: API Rate Limit 오류

**증상:**
```
Error: Rate limit exceeded
```

**해결:**
- **순차 실행 유지**: 병렬 실행하지 않도록 주의
- **재시도 로직**: `tenacity` 라이브러리 사용
- **시장 분석 캐싱**: 동일 날짜 분석 결과 재사용

**코드 예시:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=10, max=30),
)
async def generate_report(...):
    # 구현
    pass
```

### 7.2 디버깅 팁

#### 로그 레벨 변경

```python
import logging

# DEBUG 레벨로 변경
logging.basicConfig(
    level=logging.DEBUG,  # INFO에서 DEBUG로 변경
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)
```

#### 특정 종목만 테스트

```python
# cores/main.py 수정
result = asyncio.run(analyze_stock(
    company_code="005930",  # 테스트할 종목 코드
    company_name="삼성전자",
    reference_date="20251205"
))
```

#### 텔레그램 없이 테스트

```bash
# --no-telegram 옵션 사용
python stock_analysis_orchestrator.py --mode morning --no-telegram
```

---

## 8. 다음 단계

### 8.1 학습 경로

1. **기본 이해 (1주차)**
   - [ ] 프로젝트 구조 파악
   - [ ] 주요 컴포넌트 이해
   - [ ] 로컬 환경에서 실행해보기

2. **심화 학습 (2-3주차)**
   - [ ] AI 에이전트 시스템 이해
   - [ ] 리포트 생성 프로세스 이해
   - [ ] 매매 시뮬레이션 로직 이해

3. **실전 개발 (4주차 이후)**
   - [ ] 작은 기능 개선부터 시작
   - [ ] 버그 수정
   - [ ] 새로운 기능 추가

### 8.2 추천 학습 자료

1. **프로젝트 문서**
   - `README.md` / `README_ko.md`: 프로젝트 개요
   - `CLAUDE.md`: AI 어시스턴트용 상세 가이드
   - `CONTRIBUTING.md`: 기여 가이드

2. **코드 탐색**
   - `cores/analysis.py`: 핵심 분석 로직
   - `cores/agents/*.py`: 각 에이전트 구현
   - `stock_analysis_orchestrator.py`: 전체 파이프라인

3. **외부 자료**
   - [mcp-agent 문서](https://github.com/modelcontextprotocol/python-sdk)
   - [python-telegram-bot 문서](https://python-telegram-bot.org/)
   - [pykrx 문서](https://github.com/sharebook-kr/pykrx)

### 8.3 기여 방법

1. **작은 것부터 시작**
   - 문서 개선
   - 코드 주석 추가
   - 버그 수정

2. **기능 추가 전에**
   - Issue에서 논의
   - 작은 PR로 시작
   - 테스트 코드 작성

3. **코드 리뷰**
   - PR 생성 시 상세한 설명
   - 변경 이유 명시
   - 테스트 결과 포함

### 8.4 질문하기

**질문할 때 포함할 정보:**
- 어떤 작업을 하려고 했는지
- 어떤 에러가 발생했는지 (에러 메시지 포함)
- 어떤 환경에서 실행했는지 (OS, Python 버전 등)
- 로그 파일 (가능한 경우)

**질문 채널:**
- GitHub Issues: 버그 리포트 및 기능 요청
- GitHub Discussions: 일반적인 질문
- 텔레그램: @stock_ai_agent

---

## 부록: 빠른 참조

### 주요 명령어

```bash
# 전체 파이프라인 실행
python stock_analysis_orchestrator.py --mode morning

# 텔레그램 없이 테스트
python stock_analysis_orchestrator.py --mode morning --no-telegram

# 급등주 포착만 실행
python trigger_batch.py morning INFO --output trigger_results.json

# 특정 종목 분석
cd cores && python main.py

# 매매 시뮬레이션
python stock_tracking_agent.py

# 텔레그램 봇 실행
python telegram_ai_bot.py
```

### 주요 디렉토리

| 디렉토리 | 용도 |
|---------|------|
| `cores/` | 핵심 분석 엔진 및 에이전트 |
| `trading/` | 매매 시스템 및 KIS API |
| `examples/` | 웹 인터페이스 (Streamlit, Next.js) |
| `tests/` | 테스트 코드 |
| `utils/` | 유틸리티 스크립트 |
| `docs/` | 문서 및 이미지 |

### 환경 변수

| 변수 | 용도 | 필수 여부 |
|------|------|----------|
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 토큰 | 텔레그램 사용 시 |
| `TELEGRAM_CHANNEL_ID` | 텔레그램 채널 ID | 텔레그램 사용 시 |
| `OPENAI_API_KEY` | OpenAI API 키 | 필수 |
| `ANTHROPIC_API_KEY` | Anthropic API 키 | 텔레그램 봇 사용 시 |

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-12-05  
**작성자**: PRISM-INSIGHT 개발팀

질문이나 개선 사항이 있으시면 GitHub Issue를 통해 알려주세요!

