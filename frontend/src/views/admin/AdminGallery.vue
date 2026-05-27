<template>
  <div class="admin-gallery">
    <div class="page-header">
      <h1>图片相册管理</h1>
      <button class="btn btn-primary" @click="showUploadModal = true">
        <Plus :size="18" />
        上传图片
      </button>
    </div>
    
    <div class="gallery-grid">
      <div v-for="image in gallery" :key="image.id" class="gallery-item glass-card">
        <img :src="image.image_path" :alt="image.title" class="gallery-image" />
        <div class="image-info">
          <span class="image-title">{{ image.title || '未命名' }}</span>
          <div class="image-actions">
            <button class="action-btn edit" @click="editImage(image)">
              <Edit :size="14" />
            </button>
            <button class="action-btn delete" @click="deleteImage(image.id)">
              <Trash2 :size="14" />
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showUploadModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingImage ? '编辑图片' : '上传图片' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>
        
        <form class="upload-form" @submit.prevent="submitImage">
          <div class="form-group">
            <label>图片标题</label>
            <input v-model="imageForm.title" type="text" placeholder="请输入图片标题" />
          </div>
          
          <div class="form-group">
            <label>图片描述</label>
            <textarea v-model="imageForm.description" rows="3" placeholder="图片描述（可选）"></textarea>
          </div>
          
          <div v-if="!editingImage" class="form-group">
            <label>选择图片</label>
            <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
              <Upload :size="48" />
              <p>点击或拖拽图片到此处上传</p>
              <input ref="fileInput" type="file" accept="image/*" class="file-input" @change="handleFileSelect" />
            </div>
            <div v-if="previewImage" class="preview-container">
              <img :src="previewImage" class="preview-image" />
            </div>
          </div>
          
          <div v-if="editingImage" class="form-group">
            <label>当前图片</label>
            <img :src="editingImage.image_path" class="preview-image" />
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="!previewImage && !editingImage">
              {{ editingImage ? '保存修改' : '上传图片' }}
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

const gallery = ref([])
const showUploadModal = ref(false)
const editingImage = ref(null)
const fileInput = ref(null)
const previewImage = ref('')

const imageForm = ref({
  title: '',
  description: ''
})

const loadGallery = () => {
  fetch('/api/gallery')
    .then(res => res.json())
    .then(data => {
      gallery.value = data
    })
}

const closeModal = () => {
  showUploadModal.value = false
  editingImage.value = null
  imageForm.value = {
    title: '',
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

const editImage = (image) => {
  editingImage.value = image
  imageForm.value = {
    title: image.title || '',
    description: image.description || ''
  }
  showUploadModal.value = true
}

const deleteImage = (id) => {
  if (!confirm('确定要删除这张图片吗？')) return
  
  fetch(`/api/gallery/${id}`, {
    method: 'DELETE',
    headers: { 
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
  .then(() => {
    loadGallery()
  })
}

const submitImage = async () => {
  if (editingImage.value) {
    const data = {
      title: imageForm.value.title,
      description: imageForm.value.description
    }
    
    fetch(`/api/gallery/${editingImage.value.id}`, {
      method: 'PUT',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(data)
    })
    .then(() => {
      closeModal()
      loadGallery()
    })
  } else {
    const formData = new FormData()
    formData.append('title', imageForm.value.title)
    formData.append('description', imageForm.value.description)
    formData.append('image', fileInput.value.files[0])
    
    fetch('/api/gallery', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: formData
    })
    .then(() => {
      closeModal()
      loadGallery()
    })
  }
}

onMounted(() => {
  loadGallery()
})
</script>

<style scoped>
.admin-gallery {
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

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  aspect-ratio: 1;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-title {
  color: white;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn.edit {
  background: rgba(99, 102, 241, 0.8);
  color: white;
}

.action-btn.delete {
  background: rgba(239, 68, 68, 0.8);
  color: white;
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

.upload-form {
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

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 40px;
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
  margin-top: 10px;
  color: var(--text-secondary);
  font-size: 14px;
}

.file-input {
  display: none;
}

.preview-container {
  margin-top: 15px;
}

.preview-image {
  width: 100%;
  max-height: 200px;
  object-fit: contain;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
}
</style>
