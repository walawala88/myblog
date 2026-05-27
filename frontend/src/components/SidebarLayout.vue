<template>
  <div class="page-layout">
    <aside class="sidebar-left">
      <div class="profile-card glass-card">
        <div class="avatar-wrapper">
          <img src="/avatar.jpg" alt="头像" class="avatar" />
          <div class="status-dot"></div>
        </div>
        <h2 class="profile-name">{{ profile.name }}</h2>
        <p class="profile-bio">{{ profile.bio }}</p>
        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value">{{ stats.posts }}</span>
            <span class="stat-label">文章</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.comments }}</span>
            <span class="stat-label">评论</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.visitors }}</span>
            <span class="stat-label">访客</span>
          </div>
        </div>
        <button class="like-btn" :class="{ liked: liked }" @click="handleLike">
          <Heart :size="18" :fill="liked ? 'currentColor' : 'none'" />
          <span>{{ stats.likes }}</span>
        </button>
      </div>

      <div class="nav-menu glass-card">
        <h3 class="section-title"><Navigation :size="18" />导航菜单</h3>
        <ul>
          <li><router-link to="/" exact-active-class="active" :class="['nav-item', { active: $route.path === '/' }]"><HomeIcon :size="16" />首页</router-link></li>
          <li><router-link to="/gallery" :class="['nav-item', { active: $route.path === '/gallery' }]"><Image :size="16" />相册</router-link></li>
          <li><router-link to="/honors" :class="['nav-item', { active: $route.path === '/honors' }]"><Award :size="16" />荣誉墙</router-link></li>
          <li><router-link to="/mubu" :class="['nav-item', { active: $route.path === '/mubu' }]"><BookOpen :size="16" />幕布笔记</router-link></li>
          <li><router-link to="/hobbies" :class="['nav-item', { active: $route.path === '/hobbies' }]"><Heart :size="16" />爱好</router-link></li>
          <li><router-link to="/particles" :class="['nav-item', { active: $route.path.startsWith('/particles') }]"><Sparkles :size="16" />vibecoding作品</router-link></li>
          <li><router-link to="/message" :class="['nav-item', { active: $route.path === '/message' }]"><MessageSquare :size="16" />留言板</router-link></li>
        </ul>
      </div>

      <div class="category-list glass-card">
        <h3 class="section-title"><Folder :size="18" />文章分类</h3>
        <ul>
          <li v-for="cat in categories" :key="cat.id">
            <router-link :to="`/category/${cat.id}`" class="category-item">
              <span>{{ cat.name }}</span>
              <span class="cat-count">{{ cat.count }}</span>
            </router-link>
          </li>
        </ul>
      </div>
    </aside>

    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Heart, Navigation, HomeIcon, Image, Award, BookOpen, MessageSquare, Folder, Sparkles } from 'lucide-vue-next'

const profile = ref({ name: '博主', bio: '字节之外，还有山海与风' })
const stats = ref({ posts: 0, comments: 0, visitors: 0 })
const categories = ref([])
const liked = ref(false)

const loadStats = () => {
  fetch('/api/stats').then(r => r.json()).then(d => { stats.value = d })
}

const loadCategories = () => {
  fetch('/api/categories').then(r => r.json()).then(d => { categories.value = d })
}

const handleRefresh = () => {
  loadStats()
  loadCategories()
}

onMounted(() => {
  loadStats()
  loadCategories()
  window.addEventListener('blog:refreshStats', handleRefresh)
})

onUnmounted(() => {
  window.removeEventListener('blog:refreshStats', handleRefresh)
})

const handleLike = () => {
  if (liked.value) return
  liked.value = true
  fetch('/api/blogger/like', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
    .then(r => r.json())
    .then(data => { if (data.likes) stats.value.likes = data.likes })
}
</script>

<style scoped>
.page-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 20px;
  max-width: 1134px;
  margin: 0 auto;
  padding: 0 24px;
  min-height: calc(100vh - 76px);
  padding-top: 20px;
  padding-bottom: 20px;
}

.sidebar-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 76px;
  max-height: calc(100vh - 96px);
  overflow-y: auto;
  overflow-x: hidden;
}

.profile-card { padding: 20px; text-align: center; }
.avatar-wrapper { position: relative; width: 100px; height: 100px; margin: 0 auto 16px; }
.avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid rgba(255,255,255,0.2); }
.status-dot { position: absolute; bottom: 4px; right: 4px; width: 20px; height: 20px; background: #22c55e; border-radius: 50%; border: 3px solid rgba(255,255,255,0.1); }
.profile-name { font-size: 1.3rem; font-weight: 700; margin: 0 0 8px; }
.profile-bio { font-size: 0.9rem; color: var(--text-secondary); margin: 0 0 20px; }
.profile-stats { display: flex; justify-content: center; gap: 24px; margin-bottom: 20px; }
.stat-item { text-align: center; }
.stat-value { display: block; font-size: 1.3rem; font-weight: 700; }
.stat-label { font-size: 0.8rem; color: var(--text-secondary); }

.like-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 10px; margin-top: 16px;
  background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 20px; color: #ef4444; font-size: 0.9rem; cursor: pointer; transition: all 0.3s ease;
}
.like-btn:hover { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); transform: translateY(-1px); }
.like-btn.liked { background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.4); }

.nav-menu { padding: 16px; }
.nav-menu ul { list-style: none; padding: 0; margin: 0; }
.nav-menu li { margin-bottom: 8px; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px; color: var(--text-primary); text-decoration: none; transition: all 0.3s ease; font-size: 0.9rem; }
.nav-item:hover { background: rgba(255,255,255,0.08); }
.nav-item.active { background: rgba(99,102,241,0.2); color: #818cf8; }

.section-title { display: flex; align-items: center; gap: 8px; font-size: 0.95rem; font-weight: 600; margin: 0 0 16px; color: var(--text-secondary); }

.category-list { padding: 16px; }
.category-list ul { list-style: none; padding: 0; margin: 0; }
.category-list li { margin-bottom: 4px; }
.category-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; border-radius: 8px; color: var(--text-primary); text-decoration: none; transition: all 0.3s ease; font-size: 0.9rem; cursor: pointer; min-height: 40px; }
.category-item:hover { background: rgba(99,102,241,0.15); color: #a5b4fc; }
.category-item.router-link-active { background: rgba(99,102,241,0.2); color: #818cf8; }
.cat-count { font-size: 0.8rem; color: var(--text-muted); background: rgba(99,102,241,0.2); padding: 2px 10px; border-radius: 10px; flex-shrink: 0; }

.main-content { display: flex; flex-direction: column; gap: 24px; min-width: 0; }

@media (max-width: 1024px) {
  .page-layout { grid-template-columns: 1fr; }
  .sidebar-left { position: static; flex-direction: row; flex-wrap: wrap; justify-content: center; }
  .profile-card { width: 280px; }
  .nav-menu, .category-list { width: calc(50% - 10px); min-width: 200px; }
}
@media (max-width: 640px) {
  .page-layout { padding: 0 16px; gap: 16px; }
  .sidebar-left { flex-direction: column; align-items: stretch; }
  .profile-card, .nav-menu, .category-list { width: 100%; min-width: auto; }
}
</style>