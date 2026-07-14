import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 20000,
})

export function getErrorMessage(error, fallback = '요청을 처리하지 못했습니다.') {
  return error?.response?.data?.detail || error?.message || fallback
}

export default api
