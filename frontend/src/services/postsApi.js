import { requestJson } from './apiBase.js'

function formatDate(value) {
  if (!value) {
    return '날짜 정보 없음'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return '날짜 정보 없음'
  }

  return date.toLocaleDateString('ko-KR')
}

function mapPost(item) {
  return {
    id: String(item.id),
    category: item.category || '자유',
    title: item.title || '',
    content: item.content || '',
    author: item.author || '익명',
    festivalId: item.festival_id || null,
    createdAt: formatDate(item.created_at),
    createdAtRaw: item.created_at || null,
    updatedAtRaw: item.updated_at || null,
  }
}

/**
 * 게시글 목록을 조회합니다.
 *
 * 기존 Vue 화면에서 사용하는 인터페이스입니다.
 *
 * @param {object} params
 * @param {number} [params.page]
 * @param {number} [params.size]
 * @param {string} [params.q]
 * @param {string} [params.keyword]
 * @param {string} [params.category]
 * @param {string|number} [params.festivalId]
 * @param {object} [requestOptions]
 * @returns {Promise<object>}
 */
export async function getPostList(
  params = {},
  requestOptions = {},
) {
  const search = new URLSearchParams()

  if (params.page) {
    search.set('page', String(params.page))
  }

  if (params.size) {
    search.set('size', String(params.size))
  }

  if (params.q) {
    search.set('q', params.q)
  }

  if (params.keyword) {
    search.set('keyword', params.keyword)
  }

  if (params.category) {
    search.set('category', params.category)
  }

  if (params.festivalId) {
    search.set('festival_id', String(params.festivalId))
  }

  const query = search.toString()

  const payload = await requestJson(
    `/api/posts${query ? `?${query}` : ''}`,
    requestOptions,
  )

  const items = Array.isArray(payload?.items)
    ? payload.items.map(mapPost)
    : []

  return {
    items,
    total: payload?.total || 0,
    page: payload?.page || params.page || 1,
    size: payload?.size || params.size || 20,
    pages: payload?.pages || 0,
  }
}

/**
 * 자동 테스트와 단일 인자 방식 호출을 지원합니다.
 *
 * fetchImpl, baseUrl 등 요청 설정을 첫 번째 인자에서 분리한 뒤
 * getPostList의 두 번째 인자로 전달합니다.
 *
 * @param {object} params
 * @returns {Promise<object>}
 */
export async function listPosts(params = {}) {
  const {
    fetchImpl,
    baseUrl,
    signal,
    headers,
    ...queryParams
  } = params

  return getPostList(queryParams, {
    fetchImpl,
    baseUrl,
    signal,
    headers,
  })
}

/**
 * 게시글 한 건을 조회합니다.
 *
 * @param {string|number} id
 * @param {object} requestOptions
 * @returns {Promise<object>}
 */
export async function getPostById(
  id,
  requestOptions = {},
) {
  const payload = await requestJson(
    `/api/posts/${encodeURIComponent(String(id))}`,
    requestOptions,
  )

  return mapPost(payload)
}

/**
 * 게시글을 생성합니다.
 *
 * @param {object} post
 * @param {object} requestOptions
 * @returns {Promise<object>}
 */
export async function createPost(
  {
    category,
    title,
    content,
    author,
    password,
    festivalId,
  },
  requestOptions = {},
) {
  const payload = await requestJson('/api/posts', {
    ...requestOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(requestOptions.headers || {}),
    },
    body: JSON.stringify({
      category: category || '자유',
      title,
      content,
      author: author || '익명',
      password,
      festival_id: festivalId || null,
    }),
  })

  return mapPost(payload)
}

/**
 * 게시글을 수정합니다.
 *
 * @param {string|number} id
 * @param {object} post
 * @param {object} requestOptions
 * @returns {Promise<object>}
 */
export async function updatePost(
  id,
  {
    category,
    title,
    content,
    password,
    festivalId,
  },
  requestOptions = {},
) {
  const payload = await requestJson(
    `/api/posts/${encodeURIComponent(String(id))}`,
    {
      ...requestOptions,
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(requestOptions.headers || {}),
      },
      body: JSON.stringify({
        category,
        title,
        content,
        password,
        festival_id: festivalId || null,
      }),
    },
  )

  return mapPost(payload)
}

/**
 * 게시글을 삭제합니다.
 *
 * 백엔드가 204 No Content를 반환하면 null을 반환합니다.
 *
 * @param {string|number} id
 * @param {string} password
 * @param {object} requestOptions
 * @returns {Promise<object|null>}
 */
export async function deletePost(
  id,
  password,
  requestOptions = {},
) {
  return requestJson(
    `/api/posts/${encodeURIComponent(String(id))}`,
    {
      ...requestOptions,
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(requestOptions.headers || {}),
      },
      body: JSON.stringify({ password }),
    },
  )
}