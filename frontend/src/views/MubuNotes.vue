<template>
  <main class="main-content">
    <div class="page-header glass-card">
      <h1 class="page-title">
        <BookOpen :size="28" />
        幕布笔记分享
      </h1>
      <p class="page-desc">分享我的学习笔记和知识整理</p>
    </div>
    
    <div v-if="notes.length === 0" class="empty-state glass-card">
      <FileText :size="64" />
      <h3>暂无笔记</h3>
      <p>管理员可以在后台添加幕布笔记链接</p>
    </div>
    
    <div v-else class="notes-grid">
      <div 
        v-for="note in notes" 
        :key="note.id" 
        class="note-card glass-card"
        @click="openNote(note)"
      >
        <div class="note-icon">
          <FileText :size="32" />
        </div>
        <div class="note-content">
          <h3 class="note-title">{{ note.title }}</h3>
          <p class="note-description">{{ note.description }}</p>
          <div class="note-meta">
            <span class="note-date">{{ formatDate(note.created_at) }}</span>
          </div>
        </div>
        <div class="note-arrow">
          <ExternalLink :size="20" />
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { BookOpen, FileText, ExternalLink } from 'lucide-vue-next'

const notes = ref([])

onMounted(() => {
  fetchNotes()
})

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

const openNote = (note) => {
  window.open(note.url, '_blank')
}
</script>

<style scoped>
.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 100vh;
  padding: 20px 0;
  max-width: 1134px;
  margin: 0 auto;
  width: 100%;
  padding-left: 24px;
  padding-right: 24px;
  box-sizing: border-box;
}

.page-header {
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.page-desc {
  color: var(--text-secondary);
  margin: 0;
}

.empty-state {
  padding: 60px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-state h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0;
}

.empty-state p {
  color: var(--text-secondary);
  margin: 0;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.note-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.note-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.note-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: rgba(99, 102, 241, 0.2);
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
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 6px;
}

.note-description {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-meta {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.note-arrow {
  color: var(--text-secondary);
  transition: transform 0.3s ease;
}

.note-card:hover .note-arrow {
  transform: translateX(4px);
}

@media (max-width: 640px) {
  .main-content {
    padding-left: 16px;
    padding-right: 16px;
    gap: 16px;
  }
  
  .notes-grid {
    grid-template-columns: 1fr;
  }
}
</style>