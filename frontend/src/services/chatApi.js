const DEFAULT_API_BASE_URL = 'http://localhost:8000'

export function resolveApiBaseUrl() {
  const configured = import.meta.env?.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
  return configured.replace(/\/$/, '')
}

export async function sendChatMessage(message, options = {}) {
  const cleanedMessage = message.trim()
  if (!cleanedMessage) {
    throw new Error('질문을 입력해 주세요.')
  }

  const baseUrl = (options.baseUrl || resolveApiBaseUrl()).replace(/\/$/, '')
  const fetchImpl = options.fetchImpl || fetch
  const response = await fetchImpl(`${baseUrl}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: cleanedMessage }),
  })

  let payload = {}
  try {
    payload = await response.json()
  } catch {
    payload = {}
  }

  if (!response.ok) {
    const detail = typeof payload.detail === 'string' ? payload.detail : '챗봇 서버에 연결하지 못했습니다.'
    throw new Error(detail)
  }

  if (typeof payload.answer !== 'string' || !payload.answer.trim()) {
    throw new Error('챗봇 응답 형식이 올바르지 않습니다.')
  }

  return payload.answer.trim()
}
