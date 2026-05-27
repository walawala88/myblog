<template>
  <div class="admin-mubu">
    <div class="page-header">
      <h1>幕布笔记管理</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <Plus :size="18" />
        添加笔记
      </button>
    </div>
    
    <div class="notes-table glass-card">
      <table>
        <thead>
          <tr>
            <th>标题</th>
            <th>链接</th>
            <th>描述</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="note in notes" :key="note.id">
            <td>{{ note.title }}</td>
            <td class="url-cell">
              <a :href="note.url" target="_blank" class="url-link">
                {{ note.url.slice(0, 30) }}{{ note.url.length > 30 ? '...' : '' }}
              </a>
            </td>
            <td>{{ note.description || '-' }}</td>
            <td>{{ formatDate(note.created_at) }}</td>
            <td class="actions-cell">
              <button class="action-btn edit" @click="editNote(note)">
                <Edit :size="14" />
              </button>
              <button class="action-btn delete" @click="deleteNote(note.id)">
                <Trash2 :size="14" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="notes.length === 0" class="empty-table">
        <FileText :size="48" />
        <p>暂无笔记，点击上方按钮添加</p>
      </div>
    </div>
    
    <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingNote ? '编辑笔记' : '添加幕布笔记' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>
        
        <form class="note-form" @submit.prevent="submitNote">
          <div class="form-group">
            <label>笔记标题 <span class="required">*</span></label>
            <input 
              v-model="noteForm.title" 
              type="text" 
              required 
              placeholder="请输入笔记标题" 
            />
          </div>
          
          <div class="form-group">
            <label>幕布笔记链接 <span class="required">*</span></label>
            <input 
              v-model="noteForm.url" 
              type="url" 
              required 
              placeholder="https://mubu.com/doc/..." 
            />
            <p class="hint">请输入幕布笔记的分享链接</p>
          </div>
          
          <div class="form-group">
            <label>笔记描述</label>
            <textarea 
              v-model="noteForm.description" 
              rows="3" 
              placeholder="简短描述这个笔记的内容..."
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary">
              {{ editingNote ? '保存修改' : '添加笔记' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Trash2, X, FileText } from 'lucide-vue-next'

const notes = ref([])
const showCreateModal = ref(false)
const editingNote = ref(null)

const noteForm = ref({
  title: '',
  url: '',
  description: ''
})

const loadNotes = () => {
  fetch('/api/mubu_notes')
    .then(res => res.json())
    .then(data => {
      notes.value = data
    })
}

const closeModal = () => {
  showCreateModal.value = false
  editingNote.value = null
  noteForm.value = {
    title: '',
    url: '',
    description: ''
  }
}

const editNote = (note) => {
  editingNote.value = note
  noteForm.value = {
    title: note.title,
    url: note.url,
    description: note.description || ''
  }
  showCreateModal.value = true
}

const deleteNote = (id) => {
  if (!confirm('确定要删除这个笔记吗？')) return
  
  fetch(`/api/mubu_notes/${id}`, {
    method: 'DELETE',
    headers: { 
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
  .then(() => {
    loadNotes()
  })
}

const submitNote = () => {
  if (editingNote.value) {
    fetch(`/api/mubu_notes/${editingNote.value.id}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(noteForm.value)
    })
    .then(() => {
      closeModal()
      loadNotes()
    })
  } else {
    fetch('/api/mubu_notes', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(noteForm.value)
    })
    .then(() => {
      closeModal()
      loadNotes()
    })
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
  loadNotes()
})
</script>

<style scoped>
.admin-mubu {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.notes-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.url-cell {
  max-width: 250px;
  overflow: hidden;
}

.url-link {
  color: var(--accent-color);
  text-decoration: none;
}

.url-link:hover {
  text-decoration: underline;
}

.actions-cell {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn.edit {
  background: rgba(99, 102, 241, 0.2);
  color: var(--accent-color);
}

.action-btn.delete {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.empty-table {
  padding: 60px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-table p {
  color: var(--text-secondary);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  padding: 30px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.modal-header h2 {
  font-size: 1.3rem;
  font-weight: 600;
}

.modal-close {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.note-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text-secondary);
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
}

.hint {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin: 6px 0 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .notes-table {
    font-size: 0.85rem;
  }
  
  th, td {
    padding: 10px 8px;
  }
  
  .url-cell {
    max-width: 150px;
  }
}
</style>
