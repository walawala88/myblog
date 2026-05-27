<template>
  <div class="home-page">
    <!-- 轮播图 -->
    <div class="carousel glass-card">
      <div class="carousel-inner">
        <div 
          class="carousel-item" 
          v-for="(item, index) in carouselItems" 
          :key="index"
          :class="{ active: currentSlide === index }"
        >
          <div class="carousel-content">
            <span class="carousel-category">{{ item.category || '未分类' }}</span>
            <h3 class="carousel-title">{{ item.title }}</h3>
            <p class="carousel-excerpt">{{ item.excerpt }}</p>
            <button class="btn btn-primary carousel-btn" @click="$router.push(`/post/${item.slug}`)">
              阅读全文
            </button>
          </div>
        </div>
      </div>
      <div class="carousel-indicators">
        <span 
          v-for="(_, index) in carouselItems" 
          :key="index" 
          :class="['indicator', { active: currentSlide === index }]"
          @click="setSlide(index)"
        ></span>
      </div>
    </div>
    
    <!-- 最新文章 -->
    <section class="posts-section">
      <div class="section-header">
        <h2 class="section-title">最新文章</h2>
        <router-link to="/archive" class="view-all">查看全部</router-link>
      </div>
      
      <div class="posts-grid">
        <article 
          v-for="post in posts" 
          :key="post.id" 
          class="post-card glass-card"
          @click="$router.push(`/post/${post.slug}`)"
        >
          <div v-if="post.is_top" class="top-badge">
            <Pin :size="12" />
            置顶
          </div>
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
            <span v-for="tag in post.tags" :key="tag" class="tag">
              {{ tag }}
            </span>
          </div>
        </article>
      </div>
      
      <div v-if="hasMore" class="load-more">
        <button class="btn btn-secondary" @click="loadMore">
          <RefreshCw :size="16" />
          加载更多
        </button>
      </div>
    </section>
    
    <!-- 荣誉展示 -->
    <section class="honors-section" v-if="honors.length > 0">
      <div class="section-header">
        <h2 class="section-title">荣誉墙</h2>
        <router-link to="/honors" class="view-all">查看全部</router-link>
      </div>
      
      <div class="honors-grid">
        <div 
          v-for="honor in honors.slice(0, 4)" 
          :key="honor.id" 
          class="honor-card glass-card"
        >
          <div v-if="honor.image_path" class="honor-image">
            <img :src="honor.image_path" :alt="honor.title" />
          </div>
          <h4 class="honor-title">{{ honor.title }}</h4>
          <p class="honor-date">{{ formatDate(honor.date) }}</p>
        </div>
      </div>
    </section>
    
    <!-- 相册预览 -->
    <section class="gallery-section" v-if="gallery.length > 0">
      <div class="section-header">
        <h2 class="section-title">相册</h2>
        <router-link to="/gallery" class="view-all">查看全部</router-link>
      </div>
      
      <div class="gallery-grid">
        <div 
          v-for="image in gallery.slice(0, 6)" 
          :key="image.id" 
          class="gallery-item glass-card"
        >
          <img :src="image.image_path" :alt="image.title" />
          <span class="image-title">{{ image.title || '未命名' }}</span>
        </div>
      </div>
    </section>
    
    <!-- 幕布笔记 -->
    <section class="mubu-section" v-if="notes.length > 0">
      <div class="section-header">
        <h2 class="section-title">幕布笔记</h2>
        <router-link to="/mubu" class="view-all">查看全部</router-link>
      </div>
      <div class="notes-grid">
        <div v-for="note in notes.slice(0, 4)" :key="note.id" class="note-card glass-card" @click="openNote(note.url)">
          <div class="note-icon"><BookOpen :size="24" /></div>
          <div class="note-content">
            <h4 class="note-title">{{ note.title }}</h4>
            <p class="note-desc">{{ note.description }}</p>
          </div>
          <ExternalLink :size="16" class="note-link" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Heart, Calendar, Eye, Pin, RefreshCw, BookOpen, ExternalLink } from 'lucide-vue-next'

const posts = ref([])
const honors = ref([])
const gallery = ref([])
const notes = ref([])
const currentSlide = ref(0)
const hasMore = ref(true)
const page = ref(1)
let autoTimer = null

const carouselItems = computed(() => {
  return posts.value.slice(0, 3).map(post => ({
    title: post.title,
    excerpt: post.excerpt,
    category: post.category,
    slug: post.slug
  }))
})

onMounted(() => {
  fetchPosts()
  fetchHonors()
  fetchGallery()
  fetchNotes()
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})

const startAutoPlay = () => {
  stopAutoPlay()
  autoTimer = setInterval(() => {
    if (posts.value.length > 0) {
      currentSlide.value = (currentSlide.value + 1) % carouselItems.value.length
    }
  }, 4000)
}

const stopAutoPlay = () => {
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null }
}

const setSlide = (index) => {
  currentSlide.value = index
  startAutoPlay()
}

const fetchPosts = () => {
  fetch(`/api/posts?page=${page.value}&per_page=6`)
    .then(res => res.json())
    .then(data => {
      if (data.posts.length < 6) {
        hasMore.value = false
      }
      posts.value = [...posts.value, ...data.posts]
    })
}

const fetchHonors = () => {
  fetch('/api/honors')
    .then(res => res.json())
    .then(data => {
      honors.value = data
    })
}

const fetchGallery = () => {
  fetch('/api/gallery')
    .then(res => res.json())
    .then(data => {
      gallery.value = data
    })
}

const fetchNotes = () => {
  fetch('/api/mubu_notes')
    .then(res => res.json())
    .then(data => {
      notes.value = data
    })
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadMore = () => {
  page.value++
  fetchPosts()
}

const openNote = (url) => {
  if (url) window.open(url, '_blank')
}
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 100vh;
}

/* 轮播图 */
.carousel {
  position: relative;
  height: 200px;
  overflow: hidden;
  border-radius: 20px;
}

.carousel-inner {
  height: 100%;
}

.carousel-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease;
  display: flex;
  align-items: center;
  padding: 40px;
  box-sizing: border-box;
}

.carousel-item.active {
  opacity: 1;
}

.carousel-content {
  max-width: 600px;
}

.carousel-category {
  display: inline-block;
  background: rgba(99, 102, 241, 0.3);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-bottom: 12px;
}

.carousel-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 12px;
  line-height: 1.3;
}

.carousel-excerpt {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0 0 20px;
  line-height: 1.5;
}

.carousel-btn {
  gap: 8px;
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  width: 30px;
  border-radius: 5px;
  background: rgba(99, 102, 241, 0.8);
}

/* 文章区域 */
.posts-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0;
}

.view-all {
  color: var(--accent-color);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.view-all:hover {
  text-decoration: underline;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.post-card {
  padding: 24px;
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.top-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--accent-color);
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
}

.post-title {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0 0 10px;
  line-height: 1.4;
}

.post-excerpt {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 16px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.load-more {
  text-align: center;
  padding: 16px;
}

/* 荣誉墙 */
.honors-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.honors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.honor-card {
  padding: 16px;
  text-align: center;
}

.honor-image {
  width: 100%;
  height: 120px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
}

.honor-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.honor-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 6px;
}

.honor-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* 相册预览 */
.gallery-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}

.gallery-item {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  font-size: 0.8rem;
  color: white;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 幕布笔记 */
.mubu-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.note-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.note-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.note-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(99,102,241,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.note-content {
  flex: 1;
  min-width: 0;
}

.note-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0 0 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-link {
  color: var(--text-secondary);
  flex-shrink: 0;
}

.note-card:hover .note-link {
  color: var(--accent-color);
}

@media (max-width: 640px) {
  .home-page {
    gap: 16px;
  }
  
  .carousel {
    height: 180px;
  }
  
  .carousel-title {
    font-size: 1.5rem;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .honors-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>