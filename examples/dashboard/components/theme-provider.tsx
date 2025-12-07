/**
 * Theme Provider Component
 * 
 * [역할]
 * 다크/라이트 모드 테마를 관리하는 Context Provider입니다.
 * next-themes 라이브러리를 래핑하여 사용합니다.
 * 
 * [주요 기능]
 * 1. 테마 상태 관리
 *    - "dark" (다크 모드) 또는 "light" (라이트 모드)
 *    - "system" (시스템 설정 따르기)
 * 2. 테마 전환
 *    - setTheme() 함수로 테마 변경
 *    - 시스템 설정 자동 감지
 * 3. 테마 유지
 *    - localStorage에 저장하여 새로고침 후에도 유지
 * 
 * [사용 예시]
 *   const { theme, setTheme } = useTheme()
 *   <button onClick={() => setTheme("dark")}>Dark Mode</button>
 * 
 * [Props]
 * - attribute: HTML 속성 이름 (기본값: "class")
 * - defaultTheme: 기본 테마 (기본값: "dark")
 * - enableSystem: 시스템 설정 감지 활성화
 * - disableTransitionOnChange: 테마 변경 시 트랜지션 비활성화
 * 
 * [의존성]
 * - next-themes: Next.js용 테마 관리 라이브러리
 */
"use client"

import type * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children, ...props }: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
