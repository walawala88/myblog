<template>
  <div class="category-page">
    <div class="page-content glass-card">
      <h1 class="page-title">
        <Folder :size="28" />
        {{ categoryName }}
      </h1>
      
      <div class="posts-list">
        <article 
          v-for="post in posts" 
          :key="post.id" 
          class="post-card glass-panel"
          @click="$router.push(`/post/${post.slug}`)"
        >
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-excerpt">{{ post.excerpt }}</p>
          <div class="post-meta">
            <span class="meta-item">
              <Calendar :size="14" />
              {{ formatDate(post.created_at) }}
            </span>
            <span class="meta-item">
              <Eye :size="14" />
              {{ post.views }}
            </span>
            <span class="meta-item">
              <Heart :size="14" />
              {{ post.likes }}
            </span>
          </div>
          <div class="post-tags">
            <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Folder, Calendar, Eye, Heart } from 'lucide-vue-next'

const posts = ref([])
const categoryName = ref('')
const route = useRoute()

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadCategoryData = (categoryId) => {
  fetch(`/api/posts?category_id=${categoryId}`)
    .then(res => res.json())
    .then(data => {
      posts.value = data.posts
    })
  
  fetch('/api/categories')
    .then(res => res.json())
    .then(data => {
      const category = data.find(c => c.id == categoryId)
      categoryName.value = category ? category.name : '未知分类'
    })
}

onMounted(() => {
  loadCategoryData(route.params.id)
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    loadCategoryData(newId)
  }
})
</script>

<style scoped>
.category-page {
  width: 100%;
}

.page-content {
  padding: 26px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 30px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.post-card {
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.post-excerpt {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-muted);
  font-size: 13px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: rgba(99, 102, 241, 0.15);
  color: var(--accent-color);
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
}

@media (max-width: 768px) {
  .category-page {
    padding: 10px;
  }
  
  .page-content {
    padding: 20px;
  }
}
</style>