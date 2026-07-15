const DEFAULT_API_BASE_URL = 'http://localhost:8000'

export function resolveApiBaseUrl() {
  const configured = import.meta.env?.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
  return configured.replace(/\/$/, '')
}

export async function requestJson(path, options = {}) {
  const baseUrl = (options.baseUrl || resolveApiBaseUrl()).replace(/\/$/, '')
  const response = await fetch(`${baseUrl}${path}`, options)

  let payload = null
  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok) {
    const detail = payload && typeof payload.detail === 'string' ? payload.detail : '서버 요청에 실패했습니다.'
    throw new Error(detail)
  }

  return payload
}
