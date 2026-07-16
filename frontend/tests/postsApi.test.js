import test from 'node:test'
import assert from 'node:assert/strict'

import { createPost, deletePost, listPosts } from '../src/services/postsApi.js'

test('listPosts forwards pagination and query params', async () => {
  const calls = []
  const fetchImpl = async (url) => {
    calls.push(url)
    return {
      ok: true,
      async json() {
        return { items: [], total: 0, page: 1, size: 20, pages: 0 }
      },
    }
  }

  await listPosts({ q: '축제', page: 2, size: 10, fetchImpl, baseUrl: 'https://api.example.com' })

  assert.match(calls[0], /q=%EC%B6%95%EC%A0%9C/)
  assert.match(calls[0], /page=2/)
  assert.match(calls[0], /size=10/)
})

test('createPost sends JSON body', async () => {
  const calls = []
  const fetchImpl = async (_url, options) => {
    calls.push(options)
    return {
      ok: true,
      async json() {
        return { id: 1, title: '테스트', content: '내용', author: '익명' }
      },
    }
  }

  await createPost(
    { title: '테스트', content: '내용', author: '익명', password: '1234' },
    { fetchImpl, baseUrl: 'https://api.example.com' },
  )

  const body = JSON.parse(calls[0].body)
  assert.equal(body.password, '1234')
})

test('deletePost accepts 204 response without body', async () => {
  const fetchImpl = async () => ({
    ok: true,
    async json() {
      throw new Error('no body')
    },
  })

  const payload = await deletePost('1', '1234', { fetchImpl, baseUrl: 'https://api.example.com' })
  assert.equal(payload, null)
})
