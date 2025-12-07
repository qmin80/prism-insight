/**
 * Utility Functions
 * 
 * [역할]
 * 대시보드에서 사용하는 공통 유틸리티 함수입니다.
 * 
 * [주요 함수]
 * - cn(): 클래스명 병합 함수
 *   * clsx와 tailwind-merge를 결합하여 클래스명을 병합
 *   * Tailwind CSS 클래스 충돌 해결
 *   * 조건부 클래스명 적용
 * 
 * [사용 예시]
 *   cn("px-4", "py-2", isActive && "bg-blue-500")
 *   cn("text-sm", className) // 외부에서 전달된 className과 병합
 * 
 * [의존성]
 * - clsx: 조건부 클래스명 생성
 * - tailwind-merge: Tailwind CSS 클래스 병합 및 충돌 해결
 */
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
