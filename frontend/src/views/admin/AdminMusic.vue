<template>
  <div class="admin-music">
    <div class="page-header">
      <h1>音乐管理</h1>
      <button class="btn btn-primary" @click="openCreateModal">
        <Plus :size="18" />
        新增音乐
      </button>
    </div>

    <div class="music-table glass-card">
      <table>
        <thead>
          <tr>
            <th>标题</th>
            <th>艺术家</th>
            <th>专辑</th>
            <th>类型</th>
            <th>描述</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="song in songs" :key="song.id">
            <td class="title-cell">
              <img v-if="song.cover_path" :src="song.cover_path" class="cover-thumb" />
              <span>{{ song.title }}</span>
            </td>
            <td>{{ song.artist || '-' }}</td>
            <td>{{ song.album || '-' }}</td>
            <td>{{ song.genre || '-' }}</td>
            <td class="desc-cell">{{ song.description || '-' }}</td>
            <td class="actions">
              <button class="action-btn edit" @click="editSong(song)">
                <Edit2 :size="16" />
              </button>
              <button class="action-btn delete" @click="deleteSong(song.id)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
          <tr v-if="songs.length === 0">
            <td colspan="6" class="empty-row">暂无音乐，点击"新增音乐"添加</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingSong ? '编辑音乐' : '新增音乐' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>

        <form class="music-form" @submit.prevent="submitSong">
          <div class="form-row">
            <div class="form-group">
              <label>标题 *</label>
              <input v-model="form.title" type="text" required placeholder="请输入歌曲标题" />
            </div>
            <div class="form-group">
              <label>艺术家</label>
              <input v-model="form.artist" type="text" placeholder="艺术家名称" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>专辑</label>
              <input v-model="form.album" type="text" placeholder="专辑名称" />
            </div>
            <div class="form-group">
              <label>类型</label>
              <input v-model="form.genre" type="text" placeholder="如：流行、古典、电子" />
            </div>
          </div>

          <div class="form-group">
            <label>描述</label>
            <textarea v-model="form.description" rows="3" placeholder="歌曲描述"></textarea>
          </div>

          <div class="form-group">
            <label>{{ editingSong ? '替换音乐文件（可选）' : '音乐文件 *' }}</label>
            <div class="file-input-wrapper">
              <label class="file-input-label">
                <Upload :size="16" />
                <span>{{ form.file ? form.file.name : '选择MP3文件' }}</span>
                <input type="file" accept="audio/mpeg,audio/wav,audio/flac,audio/aac" @change="onFileChange" :required="!editingSong" />
              </label>
            </div>
          </div>

          <div class="form-group">
            <label>封面图片（可选）</label>
            <div class="file-input-wrapper">
              <label class="file-input-label">
                <Upload :size="16" />
                <span>{{ form.cover ? form.cover.name : '选择封面图片' }}</span>
                <input type="file" accept="image/png,image/jpeg,image/gif" @change="onCoverChange" />
              </label>
            </div>
            <div v-if="editingSong && editingSong.cover_path && !form.cover" class="current-cover">
              <span>当前封面：</span>
              <img :src="editingSong.cover_path" class="cover-preview" />
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? '提交中...' : (editingSong ? '保存修改' : '添加音乐') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit2, Trash2, X, Upload } from 'lucide-vue-next'

const songs = ref([])
const showModal = ref(false)
const editingSong = ref(null)
const submitting = ref(false)

const form = ref({
  title: '',
  artist: '',
  album: '',
  genre: '',
  description: '',
  file: null,
  cover: null
})

const getToken = () => localStorage.getItem('token')

const loadSongs = () => {
  fetch('/api/music')
    .then(res => res.json())
    .then(data => {
      songs.value = data
    })
}

const openCreateModal = () => {
  editingSong.value = null
  resetForm()
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingSong.value = null
  resetForm()
}

const resetForm = () => {
  form.value = {
    title: '',
    artist: '',
    album: '',
    genre: '',
    description: '',
    file: null,
    cover: null
  }
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.file = file
  }
}

const onCoverChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.cover = file
  }
}

const editSong = (song) => {
  editingSong.value = song
  form.value = {
    title: song.title || '',
    artist: song.artist || '',
    album: song.album || '',
    genre: song.genre || '',
    description: song.description || '',
    file: null,
    cover: null
  }
  showModal.value = true
}

const deleteSong = (id) => {
  if (!confirm('确定要删除这首音乐吗？')) return

  fetch(`/api/music/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(() => {
      loadSongs()
    })
}

const submitSong = () => {
  if (!editingSong.value && !form.value.file) return

  submitting.value = true

  const formData = new FormData()
  formData.append('title', form.value.title)
  formData.append('artist', form.value.artist)
  formData.append('album', form.value.album)
  formData.append('genre', form.value.genre)
  formData.append('description', form.value.description)

  if (form.value.file) {
    formData.append('file', form.value.file)
  }
  if (form.value.cover) {
    formData.append('cover', form.value.cover)
  }

  const url = editingSong.value ? `/api/music/${editingSong.value.id}` : '/api/music'
  const method = editingSong.value ? 'PUT' : 'POST'

  fetch(url, {
    method,
    headers: {
      'Authorization': `Bearer ${getToken()}`
    },
    body: formData
  })
    .then(res => res.json())
    .then(() => {
      closeModal()
      loadSongs()
    })
    .finally(() => {
      submitting.value = false
    })
}

onMounted(() => {
  loadSongs()
})
</script>

<style scoped>
.admin-music {
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
  color: var(--text-primary);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.music-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  text-align: left;
  padding: 15px;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  white-space: nowrap;
}

tbody td {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cover-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.desc-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-row {
  text-align: center;
  color: var(--text-secondary);
  padding: 40px 15px !important;
}

.actions {
  display: flex;
  gap: 10px;
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
  flex-shrink: 0;
}

.action-btn.edit {
  background: rgba(99, 102, 241, 0.2);
  color: var(--accent-color);
}

.action-btn.edit:hover {
  background: rgba(99, 102, 241, 0.3);
}

.action-btn.delete {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.3);
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
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.modal-header h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
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

.music-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
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
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
}

.form-group textarea {
  resize: vertical;
}

.file-input-wrapper {
  position: relative;
}

.file-input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-input-label:hover {
  border-color: rgba(99, 102, 241, 0.4);
  background: rgba(99, 102, 241, 0.05);
}

.file-input-label input[type="file"] {
  display: none;
}

.file-input-label span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.current-cover {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.cover-preview {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  object-fit: cover;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .music-table {
    font-size: 13px;
  }

  thead th,
  tbody td {
    padding: 10px 8px;
  }

  .actions {
    flex-direction: column;
  }

  .desc-cell {
    max-width: 100px;
  }
}
</style>