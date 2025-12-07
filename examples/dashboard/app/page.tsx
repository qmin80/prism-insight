/**
 * Dashboard Main Page
 * 
 * [역할]
 * Next.js 대시보드의 메인 페이지입니다.
 * 대시보드 데이터를 로드하고 여러 탭을 통해 다양한 정보를 표시합니다.
 * 
 * [주요 기능]
 * 1. 대시보드 데이터 로드
 *    - dashboard_data.json (한국어) 또는 dashboard_data_en.json (영어) 로드
 *    - 5분마다 자동 갱신
 * 2. 탭 네비게이션
 *    - dashboard: 메인 대시보드 (포트폴리오, 성과 차트)
 *    - ai-decisions: AI 의사결정 이력
 *    - trading: 거래 이력
 *    - watchlist: 관심종목 이력
 *    - jeoningu-lab: 전인구 트레이딩 실험실
 * 3. 종목 상세 모달
 *    - 종목 클릭 시 상세 정보 표시
 * 
 * [사용 컴포넌트]
 * - DashboardHeader: 헤더 및 탭 네비게이션
 * - OperatingCostsCard: 운영 비용 표시
 * - MetricsCards: 핵심 지표 카드
 * - HoldingsTable: 보유 종목 테이블 (실전투자/시뮬레이터)
 * - PerformanceChart: 성과 차트
 * - AIDecisionsPage: AI 의사결정 페이지
 * - TradingHistoryPage: 거래 이력 페이지
 * - WatchlistPage: 관심종목 페이지
 * - JeoninguLabPage: 전인구 실험실 페이지
 * - StockDetailModal: 종목 상세 모달
 * 
 * [데이터 소스]
 * - /dashboard_data.json (한국어)
 * - /dashboard_data_en.json (영어)
 * 
 * [자동 갱신]
 * - 5분마다 데이터 자동 갱신 (useEffect + setInterval)
 */
"use client"

import { useState, useEffect } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { OperatingCostsCard } from "@/components/operating-costs-card"
import { MetricsCards } from "@/components/metrics-cards"
import { HoldingsTable } from "@/components/holdings-table"
import { PerformanceChart } from "@/components/performance-chart"
import { AIDecisionsPage } from "@/components/ai-decisions-page"
import { TradingHistoryPage } from "@/components/trading-history-page"
import { WatchlistPage } from "@/components/watchlist-page"
import { JeoninguLabPage } from "@/components/jeoningu-lab-page"
import { StockDetailModal } from "@/components/stock-detail-modal"
import { ProjectFooter } from "@/components/project-footer"
import { useLanguage } from "@/components/language-provider"
import type { DashboardData, Holding } from "@/types/dashboard"

export default function Page() {
  const { language, t } = useLanguage()
  const [data, setData] = useState<DashboardData | null>(null)
  const [activeTab, setActiveTab] = useState<"dashboard" | "ai-decisions" | "trading" | "watchlist" | "jeoningu-lab">("dashboard")
  const [selectedStock, setSelectedStock] = useState<Holding | null>(null)
  const [isRealTrading, setIsRealTrading] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const dataFile = language === "en" ? "/dashboard_data_en.json" : "/dashboard_data.json"
        const response = await fetch(dataFile)
        const jsonData = await response.json()
        setData(jsonData)
      } catch (error) {
        console.error("[v0] Failed to fetch dashboard data:", error)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 5 * 60 * 1000) // 5분마다 갱신

    return () => clearInterval(interval)
  }, [language])

  const handleStockClick = (stock: Holding, isReal: boolean) => {
    setSelectedStock(stock)
    setIsRealTrading(isReal)
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">{t("loading.text")}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader activeTab={activeTab} onTabChange={setActiveTab} lastUpdated={data.generated_at} />

      <main className="container mx-auto px-4 py-6 max-w-[1600px]">
        {activeTab === "dashboard" && (
          <div className="space-y-6">
            {/* 운영 비용 카드 - 최상단 배치 */}
            <OperatingCostsCard costs={data.operating_costs} />

            {/* 핵심 지표 카드 */}
            <MetricsCards
              summary={data.summary}
              realPortfolio={data.real_portfolio || []}
              tradingHistoryCount={data.trading_history?.length || 0}
              tradingHistoryTotalProfit={
                data.trading_history?.reduce((sum, trade) => sum + trade.profit_rate, 0) || 0
              }
              tradingHistoryAvgProfit={
                data.trading_history?.length > 0
                  ? data.trading_history.reduce((sum, trade) => sum + trade.profit_rate, 0) / data.trading_history.length
                  : 0
              }
              tradingHistoryAvgDays={
                data.trading_history?.length > 0
                  ? data.trading_history.reduce((sum, trade) => sum + trade.holding_days, 0) / data.trading_history.length
                  : 0
              }
              tradingHistoryWinRate={
                data.trading_history?.length > 0
                  ? (data.trading_history.filter(t => t.profit_rate > 0).length / data.trading_history.length) * 100
                  : 0
              }
              tradingHistoryWinCount={
                data.trading_history?.filter(t => t.profit_rate > 0).length || 0
              }
              tradingHistoryLossCount={
                data.trading_history?.filter(t => t.profit_rate <= 0).length || 0
              }
            />

            {/* 실전투자 포트폴리오 - 최우선 표시 */}
            {data.real_portfolio && data.real_portfolio.length > 0 && (
              <HoldingsTable
                holdings={data.real_portfolio}
                onStockClick={(stock) => handleStockClick(stock, true)}
                title={t("table.realPortfolio")}
                isRealTrading={true}
              />
            )}

            {/* 프리즘 시뮬레이터 */}
            <HoldingsTable
              holdings={data.holdings}
              onStockClick={(stock) => handleStockClick(stock, false)}
              title={t("table.simulator")}
              isRealTrading={false}
            />

            {/* 시장 지수 차트 - 하단 배치 */}
            <PerformanceChart
              data={data.market_condition}
              prismPerformance={data.prism_performance}
              holdings={data.holdings}
              summary={data.summary}
            />
          </div>
        )}

        {activeTab === "ai-decisions" && <AIDecisionsPage data={data} />}

        {activeTab === "trading" && <TradingHistoryPage history={data.trading_history} summary={data.summary} />}

        {activeTab === "watchlist" && <WatchlistPage watchlist={data.watchlist} />}

        {activeTab === "jeoningu-lab" && data.jeoningu_lab && <JeoninguLabPage data={data.jeoningu_lab} />}
      </main>

      {/* 프로젝트 소개 Footer */}
      <ProjectFooter />

      {selectedStock && (
        <StockDetailModal 
          stock={selectedStock} 
          onClose={() => setSelectedStock(null)} 
          isRealTrading={isRealTrading}
        />
      )}
    </div>
  )
}
