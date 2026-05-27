<template>
  <div class="app-container">
    <div class="video-background">
      <video autoplay muted loop playsinline>
        <source src="/lv_0_20260525143810.mp4" type="video/mp4">
      </video>
      <div class="video-overlay"></div>
    </div>

    <template v-if="!isAuthPage && isAuthenticated">
      <nav v-if="!aiChatOpen" class="top-nav glass-panel">
        <div class="nav-content">
          <router-link to="/" class="nav-brand">
            <span>{{ siteName }}</span>
          </router-link>

          <div class="nav-links">
            <router-link to="/" class="nav-link">首页</router-link>
            <router-link to="/gallery" class="nav-link">相册</router-link>
            <router-link to="/honors" class="nav-link">荣誉墙</router-link>
            <router-link to="/mubu" class="nav-link">幕布笔记</router-link>
            <router-link to="/hobbies" class="nav-link">爱好</router-link>
            <router-link to="/particles" class="nav-link">vibecoding作品</router-link>
            <router-link to="/message" class="nav-link">留言板</router-link>
          </div>

          <div class="nav-actions">
            <button v-if="isLoggedIn" class="btn btn-outline-sm" @click="logout">退出</button>
            <button v-else-if="isVisitor" class="btn btn-outline-sm btn-visitor" @click="exitVisitor">退出游客模式</button>
          </div>
        </div>
      </nav>

      <main v-show="!aiChatOpen" class="app-main">
        <SidebarLayout>
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </SidebarLayout>
      </main>

      <MusicPlayer />
      <AIAssistant @update:visible="aiChatOpen = $event" />
    </template>

    <main v-if="isAuthPage" class="auth-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AIAssistant from './components/AIAssistant.vue'
import MusicPlayer from './components/MusicPlayer.vue'
import SidebarLayout from './components/SidebarLayout.vue'

const router = useRouter()
const route = useRoute()

const isLoggedIn = ref(!!localStorage.getItem('token'))
const isVisitor = ref(!!localStorage.getItem('visitor'))
const siteName = ref('My Blog')
const aiChatOpen = ref(false)

const isAuthPage = computed(() => {
  return route.path === '/login' || route.path.startsWith('/admin')
})

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token') || !!localStorage.getItem('visitor')
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('visitor')
  isLoggedIn.value = false
  isVisitor.value = false
  router.push('/login')
}

const exitVisitor = () => {
  localStorage.removeItem('visitor')
  isVisitor.value = false
  router.push('/login')
}

onMounted(() => {
  trackVisitor()
})

const trackVisitor = () => {
  const sessionKey = 'blog_visit_session'
  const visitTime = sessionStorage.getItem(sessionKey)
  const now = Date.now()
  if (visitTime && (now - parseInt(visitTime)) < 30 * 60 * 1000) {
    return
  }
  sessionStorage.setItem(sessionKey, now.toString())
  fetch('/api/visitor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page_url: window.location.pathname })
  }).catch(() => {})
}

fetch('/api/settings')
  .then(res => res.json())
  .then(settings => {
    if (settings.site_name) siteName.value = settings.site_name
  })
  .catch(() => {})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  position: relative;
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.video-background video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(10,10,15,0.5) 0%, rgba(10,10,15,0.4) 50%, rgba(10,10,20,0.5) 100%);
}

.top-nav {
  position: sticky;
  top: 0;
  width: calc(100% - 60px);
  max-width: 1134px;
  margin: 0 auto;
  z-index: 99;
  background: rgba(20, 20, 30, 0.85);
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
  padding: 0 24px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  padding: 6px 0;
  transition: color 0.3s ease;
  border-bottom: 2px solid transparent;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--text-primary);
  border-bottom-color: var(--accent-color);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-outline-sm {
  padding: 6px 16px;
  font-size: 0.8rem;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.08);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-outline-sm:hover {
  background: rgba(255,255,255,0.15);
  color: var(--text-primary);
}

.btn-visitor {
  border-color: rgba(99,102,241,0.3);
  background: rgba(99,102,241,0.1);
  color: #a5b4fc;
}

.btn-visitor:hover {
  background: rgba(99,102,241,0.2);
  color: #c7d2fe;
}

.app-main {
  position: relative;
  z-index: 1;
}

.auth-main {
  position: relative;
  z-index: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .top-nav { width: calc(100% - 24px); border-radius: 0 0 12px 12px; }
  .nav-links { gap: 12px; }
  .nav-link { font-size: 0.8rem; }
}
</style>