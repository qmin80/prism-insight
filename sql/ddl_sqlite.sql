-- =====================================================
-- PRISM-INSIGHT SQLite DDL
-- =====================================================
-- 매매 시뮬레이션 및 트레이딩 이력 저장용 SQLite 데이터베이스 스키마
-- 작성일: 2025-12-05
-- =====================================================

-- =====================================================
-- 1. 보유 종목 테이블 (stock_holdings)
-- =====================================================
-- 현재 포트폴리오에 보유 중인 종목 정보를 저장
-- =====================================================

CREATE TABLE IF NOT EXISTS stock_holdings (
    ticker TEXT PRIMARY KEY,              -- 종목 코드 (예: "005930")
    company_name TEXT NOT NULL,           -- 회사명 (예: "삼성전자")
    buy_price REAL NOT NULL,              -- 매수가
    buy_date TEXT NOT NULL,                -- 매수일 (YYYY-MM-DD 형식)
    current_price REAL,                    -- 현재가 (최신 업데이트)
    last_updated TEXT,                     -- 마지막 업데이트 시간
    scenario TEXT,                         -- 매매 시나리오 (JSON 형식)
    target_price REAL,                     -- 목표가
    stop_loss REAL                         -- 손절가
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_stock_holdings_buy_date 
    ON stock_holdings(buy_date);

CREATE INDEX IF NOT EXISTS idx_stock_holdings_company_name 
    ON stock_holdings(company_name);

-- =====================================================
-- 2. 매매 이력 테이블 (trading_history)
-- =====================================================
-- 완료된 매매 거래(매수→매도)의 전체 이력을 저장
-- =====================================================

CREATE TABLE IF NOT EXISTS trading_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,                 -- 종목 코드
    company_name TEXT NOT NULL,           -- 회사명
    buy_price REAL NOT NULL,              -- 매수가
    buy_date TEXT NOT NULL,                -- 매수일 (YYYY-MM-DD)
    sell_price REAL NOT NULL,              -- 매도가
    sell_date TEXT NOT NULL,               -- 매도일 (YYYY-MM-DD)
    profit_rate REAL NOT NULL,             -- 수익률 (소수점, 예: 0.15 = 15%)
    holding_days INTEGER NOT NULL,         -- 보유 기간 (일)
    scenario TEXT                          -- 매매 시나리오 (JSON 형식)
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_trading_history_ticker 
    ON trading_history(ticker);

CREATE INDEX IF NOT EXISTS idx_trading_history_buy_date 
    ON trading_history(buy_date DESC);

CREATE INDEX IF NOT EXISTS idx_trading_history_sell_date 
    ON trading_history(sell_date DESC);

CREATE INDEX IF NOT EXISTS idx_trading_history_profit_rate 
    ON trading_history(profit_rate DESC);

-- =====================================================
-- 3. 시장 상황 분석 테이블 (market_condition)
-- =====================================================
-- 일별 시장 상황(강세/중립/약세) 및 변동성 분석 결과 저장
-- =====================================================

CREATE TABLE IF NOT EXISTS market_condition (
    date TEXT PRIMARY KEY,                -- 분석일 (YYYY-MM-DD)
    kospi_index REAL,                      -- KOSPI 지수
    kosdaq_index REAL,                     -- KOSDAQ 지수
    condition INTEGER,                     -- 시장 상황 (1: 강세, 0: 중립, -1: 약세)
    volatility REAL                        -- 시장 변동성
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_market_condition_date 
    ON market_condition(date DESC);

CREATE INDEX IF NOT EXISTS idx_market_condition_condition 
    ON market_condition(condition);

-- =====================================================
-- 4. 관심종목 이력 테이블 (watchlist_history)
-- =====================================================
-- AI 분석을 통해 평가된 종목들의 매수/관망 결정 이력 저장
-- 매수하지 않은 종목도 포함하여 추적
-- =====================================================

CREATE TABLE IF NOT EXISTS watchlist_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,                 -- 종목 코드
    company_name TEXT NOT NULL,           -- 회사명
    current_price REAL NOT NULL,          -- 분석 시점 주가
    analyzed_date TEXT NOT NULL,          -- 분석일 (YYYY-MM-DD)
    buy_score INTEGER NOT NULL,           -- 매수 점수 (1-10점)
    min_score INTEGER NOT NULL,           -- 최소 요구 점수 (보통 6점)
    decision TEXT NOT NULL,               -- 결정 ("BUY", "SKIP", "WATCH")
    skip_reason TEXT NOT NULL,            -- 스킵 사유 (매수하지 않은 경우)
    target_price REAL,                    -- 목표가
    stop_loss REAL,                       -- 손절가
    investment_period TEXT,                -- 투자 기간 ("단기", "중기", "장기")
    sector TEXT,                          -- 섹터/업종
    scenario TEXT,                        -- 매매 시나리오 (JSON 형식)
    portfolio_analysis TEXT,               -- 포트폴리오 분석 결과
    valuation_analysis TEXT,               -- 밸류에이션 분석 결과
    sector_outlook TEXT,                  -- 섹터 전망
    market_condition TEXT,               -- 시장 상황 분석
    rationale TEXT                        -- 매수/스킵 근거
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_watchlist_history_ticker 
    ON watchlist_history(ticker);

CREATE INDEX IF NOT EXISTS idx_watchlist_history_analyzed_date 
    ON watchlist_history(analyzed_date DESC);

CREATE INDEX IF NOT EXISTS idx_watchlist_history_decision 
    ON watchlist_history(decision);

CREATE INDEX IF NOT EXISTS idx_watchlist_history_buy_score 
    ON watchlist_history(buy_score DESC);

CREATE INDEX IF NOT EXISTS idx_watchlist_history_sector 
    ON watchlist_history(sector);

-- =====================================================
-- 5. 보유 종목 매도 결정 테이블 (holding_decisions)
-- =====================================================
-- AI가 보유 종목에 대해 매도 여부를 판단한 결정 이력 저장
-- =====================================================

CREATE TABLE IF NOT EXISTS holding_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,                 -- 종목 코드
    decision_date TEXT NOT NULL,           -- 결정일 (YYYY-MM-DD)
    decision_time TEXT NOT NULL,          -- 결정 시간 (HH:MM:SS)
    
    -- 현재 상태
    current_price REAL NOT NULL,          -- 현재가
    should_sell BOOLEAN NOT NULL,         -- 매도 여부 (TRUE/FALSE)
    sell_reason TEXT,                     -- 매도 사유
    confidence INTEGER,                    -- 신뢰도 (1-10점)
    
    -- 분석 결과
    technical_trend TEXT,                 -- 기술적 추세 분석
    volume_analysis TEXT,                 -- 거래량 분석
    market_condition_impact TEXT,         -- 시장 상황 영향
    time_factor TEXT,                     -- 시간 요소 분석
    
    -- 포트폴리오 조정 필요 여부
    portfolio_adjustment_needed BOOLEAN,  -- 포트폴리오 조정 필요 여부
    adjustment_reason TEXT,               -- 조정 사유
    new_target_price REAL,                -- 새로운 목표가
    new_stop_loss REAL,                   -- 새로운 손절가
    adjustment_urgency TEXT,              -- 조정 긴급도
    
    -- 전체 JSON 데이터 (원본 데이터 보존)
    full_json_data TEXT NOT NULL,         -- 전체 결정 데이터 (JSON 형식)
    
    -- 메타데이터
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    
    -- 외래키 (선택적, stock_holdings 참조)
    FOREIGN KEY (ticker) REFERENCES stock_holdings(ticker)
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_holding_decisions_ticker 
    ON holding_decisions(ticker);

CREATE INDEX IF NOT EXISTS idx_holding_decisions_decision_date 
    ON holding_decisions(decision_date DESC, decision_time DESC);

CREATE INDEX IF NOT EXISTS idx_holding_decisions_should_sell 
    ON holding_decisions(should_sell);

CREATE INDEX IF NOT EXISTS idx_holding_decisions_confidence 
    ON holding_decisions(confidence DESC);

-- =====================================================
-- 6. 전인구 트레이딩 이력 테이블 (jeoningu_trades)
-- =====================================================
-- 전인구 유튜브 채널 분석 기반 역추세 매매 시뮬레이션 이력
-- 각 영상 = 1행, 매매 실행 시 추가 정보 기록
-- =====================================================

CREATE TABLE IF NOT EXISTS jeoningu_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 영상 정보 (모든 행에 포함)
    video_id TEXT NOT NULL UNIQUE,        -- 유튜브 영상 ID
    video_title TEXT NOT NULL,            -- 영상 제목
    video_date TEXT NOT NULL,              -- 영상 업로드일 (YYYY-MM-DD)
    video_url TEXT NOT NULL,              -- 영상 URL
    analyzed_date TEXT NOT NULL,          -- 분석일 (YYYY-MM-DD HH:MM:SS)
    
    -- AI 분석 결과 (모든 행에 포함)
    jeon_sentiment TEXT NOT NULL,         -- 전인구 감정 분석 ("상승", "하락", "중립")
    jeon_reasoning TEXT,                  -- 감정 분석 근거
    contrarian_action TEXT NOT NULL,      -- 역추세 행동 ("인버스2X매수", "레버리지매수", "전량매도", "관망")
    
    -- 매매 실행 정보 (매매가 발생한 경우만)
    trade_type TEXT,                      -- 매매 유형 ("BUY", "SELL", "HOLD")
    stock_code TEXT,                      -- 종목 코드 (ETF 코드)
    stock_name TEXT,                      -- 종목명 (ETF명)
    quantity INTEGER DEFAULT 0,           -- 수량
    price REAL DEFAULT 0,                 -- 단가
    amount REAL DEFAULT 0,                -- 거래 금액
    
    -- 수익 추적 (매도 시만)
    related_buy_id INTEGER,               -- 관련 매수 거래 ID (매도 시 매수 거래와 연결)
    profit_loss REAL DEFAULT 0,           -- 손익 금액
    profit_loss_pct REAL DEFAULT 0,      -- 손익률 (%)
    
    -- 포트폴리오 추적
    balance_before REAL NOT NULL,         -- 거래 전 잔액
    balance_after REAL NOT NULL,          -- 거래 후 잔액
    cumulative_return_pct REAL DEFAULT 0, -- 누적 수익률 (%)
    
    -- 메타데이터
    notes TEXT,                           -- 기타 메모
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    -- 외래키 (자기 참조: 매도 거래가 매수 거래를 참조)
    FOREIGN KEY (related_buy_id) REFERENCES jeoningu_trades(id)
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_jeoningu_video_id 
    ON jeoningu_trades(video_id);

CREATE INDEX IF NOT EXISTS idx_jeoningu_analyzed_date 
    ON jeoningu_trades(analyzed_date DESC);

CREATE INDEX IF NOT EXISTS idx_jeoningu_trade_type 
    ON jeoningu_trades(trade_type);

CREATE INDEX IF NOT EXISTS idx_jeoningu_stock_code 
    ON jeoningu_trades(stock_code);

CREATE INDEX IF NOT EXISTS idx_jeoningu_related_buy_id 
    ON jeoningu_trades(related_buy_id);

CREATE INDEX IF NOT EXISTS idx_jeoningu_jeon_sentiment 
    ON jeoningu_trades(jeon_sentiment);

-- =====================================================
-- 뷰 (Views)
-- =====================================================

-- 현재 보유 종목 뷰 (현재가 포함)
CREATE VIEW IF NOT EXISTS v_current_holdings AS
SELECT 
    h.ticker,
    h.company_name,
    h.buy_price,
    h.buy_date,
    h.current_price,
    h.target_price,
    h.stop_loss,
    CASE 
        WHEN h.current_price > 0 THEN 
            ((h.current_price - h.buy_price) / h.buy_price * 100)
        ELSE NULL 
    END AS current_profit_rate,
    CASE 
        WHEN h.current_price > 0 AND h.buy_price > 0 THEN 
            (h.current_price - h.buy_price)
        ELSE NULL 
    END AS current_profit_amount,
    h.last_updated,
    h.scenario
FROM stock_holdings h;

-- 매매 성과 요약 뷰
CREATE VIEW IF NOT EXISTS v_trading_performance AS
SELECT 
    COUNT(*) AS total_trades,
    SUM(CASE WHEN profit_rate > 0 THEN 1 ELSE 0 END) AS winning_trades,
    SUM(CASE WHEN profit_rate <= 0 THEN 1 ELSE 0 END) AS losing_trades,
    ROUND(AVG(profit_rate) * 100, 2) AS avg_profit_rate_pct,
    ROUND(SUM(CASE WHEN profit_rate > 0 THEN profit_rate ELSE 0 END) * 100, 2) AS total_profit_rate_pct,
    ROUND(AVG(holding_days), 1) AS avg_holding_days,
    MIN(buy_date) AS first_trade_date,
    MAX(sell_date) AS last_trade_date
FROM trading_history;

-- 관심종목 분석 통계 뷰
CREATE VIEW IF NOT EXISTS v_watchlist_stats AS
SELECT 
    analyzed_date,
    COUNT(*) AS total_analyzed,
    SUM(CASE WHEN decision = 'BUY' THEN 1 ELSE 0 END) AS buy_decisions,
    SUM(CASE WHEN decision = 'SKIP' THEN 1 ELSE 0 END) AS skip_decisions,
    SUM(CASE WHEN decision = 'WATCH' THEN 1 ELSE 0 END) AS watch_decisions,
    ROUND(AVG(buy_score), 2) AS avg_buy_score,
    ROUND(AVG(CASE WHEN decision = 'BUY' THEN buy_score ELSE NULL END), 2) AS avg_buy_score_bought
FROM watchlist_history
GROUP BY analyzed_date
ORDER BY analyzed_date DESC;

-- 전인구 트레이딩 성과 뷰
CREATE VIEW IF NOT EXISTS v_jeoningu_performance AS
SELECT 
    COUNT(DISTINCT CASE WHEN trade_type = 'SELL' THEN id END) AS total_sell_trades,
    SUM(CASE WHEN trade_type = 'SELL' AND profit_loss > 0 THEN 1 ELSE 0 END) AS winning_trades,
    SUM(CASE WHEN trade_type = 'SELL' AND profit_loss <= 0 THEN 1 ELSE 0 END) AS losing_trades,
    ROUND(
        CASE 
            WHEN COUNT(DISTINCT CASE WHEN trade_type = 'SELL' THEN id END) > 0 
            THEN (SUM(CASE WHEN trade_type = 'SELL' AND profit_loss > 0 THEN 1 ELSE 0 END) * 100.0 / 
                  COUNT(DISTINCT CASE WHEN trade_type = 'SELL' THEN id END))
            ELSE 0 
        END, 2
    ) AS win_rate_pct,
    ROUND(SUM(CASE WHEN trade_type = 'SELL' THEN profit_loss ELSE 0 END), 0) AS total_profit_loss,
    ROUND(AVG(CASE WHEN trade_type = 'SELL' THEN profit_loss_pct ELSE NULL END), 2) AS avg_profit_loss_pct,
    MAX(cumulative_return_pct) AS max_cumulative_return_pct
FROM jeoningu_trades;

-- =====================================================
-- 주석 및 설명
-- =====================================================

/*
데이터베이스 파일 위치: stock_tracking_db.sqlite (프로젝트 루트)

주요 테이블 설명:
1. stock_holdings: 현재 포트폴리오에 보유 중인 종목
2. trading_history: 완료된 매매 거래 이력
3. market_condition: 일별 시장 상황 분석 결과
4. watchlist_history: AI 분석을 통해 평가된 관심종목 이력
5. holding_decisions: 보유 종목에 대한 매도 결정 이력
6. jeoningu_trades: 전인구 유튜브 분석 기반 역추세 매매 이력

데이터 보존 정책:
- watchlist_history: 1개월 이상 된 데이터는 자동 정리 (stock_tracking_enhanced_agent.py)
- market_condition: 일별 데이터만 유지 (최신 데이터로 업데이트)
- trading_history, stock_holdings: 전체 이력 보존

사용 예시:
-- 현재 보유 종목 조회
SELECT * FROM v_current_holdings;

-- 매매 성과 확인
SELECT * FROM v_trading_performance;

-- 최근 관심종목 분석 결과
SELECT * FROM watchlist_history 
WHERE analyzed_date >= date('now', '-7 days')
ORDER BY analyzed_date DESC, buy_score DESC;

-- 전인구 트레이딩 성과
SELECT * FROM v_jeoningu_performance;
*/

