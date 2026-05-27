<template>
  <div class="gallery-page">
    <div class="page-header glass-card">
      <h1 class="page-title"><Image :size="28" />图片相册</h1>
      <p class="page-desc">记录美好瞬间</p>
    </div>

    <div v-if="gallery.length === 0" class="empty-state glass-card">
      <Image :size="64" />
      <h3>暂无图片</h3>
      <p>管理员可以在后台添加图片</p>
    </div>

    <div v-else class="gallery-grid">
      <div
        v-for="image in gallery"
        :key="image.id"
        class="gallery-item glass-card"
        @click="selectedItem = image"
      >
        <img :src="image.image_path" :alt="image.title" class="gallery-image" />
        <div class="image-overlay">
          <span class="image-title">{{ image.title || '未命名' }}</span>
        </div>
      </div>
    </div>

    <div v-if="selectedItem" class="popup-overlay" @click.self="selectedItem = null">
      <div class="popup-card">
        <button class="popup-close" @click="selectedItem = null">
          <X :size="20" />
        </button>
        <div class="popup-body">
          <div class="popup-image-side">
            <img :src="selectedItem.image_path" :alt="selectedItem.title" />
          </div>
          <div class="popup-info">
            <div class="popup-info-header">
              <Image :size="28" class="popup-icon" />
              <h2 class="popup-title">{{ selectedItem.title || '未命名' }}</h2>
            </div>
            <p class="popup-desc">{{ selectedItem.description || '暂无描述' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Image, X } from 'lucide-vue-next'

const gallery = ref([])
const selectedItem = ref(null)

onMounted(() => {
  fetch('/api/gallery').then(r => r.json()).then(d => { gallery.value = d })
})
</script>

<style scoped>
.gallery-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 100vh;
}

.page-header { padding: 30px; display: flex; flex-direction: column; gap: 8px; }
.page-title { display: flex; align-items: center; gap: 12px; font-size: 1.8rem; font-weight: 700; margin: 0; }
.page-desc { color: var(--text-secondary); margin: 0; }

.empty-state { padding: 60px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 16px; }
.empty-state h3 { font-size: 1.3rem; font-weight: 600; margin: 0; }
.empty-state p { color: var(--text-secondary); margin: 0; }

.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.gallery-item { position: relative; overflow: hidden; border-radius: 16px; cursor: pointer; }
.gallery-image { width: 100%; height: 240px; object-fit: cover; display: block; transition: transform 0.4s ease; }
.gallery-item:hover .gallery-image { transform: scale(1.1); }
.image-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 12px; background: linear-gradient(transparent, rgba(0,0,0,0.8)); opacity: 0; transition: opacity 0.3s ease; }
.gallery-item:hover .image-overlay { opacity: 1; }
.image-title { color: white; font-size: 13px; font-weight: 500; }

.popup-overlay { position: fixed; inset: 0; z-index: 1500; background: rgba(0,0,0,0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); display: flex; align-items: center; justify-content: center; padding: 20px; }
.popup-card { position: relative; max-width: 880px; width: 100%; max-height: 85vh; }
.popup-close { position: absolute; top: 14px; right: 14px; z-index: 10; width: 40px; height: 40px; border: none; background: rgba(255,255,255,0.12); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.15); }
.popup-close:hover { background: rgba(255,255,255,0.25); transform: rotate(90deg); }

.popup-body {
  display: flex;
  background: rgba(15,15,30,0.75);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05) inset;
}
.popup-image-side {
  width: 55%;
  flex-shrink: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  max-height: 75vh;
  overflow: hidden;
}
.popup-image-side img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.popup-info {
  flex: 1;
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  min-width: 0;
}
.popup-info-header {
  display: flex;
  align-items: center;
  gap: 14px;
}
.popup-icon { color: #a5b4fc; flex-shrink: 0; }
.popup-title { font-size: 1.4rem; font-weight: 700; color: white; margin: 0; }
.popup-desc {
  color: rgba(255,255,255,0.75);
  font-size: 0.95rem;
  line-height: 1.8;
  margin: 0;
  overflow-y: auto;
  max-height: 40vh;
}

@media (max-width: 768px) {
  .gallery-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .popup-body { flex-direction: column; max-width: 95vw; }
  .popup-image-side { width: 100%; min-height: 240px; max-height: 320px; }
  .popup-info { padding: 28px 24px; }
  .popup-title { font-size: 1.2rem; }
}
</style>