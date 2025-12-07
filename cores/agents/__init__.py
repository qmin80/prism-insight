"""
AI Agent Directory Factory

[역할]
각 섹션별 AI 에이전트를 생성하는 팩토리 함수입니다.
cores/analysis.py에서 호출되어 필요한 에이전트들을 생성합니다.

[생성하는 에이전트]
1. price_volume_analysis: 기술적 분석가 (stock_price_agents.py)
2. investor_trading_analysis: 거래동향 분석가 (stock_price_agents.py)
3. company_status: 재무 분석가 (company_info_agents.py)
4. company_overview: 산업 분석가 (company_info_agents.py)
5. news_analysis: 정보 분석가 (news_strategy_agents.py)
6. market_index_analysis: 시장 분석가 (market_index_agents.py)

[호출 관계]
- 호출하는 모듈:
  * cores/agents/stock_price_agents.py
  * cores/agents/company_info_agents.py
  * cores/agents/news_strategy_agents.py
  * cores/agents/market_index_agents.py
  * cores/utils.py: WiseReport URL 생성

- 호출되는 모듈:
  * cores/analysis.py: 에이전트 디렉토리 가져오기

[주요 함수]
- get_agent_directory(): 섹션별 에이전트 딕셔너리 반환

[파라미터]
- company_name: 기업명
- company_code: 종목 코드
- reference_date: 분석 기준일 (YYYYMMDD)
- base_sections: 생성할 에이전트 섹션 리스트
- language: 언어 코드 ("ko" 또는 "en")

[반환값]
- Dict[str, Agent]: 섹션명을 키로 하는 에이전트 딕셔너리
"""
def get_agent_directory(company_name, company_code, reference_date, base_sections, language: str = "ko"):
    """
    각 섹션별 에이전트 디렉토리를 반환

    Args:
        company_name: 기업명
        company_code: 종목 코드
        reference_date: 분석 기준일 (YYYYMMDD)
        base_sections: 생성할 에이전트 섹션 리스트
        language: Language code ("ko" or "en")

    Returns:
        Dict[str, Agent]: 섹션명을 키로 하는 에이전트 딕셔너리
    """
    from cores.agents.stock_price_agents import (
        create_price_volume_analysis_agent,
        create_investor_trading_analysis_agent
    )
    from cores.agents.company_info_agents import (
        create_company_status_agent,
        create_company_overview_agent
    )
    from cores.agents.news_strategy_agents import (
        create_news_analysis_agent
    )
    from cores.agents.market_index_agents import (
        create_market_index_analysis_agent
    )
    from cores.agents.trading_agents import (
        create_trading_scenario_agent,
        create_sell_decision_agent
    )
    from cores.utils import get_wise_report_url
    
    # URL 매핑 생성
    urls = {k: get_wise_report_url(k, company_code) for k in [
        "기업현황", "기업개요", "재무분석", "투자지표", 
        "컨센서스", "경쟁사분석", "지분현황", "업종분석", "최근리포트"
    ]}
    
    # 날짜 계산
    from datetime import datetime, timedelta
    ref_date = datetime.strptime(reference_date, "%Y%m%d")
    max_years = 2
    max_years_ago = (ref_date - timedelta(days=365*max_years)).strftime("%Y%m%d")
    
    agent_creators = {
        "price_volume_analysis": lambda: create_price_volume_analysis_agent(
            company_name, company_code, reference_date, max_years_ago, max_years, language
        ),
        "investor_trading_analysis": lambda: create_investor_trading_analysis_agent(
            company_name, company_code, reference_date, max_years_ago, max_years, language
        ),
        "company_status": lambda: create_company_status_agent(
            company_name, company_code, reference_date, urls, language
        ),
        "company_overview": lambda: create_company_overview_agent(
            company_name, company_code, reference_date, urls, language
        ),
        "news_analysis": lambda: create_news_analysis_agent(
            company_name, company_code, reference_date, language
        ),
        "market_index_analysis": lambda: create_market_index_analysis_agent(
            reference_date, max_years_ago, max_years, language
        )
    }
    
    agents = {}
    for section in base_sections:
        if section in agent_creators:
            agents[section] = agent_creators[section]()
    
    return agents
