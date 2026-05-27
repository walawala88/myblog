<template>
  <div class="admin-honors">
    <div class="page-header">
      <h1>荣誉墙管理</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <Plus :size="18" />
        添加荣誉
      </button>
    </div>
    
    <div class="honors-list">
      <div v-for="honor in honors" :key="honor.id" class="honor-card glass-card">
        <div class="honor-image" v-if="honor.image_path">
          <img :src="honor.image_path" :alt="honor.title" />
        </div>
        <div class="honor-content">
          <h3 class="honor-title">{{ honor.title }}</h3>
          <p class="honor-date">{{ formatDate(honor.date) }}</p>
          <p class="honor-description">{{ honor.description }}</p>
        </div>
        <div class="honor-actions">
          <button class="action-btn edit" @click="editHonor(honor)">
            <Edit :size="14" />
          </button>
          <button class="action-btn delete" @click="deleteHonor(honor.id)">
            <Trash2 :size="14" />
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingHonor ? '编辑荣誉' : '添加荣誉' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>
        
        <form class="honor-form" @submit.prevent="submitHonor">
          <div class="form-group">
            <label>荣誉名称</label>
            <input v-model="honorForm.title" type="text" required placeholder="请输入荣誉名称" />
          </div>
          
          <div class="form-group">
            <label>获得日期</label>
            <input v-model="honorForm.date" type="date" required />
          </div>
          
          <div class="form-group">
            <label>荣誉描述</label>
            <textarea v-model="honorForm.description" rows="4" placeholder="请描述这个荣誉..."></textarea>
          </div>
          
          <div class="form-group">
            <label>荣誉图片（可选）</label>
            <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
              <Upload :size="32" />
              <p>点击或拖拽图片到此处上传</p>
              <input ref="fileInput" type="file" accept="image/*" class="file-input" @change="handleFileSelect" />
            </div>
            <div v-if="previewImage" class="preview-container">
              <img :src="previewImage" class="preview-image" />
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary">
              {{ editingHonor ? '保存修改' : '添加荣誉' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Trash2, X, Upload } from 'lucide-vue-next'

const honors = ref([])
const showCreateModal = ref(false)
const editingHonor = ref(null)
const fileInput = ref(null)
const previewImage = ref('')

const honorForm = ref({
  title: '',
  date: '',
  description: ''
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

const loadHonors = () => {
  fetch('/api/honors')
    .then(res => res.json())
    .then(data => {
      honors.value = data.sort((a, b) => new Date(b.date) - new Date(a.date))
    })
}

const closeModal = () => {
  showCreateModal.value = false
  editingHonor.value = null
  honorForm.value = {
    title: '',
    date: '',
    description: ''
  }
  previewImage.value = ''
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    previewImage.value = URL.createObjectURL(file)
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files?.[0]
  if (file && file.type.startsWith('image/')) {
    previewImage.value = URL.createObjectURL(file)
    fileInput.value.files = event.dataTransfer.files
  }
}

const editHonor = (honor) => {
  editingHonor.value = honor
  honorForm.value = {
    title: honor.title,
    date: honor.date ? honor.date.split('T')[0] : '',
    description: honor.description || ''
  }
  previewImage.value = honor.image_path || ''
  showCreateModal.value = true
}

const deleteHonor = (id) => {
  if (!confirm('确定要删除这个荣誉吗？')) return
  
  fetch(`/api/honors/${id}`, {
    method: 'DELETE',
    headers: { 
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
  .then(() => {
    loadHonors()
  })
}

const submitHonor = async () => {
  if (editingHonor.value) {
    const formData = new FormData()
    formData.append('title', honorForm.value.title)
    formData.append('date', honorForm.value.date)
    formData.append('description', honorForm.value.description)
    if (fileInput.value.files?.[0]) {
      formData.append('image', fileInput.value.files[0])
    }
    
    fetch(`/api/honors/${editingHonor.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: formData
    })
    .then(() => {
      closeModal()
      loadHonors()
    })
  } else {
    const formData = new FormData()
    formData.append('title', honorForm.value.title)
    formData.append('date', honorForm.value.date)
    formData.append('description', honorForm.value.description)
    if (fileInput.value.files?.[0]) {
      formData.append('image', fileInput.value.files[0])
    }
    
    fetch('/api/honors', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: formData
    })
    .then(() => {
      closeModal()
      loadHonors()
    })
  }
}

onMounted(() => {
  loadHonors()
})
</script>

<style scoped>
.admin-honors {
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

.honors-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.honor-card {
  display: flex;
  gap: 20px;
  padding: 20px;
  position: relative;
}

.honor-image {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
}

.honor-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.honor-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.honor-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.honor-date {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}

.honor-description {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.honor-actions {
  display: flex;
  flex-direction: column;
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

.honor-form {
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

.form-group input[type="date"] {
  color-scheme: dark;
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 0, 0, 0.1);
}

.upload-area:hover {
  border-color: var(--accent-color);
  background: rgba(99, 102, 241, 0.1);
}

.upload-area p {
  margin-top: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.file-input {
  display: none;
}

.preview-container {
  margin-top: 12px;
}

.preview-image {
  width: 100%;
  max-height: 150px;
  object-fit: contain;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

@media (max-width: 768px) {
  .honor-card {
    flex-direction: column;
  }
  
  .honor-image {
    width: 100%;
    height: 150px;
  }
  
  .honor-actions {
    flex-direction: row;
    justify-content: flex-end;
  }
}
</style>
