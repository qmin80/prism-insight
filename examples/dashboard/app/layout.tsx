/**
 * Next.js Root Layout
 * 
 * [역할]
 * Next.js App Router의 루트 레이아웃 컴포넌트입니다.
 * 모든 페이지에 공통으로 적용되는 설정을 포함합니다.
 * 
 * [주요 기능]
 * 1. 전역 메타데이터 설정
 *    - 페이지 제목, 설명 등
 * 2. 폰트 설정
 *    - Geist Sans: 본문 폰트
 *    - Geist Mono: 코드 폰트
 * 3. 테마 제공자 설정
 *    - 다크/라이트 모드 지원
 *    - 시스템 설정 자동 감지
 * 4. 언어 제공자 설정
 *    - 한국어/영어 전환 지원
 * 
 * [사용 컴포넌트]
 * - ThemeProvider: 다크/라이트 모드 관리
 * - LanguageProvider: 다국어 지원
 * 
 * [스타일]
 * - globals.css: 전역 CSS 스타일
 */
import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { LanguageProvider } from "@/components/language-provider"

const _geist = Geist({ subsets: ["latin"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Prism Insight Dashboard",
  description: "AI Agent-based Korean Stock Analysis & Trading System",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className={`font-sans antialiased`}>
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
          <LanguageProvider>
            {children}
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
