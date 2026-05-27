<template>
  <div class="admin-page">
    <div class="video-background">
      <video autoplay muted loop playsinline>
        <source src="/lv_0_20260525143810.mp4" type="video/mp4">
      </video>
      <div class="video-overlay"></div>
    </div>
    
    <nav class="admin-nav glass-panel">
      <div class="nav-content">
        <router-link to="/admin" class="nav-brand">
          <Settings :size="20" />
          <span>管理后台</span>
        </router-link>
        
        <div class="nav-links">
          <router-link to="/admin" :class="['nav-link', { active: currentRoute === '/admin' }]">
            <FileText :size="16" /><span>文章</span>
          </router-link>
          <router-link to="/admin/comments" :class="['nav-link', { active: currentRoute === '/admin/comments' }]">
            <MessageCircle :size="16" /><span>评论</span>
          </router-link>
          <router-link to="/admin/gallery" :class="['nav-link', { active: currentRoute === '/admin/gallery' }]">
            <Image :size="16" /><span>相册</span>
          </router-link>
          <router-link to="/admin/honors" :class="['nav-link', { active: currentRoute === '/admin/honors' }]">
            <Award :size="16" /><span>荣誉</span>
          </router-link>
          <router-link to="/admin/mubu" :class="['nav-link', { active: currentRoute === '/admin/mubu' }]">
            <BookOpen :size="16" /><span>笔记</span>
          </router-link>
          <router-link to="/admin/movies" :class="['nav-link', { active: currentRoute === '/admin/movies' }]">
            <Film :size="16" /><span>电影</span>
          </router-link>
          <router-link to="/admin/music" :class="['nav-link', { active: currentRoute === '/admin/music' }]">
            <Music :size="16" /><span>音乐</span>
          </router-link>
          <router-link to="/admin/settings" :class="['nav-link', { active: currentRoute === '/admin/settings' }]">
            <Settings :size="16" /><span>设置</span>
          </router-link>
        </div>
        
        <button class="logout-btn" @click="logout">
          <LogOut :size="16" />
          <span>退出</span>
        </button>
      </div>
    </nav>
    
    <main class="admin-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Settings, FileText, MessageCircle, LogOut, Image, Award, BookOpen, Film, Music } from 'lucide-vue-next'

const router = useRouter()
const currentRoute = ref(window.location.pathname)

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  position: relative;
}

.video-background {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: -1;
  overflow: hidden;
}
.video-background video {
  width: 100%; height: 100%;
  object-fit: cover;
}
.video-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: linear-gradient(135deg, rgba(10,10,15,0.5), rgba(10,10,15,0.4), rgba(10,10,20,0.5));
}

.admin-nav {
  position: sticky;
  top: 0;
  width: calc(100% - 48px);
  max-width: 1200px;
  margin: 0 auto;
  z-index: 99;
  background: rgba(20,20,30,0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-top: none;
  border-radius: 0 0 16px 16px;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 20px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  text-decoration: none;
  color: var(--text-secondary);
  border-radius: 8px;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: rgba(255,255,255,0.08);
  color: var(--text-primary);
}

.nav-link.active {
  background: rgba(99,102,241,0.2);
  color: #818cf8;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 8px;
  color: #ef4444;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(239,68,68,0.15);
}

.admin-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 24px auto;
  padding: 0 24px 40px;
}

@media (max-width: 768px) {
  .admin-nav {
    width: calc(100% - 24px);
    border-radius: 0 0 12px 12px;
  }
  .nav-content {
    padding: 0 12px;
  }
  .nav-link {
    padding: 8px 10px;
    font-size: 0.8rem;
  }
  .nav-link span {
    display: none;
  }
  .logout-btn span {
    display: none;
  }
}
</style>