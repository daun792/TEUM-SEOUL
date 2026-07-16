import test from 'node:test'
import assert from 'node:assert/strict'
import { createFestivalQueryController } from '../src/composables/useFestivalQuery.js'

function deferred() {
  let resolve
  let reject
  const promise = new Promise((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

test('suppresses a stale response after a newer request finishes', async () => {
  const first = deferred()
  const second = deferred()
  let call = 0
  const controller = createFestivalQueryController(() => {
    call += 1
    return call === 1 ? first.promise : second.promise
  })

  const firstRun = controller.run({ q: 'first' })
  const secondRun = controller.run({ q: 'second' })
  second.resolve({ items: ['new'] })
  await secondRun
  first.resolve({ items: ['old'] })
  await firstRun

  assert.deepEqual(controller.getState().data, { items: ['new'] })
  assert.equal(controller.getState().loading, false)
})

test('aborts the previous request when a new request starts', async () => {
  const signals = []
  const first = deferred()
  const controller = createFestivalQueryController((_params, options) => {
    signals.push(options.signal)
    if (signals.length === 1) return first.promise
    return Promise.resolve({ items: [] })
  })

  const firstRun = controller.run({ page: 1 })
  await controller.run({ page: 2 })
  assert.equal(signals[0].aborted, true)

  first.resolve({ items: ['ignored'] })
  await firstRun
})

test('enters waking state after the configured delay', async () => {
  let wakeCallback
  const request = deferred()
  const controller = createFestivalQueryController(
    () => request.promise,
    {
      setTimer: (callback) => {
        wakeCallback = callback
        return 1
      },
      clearTimer: () => {},
    },
  )

  const run = controller.run({ page: 1 })
  assert.equal(controller.getState().waking, false)
  wakeCallback()
  assert.equal(controller.getState().waking, true)

  request.resolve({ items: [] })
  await run
  assert.equal(controller.getState().waking, false)
})

test('retry repeats the last request and forces refresh', async () => {
  const calls = []
  const controller = createFestivalQueryController(async (params, options) => {
    calls.push({ params, options })
    if (calls.length === 1) throw new Error('temporary')
    return { items: ['ok'] }
  })

  await controller.run({ q: '서울' })
  assert.match(controller.getState().error, /temporary/)
  await controller.retry()

  assert.equal(calls.length, 2)
  assert.deepEqual(calls[1].params, { q: '서울' })
  assert.equal(calls[1].options.forceRefresh, true)
  assert.deepEqual(controller.getState().data, { items: ['ok'] })
})

test('dispose aborts work and prevents later state changes', async () => {
  const request = deferred()
  let signal
  const controller = createFestivalQueryController((_params, options) => {
    signal = options.signal
    return request.promise
  })

  const run = controller.run({ page: 1 })
  controller.dispose()
  assert.equal(signal.aborted, true)

  request.resolve({ items: ['late'] })
  await run
  assert.equal(controller.getState().data, null)
})

test('a stale request cannot clear the wake timer for the active request', async () => {
  const timers = new Map()
  let timerId = 0
  const first = deferred()
  const second = deferred()
  let call = 0
  const controller = createFestivalQueryController(
    () => {
      call += 1
      return call === 1 ? first.promise : second.promise
    },
    {
      setTimer: (callback) => {
        timerId += 1
        timers.set(timerId, callback)
        return timerId
      },
      clearTimer: (id) => timers.delete(id),
    },
  )

  const firstRun = controller.run({ q: 'first' })
  const secondRun = controller.run({ q: 'second' })
  first.resolve({ items: ['stale'] })
  await firstRun

  assert.equal(timers.size, 1)
  const activeWake = [...timers.values()][0]
  activeWake()
  assert.equal(controller.getState().waking, true)

  second.resolve({ items: ['active'] })
  await secondRun
})
