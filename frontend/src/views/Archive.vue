<template>
  <div class="archive-page">
    <div class="page-content glass-card">
      <h1 class="page-title">
        <ArchiveIcon :size="28" />
        时间归档
      </h1>
      
      <div class="archive-content">
        <div 
          v-for="(posts, month) in archive" 
          :key="month" 
          class="archive-group"
        >
          <div class="month-header">
            <span class="month-label">{{ formatMonth(month) }}</span>
            <span class="post-count">{{ posts.length }} 篇文章</span>
          </div>
          
          <ul class="post-list">
            <li v-for="post in posts" :key="post.id">
              <router-link :to="`/post/${post.slug}`" class="post-link">
                <Calendar :size="14" class="post-calendar" />
                <span class="post-title">{{ post.title }}</span>
                <span class="post-date">{{ formatDay(post.created_at) }}</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Archive as ArchiveIcon, Calendar } from 'lucide-vue-next'

const archive = ref({})

const formatMonth = (month) => {
  const [year, m] = month.split('-')
  return `${year}年${parseInt(m)}月`
}

const formatDay = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getDate()}日`
}

onMounted(() => {
  fetch('/api/archive')
    .then(res => res.json())
    .then(data => {
      archive.value = data
    })
})
</script>

<style scoped>
.archive-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-content {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 30px;
}

.archive-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.archive-group {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 20px;
}

.archive-group:last-child {
  border-bottom: none;
}

.month-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.month-label {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--accent-color);
}

.post-count {
  color: var(--text-muted);
  font-size: 13px;
}

.post-list {
  list-style: none;
}

.post-list li {
  margin-bottom: 12px;
}

.post-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-secondary);
  transition: all 0.3s ease;
  padding: 10px 15px;
  border-radius: 8px;
}

.post-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.post-calendar {
  color: var(--accent-color);
}

.post-title {
  flex: 1;
}

.post-date {
  color: var(--text-muted);
  font-size: 13px;
}

@media (max-width: 768px) {
  .archive-page {
    padding: 10px;
  }
  
  .page-content {
    padding: 20px;
  }
}
</style>