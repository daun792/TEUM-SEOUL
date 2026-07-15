<script setup>
import { useRouter } from 'vue-router'
import mascotImage from '../../assets/chatbot-mascot.webp'

const router = useRouter()

const previewPosts = [
  { id: '1', title: '이번 주말 여의도 축제 사람 많을까요?', timeAgo: '12분 전', comments: 8, avatar: 'A' },
  { id: '2', title: '성수 근처 무료 전시 추천해요!', timeAgo: '1시간 전', comments: 3, avatar: 'B' },
  { id: '3', title: '아이와 함께 가기 좋은 체험 축제 있을까요?', timeAgo: '2시간 전', comments: 5, avatar: 'C' },
]
</script>

<template>
  <section class="community-section section-card">
    <header class="section-head">
      <h2>틈서울 익명 게시판</h2>
      <RouterLink to="/board">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <ul class="post-list">
      <li v-for="post in previewPosts" :key="post.id">
        <button type="button" class="post-button" @click="router.push(`/board/${post.id}`)">
          <span class="avatar-placeholder" aria-hidden="true">{{ post.avatar }}</span>
          <span class="post-copy">
            <strong>{{ post.title }}</strong>
            <small>{{ post.timeAgo }}　○ {{ post.comments }}</small>
          </span>
        </button>
      </li>
    </ul>

    <div class="helper-card">
      <div class="helper-copy">
        <strong>서울 축제 도우미</strong>
        <span>어디로 떠나볼까요?</span>
      </div>
      <img :src="mascotImage" alt="서울 축제 도우미" class="bot-avatar" />
    </div>
  </section>
</template>

<style scoped>
.community-section {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 18px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

h2 {
  margin: 0;
  color: #24372e;
  font-size: 20px;
  letter-spacing: -0.035em;
}

.section-head a {
  color: #6b756f;
  font-size: 12px;
  font-weight: 750;
}

.post-list {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid #e3e5de;
  border-radius: 14px;
  overflow: hidden;
}

.post-list li + li {
  border-top: 1px solid #ecece6;
}

.post-button {
  width: 100%;
  min-height: 84px;
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  padding: 12px 10px;
  border: 0;
  background: #fff;
  text-align: left;
  cursor: pointer;
}

.post-button:hover {
  background: #fbfcf8;
}

.avatar-placeholder {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border: 1.5px dashed #b9c9b2;
  border-radius: 50%;
  background: #f5f9f0;
  color: #7b8a75;
  font-size: 10px;
  font-weight: 900;
}

.post-copy {
  min-width: 0;
  display: grid;
  gap: 5px;
}

.post-copy strong {
  overflow: hidden;
  color: #34463d;
  font-size: 12px;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-copy small {
  color: #8a928d;
  font-size: 10px;
}

.helper-card {
  min-height: 92px;
  display: grid;
  grid-template-columns: 1fr 82px;
  align-items: center;
  gap: 8px;
  margin-top: auto;
  padding: 10px 9px 10px 14px;
  border: 1px solid #d9e9ce;
  border-radius: 18px;
  background: linear-gradient(135deg, #fbfff5, #f0f8e8);
}

.helper-copy {
  display: grid;
  gap: 3px;
}

.helper-copy strong {
  color: var(--color-primary-dark);
  font-size: 15px;
}

.helper-copy span {
  color: #5e7066;
  font-size: 11px;
}

.mascot-placeholder {
  width: 72px;
  height: 72px;
  border-radius: 50%;
}

.mascot-placeholder::after {
  content: '캐릭터';
  padding: 4px 7px;
  font-size: 9px;
}

@media (max-width: 1320px) {
  .helper-card {
    margin-top: 14px;
  }
}
</style>
