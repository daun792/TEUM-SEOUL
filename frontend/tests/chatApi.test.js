import test from 'node:test'
import assert from 'node:assert/strict'

import { sendChatMessage } from '../src/services/chatApi.js'

test('sendChatMessage posts the trimmed message to the configured backend', async () => {
  const calls = []
  const fetchImpl = async (url, options) => {
    calls.push({ url, options })
    return {
      ok: true,
      async json() {
        return { answer: '경복궁 안내입니다.' }
      },
    }
  }

  const answer = await sendChatMessage('  경복궁 위치 알려줘  ', {
    baseUrl: 'https://api.example.com/',
    fetchImpl,
  })

  assert.equal(answer, '경복궁 안내입니다.')
  assert.equal(calls[0].url, 'https://api.example.com/api/chat')
  assert.deepEqual(JSON.parse(calls[0].options.body), { message: '경복궁 위치 알려줘' })
})

test('sendChatMessage exposes a readable backend error', async () => {
  const fetchImpl = async () => ({
    ok: false,
    async json() {
      return { detail: '서비스 설정을 확인해 주세요.' }
    },
  })

  await assert.rejects(
    () => sendChatMessage('축제 추천', { baseUrl: 'https://api.example.com', fetchImpl }),
    /서비스 설정을 확인해 주세요/,
  )
})
