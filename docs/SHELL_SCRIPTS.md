# PRISM-INSIGHT Shell Scripts 가이드

> **작성일**: 2025-12-05  
> **목적**: 프로젝트 내 모든 Shell 스크립트의 요약 정보와 사용법 정리

---

## 목차

1. [개요](#개요)
2. [스크립트 목록](#스크립트-목록)
3. [상세 설명](#상세-설명)
4. [사용 시나리오](#사용-시나리오)

---

## 개요

PRISM-INSIGHT 프로젝트에는 **6개의 Shell 스크립트**가 포함되어 있습니다:

- **실행 스크립트**: 주식 분석 배치 작업 실행
- **설정 스크립트**: Crontab 자동 설정
- **유틸리티 스크립트**: 백업, 로그 정리, 환경 설정

---

## 스크립트 목록

| 파일명 | 위치 | 용도 | 실행 빈도 |
|--------|------|------|-----------|
| `run_stock_analysis.sh` | 루트 | 주식 분석 배치 실행 | 매일 (오전/오후) |
| `setup_crontab.sh` | utils/ | Crontab 상세 설정 | 초기 설정 시 1회 |
| `setup_crontab_simple.sh` | utils/ | Crontab 간편 설정 | 초기 설정 시 1회 |
| `setup_playwright.sh` | utils/ | Playwright 브라우저 설치 | 초기 설정 시 1회 |
| `backup_configs.sh` | utils/ | 설정 파일 백업 | 정기적 (선택) |
| `cleanup_logs.sh` | utils/ | 로그 파일 정리 | 매일 (자동) |

---

## 상세 설명

### 1. `run_stock_analysis.sh`

**역할**: 주식 분석 배치 작업을 실행하는 메인 스크립트

**주요 기능**:
- 시장 영업일 자동 확인 (`check_market_day.py`)
- Python 환경 자동 감지 (venv > pyenv > system)
- 백그라운드 실행 (nohup)
- 프로세스 ID 저장
- 로그 파일 자동 생성

**사용법**:
```bash
# 오전 모드 실행
./run_stock_analysis.sh morning

# 오후 모드 실행
./run_stock_analysis.sh afternoon
```

**실행 결과**:
- `logs/stock_analysis_{mode}_{date}.log`: 실행 로그
- `logs/stock_analysis_{mode}_{date}.pid`: 프로세스 ID

**주의사항**:
- 주말 및 공휴일에는 자동으로 실행되지 않음
- Python 환경이 올바르게 설정되어 있어야 함
- `.env` 파일이 필요함

**Crontab 설정 예시**:
```bash
# 오전 9시 30분 실행 (월-금)
30 9 * * 1-5 /path/to/prism-insight/run_stock_analysis.sh morning

# 오후 3시 40분 실행 (월-금)
40 15 * * 1-5 /path/to/prism-insight/run_stock_analysis.sh afternoon
```

---

### 2. `utils/setup_crontab.sh`

**역할**: PRISM-INSIGHT 자동 실행을 위한 Crontab을 상세하게 설정하는 스크립트

**주요 기능**:
- 대화형 설정 모드
- 환경 변수 기반 자동 설정
- 기존 crontab 백업
- 환경 검증
- 설치/제거/확인 기능

**사용법**:
```bash
# 대화형 설치 (기본)
cd utils
./setup_crontab.sh

# 자동 설치 (환경 변수 사용)
PROJECT_DIR=/opt/prism-insight PYTHON_PATH=/usr/bin/python3 ./setup_crontab.sh --non-interactive

# 현재 crontab 확인
./setup_crontab.sh --show

# Crontab 제거
./setup_crontab.sh --uninstall

# Crontab 백업
./setup_crontab.sh --backup
```

**설정되는 스케줄**:
- **오전 9시 30분**: 오전 분석 배치 (월-금)
- **오후 3시 40분**: 오후 분석 배치 (월-금)
- **오전 7시**: 종목 정보 업데이트 (월-금)
- **오전 3시**: 로그 파일 정리 (매일)
- **오후 6시**: 포트폴리오 리포트 (선택사항, 주석 처리됨)

**환경 변수**:
- `PROJECT_DIR`: 프로젝트 디렉토리 경로
- `PYTHON_PATH`: Python 실행 파일 경로
- `LOG_DIR`: 로그 디렉토리 경로

**옵션**:
- `-h, --help`: 도움말 표시
- `-i, --install`: Crontab 설치 (기본값)
- `-u, --uninstall`: PRISM-INSIGHT crontab 제거
- `-s, --show`: 현재 설치된 crontab 표시
- `-b, --backup`: 현재 crontab 백업
- `--non-interactive`: 대화형 모드 건너뛰기

**특징**:
- Python 경로 자동 감지 (pyenv > venv > system)
- PATH 환경 변수 자동 구성
- 기존 crontab과 충돌 방지
- 색상 출력으로 가독성 향상

---

### 3. `utils/setup_crontab_simple.sh`

**역할**: 최소한의 설정으로 빠르게 Crontab을 구성하는 간편 스크립트

**주요 기능**:
- 자동 Python 감지
- 최소 설정으로 빠른 구성
- 기존 crontab 백업

**사용법**:
```bash
cd utils
./setup_crontab_simple.sh
```

**설정되는 스케줄**:
- **오전 9시 30분**: 오전 분석 (월-금)
- **오후 3시 40분**: 오후 분석 (월-금)
- **오전 7시**: 데이터 업데이트 (월-금)
- **오전 3시**: 로그 정리 (매일)

**특징**:
- `setup_crontab.sh`보다 간단하고 빠름
- 대화형 입력 없이 자동 설정
- 기본 설정만 적용

**언제 사용하나요?**
- 빠르게 기본 설정만 하고 싶을 때
- 상세한 커스터마이징이 필요 없을 때
- 테스트 환경에서 빠른 설정이 필요할 때

---

### 4. `utils/setup_playwright.sh`

**역할**: Playwright 브라우저를 설치하는 스크립트

**주요 기능**:
- Python3 설치 확인
- Playwright 패키지 설치 확인 및 설치
- Chromium 브라우저 설치

**사용법**:
```bash
cd utils
./setup_playwright.sh
```

**설정 요구사항**:
- Python3 설치 필요
- 인터넷 연결 필요 (브라우저 다운로드)

**설치되는 항목**:
- Playwright Python 패키지
- Chromium 브라우저

**사용 시나리오**:
- PDF 변환 기능 사용 시 필요
- `pdf_converter.py`에서 Playwright 사용 시 필요
- 초기 환경 설정 시 1회 실행

**주의사항**:
- 브라우저 다운로드에 시간이 걸릴 수 있음
- 디스크 공간 필요 (약 200MB)

---

### 5. `utils/backup_configs.sh`

**역할**: 중요 설정 파일 및 데이터베이스를 자동으로 백업하는 스크립트

**주요 기능**:
- 설정 파일 백업 (.env, mcp_agent.*.yaml)
- 데이터베이스 백업 (stock_tracking_db.sqlite)
- KIS API 설정 백업 (trading/config/kis_devlp.yaml)
- Streamlit 설정 백업 (examples/streamlit/config.py)
- 오래된 백업 자동 삭제 (7일 이상)
- 백업 파일 권한 설정 (보안)

**사용법**:
```bash
cd utils
./backup_configs.sh
```

**백업 위치**:
- 기본 경로: `~/prism_backups/{날짜_시간}/`
- 로그 파일: `~/prism_backups/backup.log`

**백업되는 파일**:
1. 루트 디렉토리:
   - `.env`
   - `mcp_agent.*.yaml` (모든 설정 파일)
   - `stock_tracking_db.sqlite`
2. `trading/config/`:
   - `kis_devlp.yaml`
3. `examples/streamlit/`:
   - `config.py`

**백업 정리**:
- 7일 이상 된 백업 자동 삭제
- 백업 파일 권한: 디렉토리 700, 파일 600

**Crontab 설정 예시**:
```bash
# 매일 오전 2시에 백업 실행
0 2 * * * /path/to/prism-insight/utils/backup_configs.sh >> /path/to/prism-insight/logs/backup.log 2>&1

# 매주 일요일 오전 2시에 백업 실행
0 2 * * 0 /path/to/prism-insight/utils/backup_configs.sh >> /path/to/prism-insight/logs/backup.log 2>&1
```

**주의사항**:
- 백업 디렉토리에 충분한 디스크 공간 필요
- 민감한 정보가 포함된 파일이므로 백업 파일 보안 주의

---

### 6. `utils/cleanup_logs.sh`

**역할**: 오래된 로그 파일을 자동으로 정리하는 스크립트

**주요 기능**:
- 7일 이상 된 로그 파일 삭제
- 누적 로그 파일 내용 비우기 (일요일만)
- 로그 정리 이력 기록

**사용법**:
```bash
cd utils
./cleanup_logs.sh
```

**정리되는 로그 파일**:
- `ai_bot_*.log*`
- `trigger_results_morning_*.json`
- `trigger_results_afternoon_*.json`
- `*stock_tracking_*.log`
- `orchestrator_*.log`
- `logs/stock_analysis_*.log` (내용 비우기, 일요일만)

**보관 기간**:
- 기본: 7일
- `DAYS_TO_KEEP` 변수로 조정 가능

**특별 처리**:
- `logs/` 디렉토리의 누적 로그 파일은 삭제하지 않고 내용만 비움
- 일요일에만 실행 (내용 비우기)

**Crontab 설정 예시**:
```bash
# 매일 오전 3시에 로그 정리
0 3 * * * /path/to/prism-insight/utils/cleanup_logs.sh >> /path/to/prism-insight/utils/log_cleanup.log 2>&1
```

**주의사항**:
- 삭제된 로그는 복구 불가능
- 중요한 로그는 별도로 백업 권장

---

## 사용 시나리오

### 시나리오 1: 초기 환경 설정

```bash
# 1. Playwright 설치
cd utils
./setup_playwright.sh

# 2. Crontab 설정 (간편 버전)
./setup_crontab_simple.sh

# 3. 설정 파일 백업
./backup_configs.sh
```

### 시나리오 2: 수동 배치 실행

```bash
# 오전 분석 실행
./run_stock_analysis.sh morning

# 오후 분석 실행
./run_stock_analysis.sh afternoon
```

### 시나리오 3: Crontab 상세 설정

```bash
# 대화형 설정
cd utils
./setup_crontab.sh

# 또는 환경 변수로 자동 설정
PROJECT_DIR=/opt/prism-insight \
PYTHON_PATH=/usr/bin/python3 \
LOG_DIR=/opt/prism-insight/logs \
./setup_crontab.sh --non-interactive
```

### 시나리오 4: 정기 백업 설정

```bash
# Crontab에 백업 스케줄 추가
crontab -e

# 다음 줄 추가:
0 2 * * 0 /path/to/prism-insight/utils/backup_configs.sh >> /path/to/prism-insight/logs/backup.log 2>&1
```

### 시나리오 5: 로그 정리 확인

```bash
# 수동 실행
cd utils
./cleanup_logs.sh

# 정리 이력 확인
cat ../utils/log_cleanup.log
```

---

## 스크립트 간 의존 관계

```
setup_crontab.sh / setup_crontab_simple.sh
    ↓
run_stock_analysis.sh (자동 실행)
    ↓
cleanup_logs.sh (로그 정리)

backup_configs.sh (독립 실행)
setup_playwright.sh (초기 설정 시 1회)
```

---

## 권장 실행 순서

### 초기 설정
1. `setup_playwright.sh` - 브라우저 설치
2. `setup_crontab_simple.sh` 또는 `setup_crontab.sh` - 자동 실행 설정
3. `backup_configs.sh` - 초기 백업

### 정기 실행 (Crontab으로 자동화)
1. `run_stock_analysis.sh` - 매일 오전/오후 (자동)
2. `cleanup_logs.sh` - 매일 오전 3시 (자동)
3. `backup_configs.sh` - 주 1회 (선택)

---

## 문제 해결

### Python 경로를 찾을 수 없는 경우
```bash
# Python 경로 확인
which python3
which python

# 환경 변수로 지정
export PYTHON_PATH=/usr/bin/python3
./run_stock_analysis.sh morning
```

### Crontab이 실행되지 않는 경우
```bash
# Crontab 확인
crontab -l

# 로그 확인
tail -f logs/stock_analysis_morning_*.log

# 수동 실행 테스트
./run_stock_analysis.sh morning
```

### 권한 오류가 발생하는 경우
```bash
# 실행 권한 부여
chmod +x run_stock_analysis.sh
chmod +x utils/*.sh

# 디렉토리 권한 확인
ls -la
```

---

## 파일 위치 요약

```
prism-insight/
├── run_stock_analysis.sh          # 메인 실행 스크립트
└── utils/
    ├── setup_crontab.sh           # Crontab 상세 설정
    ├── setup_crontab_simple.sh    # Crontab 간편 설정
    ├── setup_playwright.sh        # Playwright 설치
    ├── backup_configs.sh          # 설정 파일 백업
    └── cleanup_logs.sh            # 로그 정리
```

---

**문서 버전**: 1.0  
**최종 업데이트**: 2025-12-05

