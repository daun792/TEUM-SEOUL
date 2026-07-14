import { describe, expect, it, vi } from 'vitest'
import { buildShareUrl, shareCourse } from '../src/utils/share'

const course = {
  performance: { id: 10, name: '문학주간 2026' },
  phase: 'after',
  available_minutes: 120,
  preferred_category: '문화시설',
  places: [{ id: 21 }, { id: 22 }],
}

describe('course sharing', () => {
  it('builds a reproducible URL with performance and place IDs', () => {
    const url = buildShareUrl(course, 'https://example.com')
    expect(url).toContain('performanceId=10')
    expect(url).toContain('phase=after')
    expect(url).toContain('minutes=120')
    expect(url).toContain('placeIds=21%2C22')
  })

  it('copies the URL when Web Share API is unavailable', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'share', { value: undefined, configurable: true })
    Object.defineProperty(navigator, 'clipboard', { value: { writeText }, configurable: true })

    const result = await shareCourse(course, 'https://example.com')

    expect(result).toBe('copied')
    expect(writeText).toHaveBeenCalledOnce()
  })
})
