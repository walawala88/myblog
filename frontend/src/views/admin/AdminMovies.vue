<template>
  <div class="admin-movies">
    <div class="page-header">
      <h1>
        <Film :size="24" />
        电影管理
      </h1>
      <button class="btn btn-primary" @click="openCreateModal">
        <Plus :size="18" />
        新增电影
      </button>
    </div>

    <div class="movies-table glass-card">
      <table>
        <thead>
          <tr>
            <th class="col-poster">海报</th>
            <th>片名</th>
            <th>导演</th>
            <th>年份</th>
            <th>类型</th>
            <th>评分</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="movie in movies" :key="movie.id">
            <td class="col-poster">
              <img
                v-if="movie.poster"
                :src="movie.poster"
                :alt="movie.title"
                class="poster-thumb"
              />
              <div v-else class="poster-placeholder">
                <Film :size="20" />
              </div>
            </td>
            <td class="movie-title-cell">{{ movie.title }}</td>
            <td>{{ movie.director || '-' }}</td>
            <td>{{ movie.year || '-' }}</td>
            <td>{{ movie.genre || '-' }}</td>
            <td>
              <span class="rating-badge" v-if="movie.rating !== null && movie.rating !== undefined">
                {{ movie.rating }}
              </span>
              <span v-else>-</span>
            </td>
            <td class="actions">
              <button class="action-btn edit" @click="editMovie(movie)">
                <Edit2 :size="16" />
              </button>
              <button class="action-btn delete" @click="deleteMovie(movie.id)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingMovie ? '编辑电影' : '新增电影' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>

        <form class="movie-form" @submit.prevent="submitMovie">
          <div class="form-row">
            <div class="form-group">
              <label>片名 *</label>
              <input v-model="movieForm.title" type="text" required placeholder="请输入电影片名" />
            </div>
            <div class="form-group">
              <label>海报图片</label>
              <div class="file-input-wrapper">
                <label class="file-input-label">
                  <Upload :size="16" />
                  <span>{{ movieForm.posterFile ? movieForm.posterFile.name : '选择海报图片' }}</span>
                  <input type="file" accept="image/png,image/jpeg,image/gif" @change="onPosterChange" />
                </label>
              </div>
              <div v-if="editingMovie && editingMovie.poster && !movieForm.posterFile" class="current-poster">
                <span>当前海报：</span>
                <img :src="editingMovie.poster" class="poster-preview" />
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>导演</label>
              <input v-model="movieForm.director" type="text" placeholder="请输入导演姓名" />
            </div>
            <div class="form-group">
              <label>年份</label>
              <input v-model="movieForm.year" type="number" placeholder="请输入上映年份" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>类型</label>
              <input v-model="movieForm.genre" type="text" placeholder="如：科幻、剧情、动画" />
            </div>
            <div class="form-group">
              <label>评分 (0-10)</label>
              <input
                v-model.number="movieForm.rating"
                type="number"
                min="0"
                max="10"
                step="0.1"
                placeholder="请输入评分"
              />
            </div>
          </div>

          <div class="form-group">
            <label>简介</label>
            <textarea v-model="movieForm.description" rows="3" placeholder="请输入电影简介"></textarea>
          </div>

          <div class="form-group">
            <label>影评</label>
            <textarea v-model="movieForm.review" rows="6" placeholder="请输入影评内容"></textarea>
          </div>

          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? '提交中...' : (editingMovie ? '保存修改' : '新增电影') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit2, Trash2, X, Film, Upload } from 'lucide-vue-next'

const movies = ref([])
const showModal = ref(false)
const editingMovie = ref(null)
const submitting = ref(false)

const movieForm = ref({
  title: '',
  posterFile: null,
  director: '',
  year: '',
  genre: '',
  rating: '',
  description: '',
  review: ''
})

const getToken = () => localStorage.getItem('token')

const loadMovies = () => {
  fetch('/api/movies')
    .then(res => res.json())
    .then(data => {
      movies.value = data
    })
    .catch(err => console.error('加载电影列表失败:', err))
}

const openCreateModal = () => {
  editingMovie.value = null
  resetForm()
  showModal.value = true
}

const resetForm = () => {
  movieForm.value = {
    title: '',
    posterFile: null,
    director: '',
    year: '',
    genre: '',
    rating: '',
    description: '',
    review: ''
  }
}

const closeModal = () => {
  showModal.value = false
  editingMovie.value = null
  resetForm()
}

const onPosterChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    movieForm.value.posterFile = file
  }
}

const editMovie = (movie) => {
  editingMovie.value = movie
  movieForm.value = {
    title: movie.title || '',
    posterFile: null,
    director: movie.director || '',
    year: movie.year || '',
    genre: movie.genre || '',
    rating: movie.rating !== null && movie.rating !== undefined ? movie.rating : '',
    description: movie.description || '',
    review: movie.review || ''
  }
  showModal.value = true
}

const deleteMovie = (id) => {
  if (!confirm('确定要删除这部电影吗？')) return

  fetch(`/api/movies/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getToken()}`
    }
  })
    .then(res => res.json())
    .then(() => {
      loadMovies()
    })
}

const submitMovie = () => {
  submitting.value = true

  const formData = new FormData()
  formData.append('title', movieForm.value.title)
  formData.append('director', movieForm.value.director || '')
  formData.append('year', movieForm.value.year || '')
  formData.append('genre', movieForm.value.genre || '')
  formData.append('rating', movieForm.value.rating !== '' ? movieForm.value.rating : '')
  formData.append('description', movieForm.value.description || '')
  formData.append('review', movieForm.value.review || '')

  if (movieForm.value.posterFile) {
    formData.append('poster', movieForm.value.posterFile)
  }

  const url = editingMovie.value ? `/api/movies/${editingMovie.value.id}` : '/api/movies'
  const method = editingMovie.value ? 'PUT' : 'POST'

  fetch(url, {
    method,
    headers: {
      'Authorization': `Bearer ${getToken()}`
    },
    body: formData
  })
    .then(res => {
      if (!res.ok) throw new Error('操作失败')
      return res.json()
    })
    .then(() => {
      closeModal()
      loadMovies()
    })
    .catch(err => console.error('提交电影失败:', err))
    .finally(() => {
      submitting.value = false
    })
}

onMounted(() => {
  loadMovies()
})
</script>

<style scoped>
.admin-movies {
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
  display: flex;
  align-items: center;
  gap: 10px;
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

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.movies-table {
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
  vertical-align: middle;
}

tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.col-poster {
  width: 60px;
}

.poster-thumb {
  width: 48px;
  height: 68px;
  object-fit: cover;
  border-radius: 4px;
}

.poster-placeholder {
  width: 48px;
  height: 68px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.movie-title-cell {
  font-weight: 500;
}

.rating-badge {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
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

.movie-form {
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
  font-family: inherit;
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

.current-poster {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.poster-preview {
  width: 48px;
  height: 68px;
  border-radius: 4px;
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

  .movies-table {
    font-size: 13px;
  }

  thead th,
  tbody td {
    padding: 10px 8px;
  }

  .actions {
    flex-direction: column;
  }
}
</style>