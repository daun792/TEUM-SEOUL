# Frontend Event Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the `통합` branch frontend so home and list pages prioritize active/upcoming events, the calendar loads only its visible month, and users receive reliable search, pagination, loading, wake-up, retry, and mobile behavior.

**Architecture:** Keep the existing Vue component structure and FastAPI contract. Centralize date-range calculations, query serialization, request cancellation, and a 60-second in-memory cache in focused frontend modules, then connect each screen to the correct date window.

**Tech Stack:** Vue 3.5, Vue Router 5, FullCalendar 6, Vite 8, Node built-in test runner, Fetch API

## Global Constraints

- Use the `통합` branch frontend as the behavioral and visual baseline.
- Do not modify the backend, database schema, board, map, or chatbot API contract.
- Default home and list views to active/upcoming events; expose past events only through an explicit `지난 행사 포함` control.
- Calendar requests must be constrained to the currently visible date range.
- Keep dependencies unchanged; do not add a Vue test framework.
- Cache successful festival list requests for 60 seconds and share identical in-flight requests.
- Show a Render wake-up message after 8 seconds while allowing the request to continue.
- Search input debounce is 300ms; list page size is 24.

---

### Task 1: Date range utilities

**Files:**
- Create: `frontend/src/utils/dateRange.js`
- Test: `frontend/tests/dateRange.test.js`

**Interfaces:**
- Produces: `formatLocalDate(date): string`, `todayIso(now?): string`, `addDaysIso(isoDate, days): string`, `monthRange(date): { startDate, endDate }`, `calendarRange(start, exclusiveEnd): { startDate, endDate }`.

- [ ] **Step 1: Write failing tests** covering local date formatting, 90-day windows, leap-year month boundaries, and conversion of FullCalendar's exclusive end to an inclusive API end.
- [ ] **Step 2: Run `npm test -- tests/dateRange.test.js`** and confirm module-not-found failure.
- [ ] **Step 3: Implement pure date utilities** without UTC `toISOString()` conversions for user-visible dates.
- [ ] **Step 4: Run `npm test -- tests/dateRange.test.js`** and confirm all date tests pass.
- [ ] **Step 5: Commit** with `test: add festival date range utilities`.

### Task 2: Festival API query, cache, and cancellation

**Files:**
- Modify: `frontend/src/services/festivalsApi.js`
- Test: `frontend/tests/festivalsApi.test.js`

**Interfaces:**
- Consumes: existing `requestJson(path, options)` from `frontend/src/services/apiBase.js`.
- Produces: `getFestivalPage(params, options): Promise<{items,total,page,size,pages}>`, `getFestivalList(params, options): Promise<Festival[]>`, `clearFestivalCache(): void`.
- `params`: `q`, `startDate`, `endDate`, `page`, `size`.
- `options`: `signal`, `forceRefresh`.

- [ ] **Step 1: Write failing tests** for query serialization, response mapping, identical in-flight request sharing, 60-second cache reuse, cache bypass, and non-caching of rejected requests.
- [ ] **Step 2: Run `npm test -- tests/festivalsApi.test.js`** and confirm failures against the current implementation.
- [ ] **Step 3: Implement stable query serialization**, preserve existing field mapping, and return pagination metadata from `getFestivalPage`.
- [ ] **Step 4: Implement cache and in-flight request sharing**, while forwarding `AbortSignal` and excluding aborted/rejected requests from cache.
- [ ] **Step 5: Run the API tests** and confirm all pass.
- [ ] **Step 6: Commit** with `feat: add cached festival query service`.

### Task 3: Reusable async festival query state

**Files:**
- Create: `frontend/src/composables/useFestivalQuery.js`
- Test: `frontend/tests/festivalQueryState.test.js`

**Interfaces:**
- Consumes: an injected async loader returning a festival page.
- Produces: refs `data`, `loading`, `waking`, `error`; functions `run(params, options)`, `retry()`, `dispose()`.

- [ ] **Step 1: Write failing tests** against a framework-free controller exported as `createFestivalQueryController`, covering cancellation, stale-response suppression, 8-second waking state, retry, and disposal.
- [ ] **Step 2: Run the query-state test** and confirm failure.
- [ ] **Step 3: Implement the controller** and a thin Vue-ref wrapper `useFestivalQuery`.
- [ ] **Step 4: Run tests** and confirm the controller tests pass.
- [ ] **Step 5: Commit** with `feat: add festival request state controller`.

### Task 4: Festival list search and pagination

**Files:**
- Modify: `frontend/src/views/FestivalListView.vue`
- Modify: `frontend/src/services/festivalsApi.js` only if integration exposes a missing mapper

**Interfaces:**
- Consumes: `todayIso`, `getFestivalPage`, `useFestivalQuery`.
- URL query: `q`, `page`, `includePast`.

- [ ] **Step 1: Add a failing integration assertion script** that checks the component source for date-constrained default queries, 300ms debounce, `지난 행사 포함`, pagination controls, and retry state.
- [ ] **Step 2: Run the assertion script** and confirm failure on the original component.
- [ ] **Step 3: Replace the one-time 60-item fetch** with route-synchronized query state and a 24-item paginated API request.
- [ ] **Step 4: Add search, past-event checkbox, result count, empty state, wake-up state, error/retry UI, and accessible pagination controls.**
- [ ] **Step 5: Add responsive styles** for stacked controls and mobile-safe cards/calendar width.
- [ ] **Step 6: Run tests and build**; confirm list integration assertions and Vite compilation pass.
- [ ] **Step 7: Commit** with `feat: improve festival search and pagination`.

### Task 5: Home active/upcoming event section

**Files:**
- Modify: `frontend/src/components/home/WeeklyFestivalSection.vue`

**Interfaces:**
- Consumes: `todayIso`, `addDaysIso`, `getFestivalList`, `useFestivalQuery`.
- Query window: today through today + 90 days, size 18.

- [ ] **Step 1: Add failing source assertions** for the 90-day window, loading/waking/error/empty states, and retry action.
- [ ] **Step 2: Run assertions** and confirm the current component fails.
- [ ] **Step 3: Implement constrained active/upcoming loading** and preserve the current category filtering and card slider.
- [ ] **Step 4: Add explicit status states and retry UI** instead of silently replacing errors with an empty list.
- [ ] **Step 5: Run tests and build.**
- [ ] **Step 6: Commit** with `feat: prioritize upcoming festivals on home`.

### Task 6: Visible-range calendar loading

**Files:**
- Modify: `frontend/src/components/home/FestivalCalendarSection.vue`
- Modify: `frontend/src/views/FestivalListView.vue` calendar integration as needed

**Interfaces:**
- Consumes: `calendarRange`, `getFestivalList`, `useFestivalQuery`.
- FullCalendar callback: `datesSet(info)` where `info.end` is exclusive.

- [ ] **Step 1: Add failing source assertions** that reject hard-coded 2026 dates and require `datesSet` range loading.
- [ ] **Step 2: Run assertions** and confirm failure.
- [ ] **Step 3: Remove hard-coded selected and initial dates**, initialize selection from the local current date, and fetch only the visible calendar range.
- [ ] **Step 4: Prevent duplicate range calls**, cancel superseded requests, and preserve category filtering and event navigation.
- [ ] **Step 5: Add compact loading/waking/error feedback** without replacing the calendar shell.
- [ ] **Step 6: Run tests and build.**
- [ ] **Step 7: Commit** with `feat: load festivals by visible calendar month`.

### Task 7: End-to-end frontend verification and packaging

**Files:**
- Modify: `frontend/tests/frontendIntegration.test.js`
- Create: `docs/superpowers/specs/2026-07-16-frontend-event-discovery-design.md`
- Create: `docs/superpowers/plans/2026-07-16-frontend-event-discovery.md`

**Interfaces:**
- Produces: deployable frontend tree and patch archive for a Fork/Netlify deployment.

- [ ] **Step 1: Run `npm test`** and require zero failures.
- [ ] **Step 2: Run `npm run build`** and require exit code 0.
- [ ] **Step 3: Search for hard-coded `2026-07-18`, fixed `size: 60`, and fixed `size: 300` festival requests** and require no runtime occurrences.
- [ ] **Step 4: Verify Netlify configuration still builds from `frontend` and uses `VITE_API_BASE_URL`.**
- [ ] **Step 5: Create a ZIP containing the improved source and a smaller overlay patch ZIP.**
- [ ] **Step 6: Write a verification report** with commands, exit codes, test counts, build output, and deployment steps.
