import { onBeforeUnmount, ref } from 'vue'

function errorMessage(error) {
  if (error instanceof Error && error.message) return error.message
  return '행사 데이터를 불러오지 못했습니다.'
}

export function createFestivalQueryController(
  loader,
  {
    wakeDelayMs = 8_000,
    setTimer = setTimeout,
    clearTimer = clearTimeout,
    onState = () => {},
    initialData = null,
  } = {},
) {
  if (typeof loader !== 'function') throw new TypeError('loader must be a function')

  const state = {
    data: initialData,
    loading: false,
    waking: false,
    error: '',
  }

  let sequence = 0
  let activeController = null
  let activeWakeTimer = null
  let lastParams = null
  let lastOptions = null
  let disposed = false

  function publish(patch) {
    Object.assign(state, patch)
    onState({ ...state })
  }

  async function run(params = {}, options = {}) {
    if (disposed) return null

    sequence += 1
    const requestSequence = sequence
    activeController?.abort()
    activeController = new AbortController()
    lastParams = { ...params }
    lastOptions = { ...options }

    if (activeWakeTimer !== null) clearTimer(activeWakeTimer)
    publish({ loading: true, waking: false, error: '' })
    const requestWakeTimer = setTimer(() => {
      if (!disposed && requestSequence === sequence && state.loading) {
        publish({ waking: true })
      }
    }, wakeDelayMs)
    activeWakeTimer = requestWakeTimer

    try {
      const result = await loader(params, {
        ...options,
        signal: activeController.signal,
      })
      if (disposed || requestSequence !== sequence) return null
      publish({ data: result, error: '' })
      return result
    } catch (error) {
      const aborted = activeController.signal.aborted || error?.name === 'AbortError'
      if (disposed || requestSequence !== sequence || aborted) return null
      publish({ error: errorMessage(error) })
      return null
    } finally {
      clearTimer(requestWakeTimer)
      if (activeWakeTimer === requestWakeTimer) activeWakeTimer = null
      if (!disposed && requestSequence === sequence) {
        publish({ loading: false, waking: false })
      }
    }
  }

  function retry() {
    if (!lastParams || disposed) return Promise.resolve(null)
    return run(lastParams, { ...lastOptions, forceRefresh: true })
  }

  function dispose() {
    disposed = true
    sequence += 1
    activeController?.abort()
    if (activeWakeTimer !== null) clearTimer(activeWakeTimer)
    activeWakeTimer = null
  }

  function getState() {
    return { ...state }
  }

  return { run, retry, dispose, getState }
}

export function useFestivalQuery(loader, { initialData = null, wakeDelayMs = 8_000 } = {}) {
  const data = ref(initialData)
  const loading = ref(false)
  const waking = ref(false)
  const error = ref('')

  const controller = createFestivalQueryController(loader, {
    initialData,
    wakeDelayMs,
    onState: (state) => {
      data.value = state.data
      loading.value = state.loading
      waking.value = state.waking
      error.value = state.error
    },
  })

  onBeforeUnmount(() => controller.dispose())

  return {
    data,
    loading,
    waking,
    error,
    run: controller.run,
    retry: controller.retry,
    dispose: controller.dispose,
  }
}
