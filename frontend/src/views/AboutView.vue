<template>
	<main class="container about-page">
		<section class="section-card hero-card">
			<p class="eyebrow">틈서울 소개</p>
			<h1>서울의 축제와 주변 명소를 한 화면에</h1>
			<p class="desc">
				틈서울은 축제 일정 확인부터 주변 관광지, 문화시설, 쇼핑 정보까지 한 번에 탐색할 수 있는
				서울형 축제 탐색 서비스입니다.
			</p>
		</section>

		<section class="feature-grid">
			<article class="section-card feature-item">
				<h2>축제 캘린더</h2>
				<p>월별 축제 일정을 캘린더로 확인하고, 날짜별 축제 흐름을 빠르게 파악할 수 있습니다.</p>
			</article>

			<article class="section-card feature-item">
				<h2>지도 탐색</h2>
				<p>축제 주변 관광지, 문화시설, 쇼핑 장소를 필터로 좁혀서 직관적으로 확인할 수 있습니다.</p>
			</article>

			<article class="section-card feature-item">
				<h2>익명 게시판</h2>
				<p>참여자 후기와 질문을 익명으로 공유하며 축제 방문 전 실전 정보를 모을 수 있습니다.</p>
			</article>
		</section>
	</main>
</template>

<style scoped>
.about-page {
	padding: 24px 0 40px;
	display: grid;
	gap: 14px;
}

.hero-card {
	padding: 22px;
}

.eyebrow {
	margin: 0;
	width: fit-content;
	border-radius: var(--radius-pill);
	background: #ecf7e2;
	color: var(--color-primary-dark);
	padding: 6px 10px;
	font-size: 12px;
	font-weight: 800;
}

h1 {
	margin: 10px 0 0;
	color: #223b30;
	font-size: 34px;
	letter-spacing: -0.04em;
	line-height: 1.2;
}

.desc {
	margin: 12px 0 0;
	color: #4c6358;
	line-height: 1.65;
}

.feature-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 12px;
}

.feature-item {
	padding: 16px;
}

.feature-item h2 {
	margin: 0 0 8px;
	color: #2a4338;
	font-size: 20px;
}

.feature-item p {
	margin: 0;
	color: #60756c;
	line-height: 1.6;
}

@media (max-width: 1024px) {
	.feature-grid {
		grid-template-columns: 1fr;
	}
}

@media (max-width: 760px) {
	.about-page {
		padding-top: 18px;
	}

	h1 {
		font-size: 28px;
	}
}
</style>