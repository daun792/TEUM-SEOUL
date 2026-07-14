<script setup> 
  import { ref } from 'vue' 
  import { useRouter } from 'vue-router' 

  const router = useRouter() 
  const posts = ref([ { id: 1, title: '여름 음악축제 사람 많나요?', author: '익명', createdAt: '2026-07-14' }, 
    { id: 2, title: '한강 축제 근처 주차 팁 공유', author: '익명', createdAt: '2026-07-14' }, 
    { id: 3, title: '인사동 축제 체험 후기', author: '익명', createdAt: '2026-07-13' }, ]) 
  const goDetail = (id) => { router.push('/board/' + id) } 
  const goWrite = () => { router.push('/board/write') } 
</script> 
<template> 
  <section class="board"> 
    <div class="board-header"> 
      <h2>익명 게시판</h2> 
      <button type="button" @click="goWrite">글쓰기</button> 
    </div>
    <ul class="post-list">
      <li v-for="post in posts" :key="post.id" class="post-item" @click="goDetail(post.id)">
        <h3>{{ post.title }}</h3>
        <p>{{ post.author }} | {{ post.createdAt }}</p>
      </li>
    </ul>
  </section> 
</template> 
<style scoped> 
  .board { max-width: 900px; } 
  .board-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; } 
  .post-list { list-style: none; padding: 0; margin: 0; } 
  .post-item { border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; margin-bottom: 10px; cursor: pointer; } 
  .post-item h3 { margin: 0 0 6px; font-size: 16px; } 
  .post-item p { margin: 0; color: #6b7280; font-size: 14px; } 
</style>