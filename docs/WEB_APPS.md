# PRISM-INSIGHT 웹앱 가이드

> **작성일**: 2025-12-05  
> **목적**: 프로젝트에 구현된 웹앱들의 상세 설명

---

## 목차

1. [웹앱 개요](#웹앱-개요)
2. [Streamlit 앱](#streamlit-앱)
3. [Next.js 대시보드](#nextjs-대시보드)
4. [데이터 생성 스크립트](#데이터-생성-스크립트)

---

## 웹앱 개요

PRISM-INSIGHT 프로젝트에는 **2개의 웹앱**이 구현되어 있습니다:

### 1. Streamlit 앱 (`examples/streamlit/`)
- **기술 스택**: Streamlit (Python)
- **포트**: 8501 (기본)
- **용도**: 사용자가 직접 종목 코드를 입력하여 AI 분석 리포트를 요청하고 이메일로 받는 웹 인터페이스
- **주요 기능**:
  - 종목 코드 입력 및 분석 요청
  - 백그라운드 분석 작업 큐 관리
  - 분석 완료 후 이메일 자동 전송
  - 분석 상태 실시간 확인

### 2. Next.js 대시보드 (`examples/dashboard/`)
- **기술 스택**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **포트**: 3000 (기본)
- **용도**: PRISM-INSIGHT의 매매 성과, 포트폴리오, 거래 이력을 실시간으로 시각화하는 대시보드
- **주요 기능**:
  - 실전투자 포트폴리오 표시
  - 시뮬레이터 포트폴리오 표시
  - 매매 성과 차트 및 통계
  - AI 의사결정 이력 조회
  - 관심종목 이력 조회
  - 전인구 트레이딩 실험실 (Jeoningu Lab)
  - 운영 비용 투명성 표시
  - 다국어 지원 (한국어/영어)

---

## Streamlit 앱

### 폴더 구조

```
examples/streamlit/
├── app_modern.py          # 메인 Streamlit 앱
├── email_sender.py        # 이메일 전송 모듈
├── config.py.example      # 설정 파일 예시
└── __init__.py
```

### 주요 파일 설명

#### `app_modern.py`
- **역할**: Streamlit 웹앱의 메인 파일
- **주요 클래스**: `ModernStockAnalysisApp`
- **주요 기능**:
  - 사용자 인터페이스 구성
  - 종목 코드 입력 폼
  - 분석 요청 큐 관리
  - 백그라운드 워커 스레드
  - 분석 상태 실시간 업데이트
  - 이메일 전송 트리거
- **호출하는 모듈**:
  - `cores/analysis.py`: 분석 리포트 생성
  - `email_sender.py`: 이메일 전송
  - `queue`, `threading`: 백그라운드 작업 관리

#### `email_sender.py`
- **역할**: 분석 리포트를 이메일로 전송하는 모듈
- **주요 함수**:
  - `send_email()`: 이메일 전송
  - `convert_md_to_html()`: 마크다운을 HTML로 변환
- **기능**:
  - 마크다운 리포트를 HTML로 변환
  - HTML 본문 + 마크다운/HTML 첨부파일 전송
  - SMTP 서버를 통한 이메일 발송

#### `config.py.example`
- **역할**: 설정 파일 템플릿
- **설정 항목**:
  - SMTP 서버 설정
  - 발신자 이메일 및 비밀번호
  - API 키 설정

### 실행 방법

```bash
# Streamlit 앱 실행
cd examples/streamlit
streamlit run app_modern.py

# 또는 특정 포트로 실행
streamlit run app_modern.py --server.port 8501
```

### 설정 방법

1. `config.py.example`을 `config.py`로 복사
2. SMTP 서버 정보 입력
3. API 키 설정 (`.env` 파일 또는 `config.py`)

---

## Next.js 대시보드

### 폴더 구조

```
examples/dashboard/
├── app/                          # Next.js App Router
│   ├── page.tsx                  # 메인 페이지
│   ├── layout.tsx                # 레이아웃
│   ├── globals.css               # 전역 스타일
│   └── favicon.ico               # 파비콘
├── components/                   # React 컴포넌트
│   ├── dashboard-header.tsx      # 대시보드 헤더
│   ├── metrics-cards.tsx         # 지표 카드
│   ├── holdings-table.tsx        # 보유 종목 테이블
│   ├── performance-chart.tsx    # 성과 차트
│   ├── ai-decisions-page.tsx     # AI 의사결정 페이지
│   ├── trading-history-page.tsx  # 거래 이력 페이지
│   ├── watchlist-page.tsx        # 관심종목 페이지
│   ├── jeoningu-lab-page.tsx     # 전인구 실험실 페이지
│   ├── stock-detail-modal.tsx    # 종목 상세 모달
│   ├── operating-costs-card.tsx  # 운영 비용 카드
│   ├── language-provider.tsx     # 다국어 제공자
│   ├── theme-provider.tsx        # 테마 제공자
│   ├── project-footer.tsx        # 프로젝트 푸터
│   └── ui/                       # shadcn/ui 컴포넌트
│       └── [70개 UI 컴포넌트]
├── hooks/                         # React 훅
│   ├── use-mobile.ts             # 모바일 감지 훅
│   └── use-toast.ts              # 토스트 알림 훅
├── lib/                           # 유틸리티
│   └── utils.ts                   # 공통 유틸리티
├── types/                         # TypeScript 타입
│   └── dashboard.ts              # 대시보드 데이터 타입
├── public/                        # 정적 파일
│   ├── dashboard_data.json       # 대시보드 데이터 (한국어)
│   ├── dashboard_data_en.json    # 대시보드 데이터 (영어)
│   └── [로고 및 이미지 파일들]
├── styles/                        # 스타일
│   └── globals.css               # 전역 CSS
├── package.json                   # 의존성 관리
├── next.config.mjs                # Next.js 설정
├── tsconfig.json                  # TypeScript 설정
└── DASHBOARD_README_ko.md         # 대시보드 가이드
```

### 주요 파일 설명

#### `app/page.tsx`
- **역할**: 대시보드 메인 페이지
- **주요 기능**:
  - 대시보드 데이터 로드 (`dashboard_data.json`)
  - 탭 네비게이션 (대시보드, AI 의사결정, 거래 이력, 관심종목, 전인구 실험실)
  - 5분마다 데이터 자동 갱신
  - 종목 클릭 시 상세 모달 표시
- **사용 컴포넌트**:
  - `DashboardHeader`: 헤더 및 탭 네비게이션
  - `OperatingCostsCard`: 운영 비용 표시
  - `MetricsCards`: 핵심 지표 카드
  - `HoldingsTable`: 보유 종목 테이블
  - `PerformanceChart`: 성과 차트
  - `AIDecisionsPage`: AI 의사결정 페이지
  - `TradingHistoryPage`: 거래 이력 페이지
  - `WatchlistPage`: 관심종목 페이지
  - `JeoninguLabPage`: 전인구 실험실 페이지

#### `app/layout.tsx`
- **역할**: Next.js 레이아웃 컴포넌트
- **주요 기능**:
  - 전역 메타데이터 설정
  - 테마 제공자 설정
  - 언어 제공자 설정

#### `components/dashboard-header.tsx`
- **역할**: 대시보드 헤더 및 네비게이션
- **주요 기능**:
  - 탭 네비게이션
  - 마지막 업데이트 시간 표시
  - 언어 전환

#### `components/metrics-cards.tsx`
- **역할**: 핵심 지표를 카드 형태로 표시
- **표시 지표**:
  - 총 보유 종목 수
  - 실전투자 수익률
  - 시뮬레이터 수익률
  - 거래 이력 통계 (승률, 평균 수익률 등)

#### `components/holdings-table.tsx`
- **역할**: 보유 종목을 테이블로 표시
- **주요 기능**:
  - 실전투자 포트폴리오 표시
  - 시뮬레이터 포트폴리오 표시
  - 종목 클릭 시 상세 모달 열기
  - 수익률 색상 코딩

#### `components/performance-chart.tsx`
- **역할**: 성과 차트 표시
- **주요 기능**:
  - 시장 지수와 PRISM 성과 비교
  - 시간별 수익률 추이
  - recharts 라이브러리 사용

#### `components/ai-decisions-page.tsx`
- **역할**: AI 의사결정 이력 페이지
- **주요 기능**:
  - 보유 종목 매도 결정 이력 표시
  - 매도 사유 및 신뢰도 표시
  - 기술적 분석 결과 표시

#### `components/trading-history-page.tsx`
- **역할**: 거래 이력 페이지
- **주요 기능**:
  - 완료된 거래 이력 표시
  - 수익률, 보유 기간 등 상세 정보
  - 필터링 및 정렬

#### `components/watchlist-page.tsx`
- **역할**: 관심종목 이력 페이지
- **주요 기능**:
  - AI 분석을 통해 평가된 종목 이력
  - 매수/스킵/관망 결정 표시
  - 매수 점수 및 근거 표시

#### `components/jeoningu-lab-page.tsx`
- **역할**: 전인구 트레이딩 실험실 페이지
- **주요 기능**:
  - 전인구 유튜브 분석 기반 역추세 매매 시뮬레이션 결과
  - 성과 지표 및 거래 이력 표시

#### `components/stock-detail-modal.tsx`
- **역할**: 종목 상세 정보 모달
- **주요 기능**:
  - 종목 상세 정보 표시
  - 매매 시나리오 표시
  - 목표가/손절가 정보

#### `components/operating-costs-card.tsx`
- **역할**: 운영 비용 투명성 카드
- **주요 기능**:
  - 월별 운영 비용 표시
  - API 비용 상세 내역
  - 서버 및 인프라 비용

#### `types/dashboard.ts`
- **역할**: TypeScript 타입 정의
- **주요 타입**:
  - `DashboardData`: 전체 대시보드 데이터
  - `Holding`: 보유 종목 정보
  - `TradingHistory`: 거래 이력
  - `WatchlistItem`: 관심종목 정보
  - `JeoninguLabData`: 전인구 실험실 데이터

### 실행 방법

```bash
# 의존성 설치
cd examples/dashboard
npm install react-is --legacy-peer-deps

# 개발 모드 실행
npm run dev

# 프로덕션 빌드
npm run build

# 프로덕션 실행
npm start

# PM2로 실행 (권장)
pm2 start npm --name "dashboard" -- start
```

### 데이터 갱신

대시보드 데이터는 `generate_dashboard_json.py` 스크립트로 생성됩니다:

```bash
# 수동 실행
cd examples
python generate_dashboard_json.py

# Crontab으로 자동 갱신 (5분마다)
*/5 * * * * cd /project-root/examples && python generate_dashboard_json.py
```

---

## 데이터 생성 스크립트

### `examples/generate_dashboard_json.py`

- **역할**: SQLite 데이터베이스에서 데이터를 읽어 대시보드용 JSON 파일 생성
- **주요 기능**:
  - SQLite 데이터베이스 연결
  - 보유 종목 데이터 조회
  - 거래 이력 데이터 조회
  - 관심종목 이력 조회
  - AI 의사결정 이력 조회
  - 전인구 트레이딩 데이터 조회
  - 한국투자증권 API 연동 (실전투자 데이터)
  - 시장 지수 데이터 조회 (pykrx)
  - 영어 번역 생성 (선택적)
  - JSON 파일 저장
- **출력 파일**:
  - `examples/dashboard/public/dashboard_data.json` (한국어)
  - `examples/dashboard/public/dashboard_data_en.json` (영어)
- **주요 클래스**: `DashboardDataGenerator`

---

## 포트 정보

| 서비스 | 포트 | 기술 스택 |
|--------|------|-----------|
| Streamlit 앱 | 8501 | Streamlit |
| Next.js 대시보드 | 3000 | Next.js |

> 두 서비스는 서로 다른 포트를 사용하므로 **포트 충돌 없이** 동시 실행 가능합니다.

---

## 배포 방법

### Streamlit 앱 배포

```bash
# Streamlit Cloud에 배포
# 또는
streamlit run app_modern.py --server.port 8501
```

### Next.js 대시보드 배포

```bash
# Vercel에 배포 (권장)
vercel deploy

# 또는 PM2로 자체 호스팅
pm2 start npm --name "dashboard" -- start
pm2 save
pm2 startup
```

---

## 데이터 흐름

```
1. SQLite 데이터베이스 (stock_tracking_db.sqlite)
   ↓
2. generate_dashboard_json.py (데이터 추출 및 변환)
   ↓
3. dashboard_data.json (JSON 파일 생성)
   ↓
4. Next.js 대시보드 (JSON 파일 읽기 및 표시)
```

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-12-05

