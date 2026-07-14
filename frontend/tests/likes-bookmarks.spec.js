import { describe, expect, it, vi } from 'vitest'
import { useBookmarks } from '../src/composables/useBookmarks'
import { useClientId } from '../src/composables/useClientId'


describe('anonymous browser state', () => {
  it('stores and removes bookmarked post IDs', () => {
    const bookmarks = useBookmarks()
    bookmarks.toggle(12)
    expect(bookmarks.isBookmarked(12)).toBe(true)
    expect(JSON.parse(localStorage.getItem('teumSeoulBookmarks'))).toEqual([12])

    bookmarks.toggle(12)
    expect(bookmarks.isBookmarked(12)).toBe(false)
  })

  it('reuses the generated anonymous client ID', () => {
    const randomUUID = vi.spyOn(crypto, 'randomUUID').mockReturnValue('12345678-test-client')
    expect(useClientId()).toBe('12345678-test-client')
    expect(useClientId()).toBe('12345678-test-client')
    expect(randomUUID).toHaveBeenCalledOnce()
  })
})
