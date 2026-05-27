<template>
  <div class="honors-page">
    <div class="page-header glass-card">
      <h1 class="page-title"><Award :size="28" />荣誉展示墙</h1>
      <p class="page-desc">记录每一个值得骄傲的瞬间</p>
    </div>

    <div v-if="honors.length === 0" class="empty-state glass-card">
      <Award :size="64" />
      <h3>暂无荣誉</h3>
      <p>管理员可以在后台添加荣誉</p>
    </div>

    <div v-else class="honors-grid">
      <div v-for="honor in honors" :key="honor.id" class="honor-card glass-card" @click="selectedItem = honor">
        <div class="honor-card-icon">
          <Trophy :size="20" />
        </div>
        <div class="honor-card-img" v-if="honor.image_path">
          <img :src="honor.image_path" :alt="honor.title" />
        </div>
        <h3 class="honor-card-title">{{ honor.title }}</h3>
        <p class="honor-card-date">{{ formatDate(honor.date) }}</p>
        <p class="honor-card-desc">{{ honor.description }}</p>
      </div>
    </div>

    <div v-if="selectedItem" class="popup-overlay" @click.self="selectedItem = null">
      <div class="popup-card">
        <button class="popup-close" @click="selectedItem = null">
          <X :size="20" />
        </button>
        <div class="popup-body">
          <div v-if="selectedItem.image_path" class="popup-image-side">
            <img :src="selectedItem.image_path" :alt="selectedItem.title" />
          </div>
          <div :class="['popup-info', { 'full-width': !selectedItem.image_path }]">
            <div class="popup-info-header">
              <div class="popup-icon-wrap">
                <Trophy :size="24" />
              </div>
              <h2 class="popup-title">{{ selectedItem.title }}</h2>
            </div>
            <p v-if="selectedItem.date" class="popup-date">{{ formatDate(selectedItem.date) }}</p>
            <p class="popup-desc">{{ selectedItem.description || '暂无描述' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Award, Trophy, X } from 'lucide-vue-next'

const honors = ref([])
const selectedItem = ref(null)

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

onMounted(() => {
  fetch('/api/honors').then(r => r.json()).then(d => { honors.value = d.sort((a,b) => new Date(b.date) - new Date(a.date)) })
})
</script>

<style scoped>
.honors-page {
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

.honors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.honor-card {
  padding: 24px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}
.honor-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.25); }

.honor-card-icon {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c084fc, #ec4899);
  display: flex; align-items: center; justify-content: center;
  color: white; flex-shrink: 0;
}
.honor-card-img {
  width: 100%; height: 140px;
  border-radius: 12px; overflow: hidden;
}
.honor-card-img img { width: 100%; height: 100%; object-fit: cover; }
.honor-card-title { font-size: 1.05rem; font-weight: 600; margin: 0; }
.honor-card-date { font-size: 0.85rem; color: var(--accent-color); margin: 0; }
.honor-card-desc {
  font-size: 0.85rem; color: var(--text-secondary);
  line-height: 1.5; margin: 0;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

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
  gap: 16px;
  min-width: 0;
}
.popup-info.full-width {
  padding: 40px;
  align-items: center;
  text-align: center;
}
.popup-info-header {
  display: flex;
  align-items: center;
  gap: 14px;
}
.popup-icon-wrap {
  width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, #c084fc, #ec4899);
  display: flex; align-items: center; justify-content: center;
  color: white; flex-shrink: 0;
}
.popup-title { font-size: 1.4rem; font-weight: 700; color: white; margin: 0; }
.popup-date { font-size: 0.9rem; color: #c084fc; margin: 0; }
.popup-desc {
  color: rgba(255,255,255,0.75);
  font-size: 0.95rem;
  line-height: 1.8;
  margin: 0;
  overflow-y: auto;
  max-height: 40vh;
}

@media (max-width: 768px) {
  .honors-grid { grid-template-columns: 1fr; gap: 14px; }
  .popup-body { flex-direction: column; max-width: 95vw; }
  .popup-image-side { width: 100%; min-height: 200px; max-height: 280px; }
  .popup-info { padding: 28px 24px; }
  .popup-info.full-width { padding: 32px 24px; }
  .popup-title { font-size: 1.2rem; }
}
</style>