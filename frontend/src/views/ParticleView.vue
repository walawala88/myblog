<template>
  <div class="particle-viewer">
    <iframe :src="src" class="particle-iframe" allow="camera; fullscreen" allowfullscreen></iframe>
    <button class="exit-btn" @click="exit">
      <ArrowLeft :size="18" />
      <span>返回博客</span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const nameMap = {
  'flower-butterfly': '花朵蝴蝶文字',
  'silk-flower': '昙花',
  'landscape': '千里江山图'
}

const src = computed(() => `/particles/${route.params.name}.html`)

const exit = () => {
  router.push('/particles')
}
</script>

<style scoped>
.particle-viewer {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: #000;
}

.particle-iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

.exit-btn {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 2001;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: rgba(255, 215, 0, 0.15);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 2px solid rgba(255, 215, 0, 0.5);
  border-radius: 16px;
  color: #ffd700;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.35s ease;
  box-shadow: 
    0 0 20px rgba(255, 215, 0, 0.2),
    0 4px 15px rgba(0, 0, 0, 0.3);
}

.exit-btn:hover {
  background: rgba(255, 215, 0, 0.25);
  color: #fff;
  border-color: rgba(255, 215, 0, 0.8);
  box-shadow: 
    0 0 30px rgba(255, 215, 0, 0.4),
    0 4px 20px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}
</style>
