<template>
  <div class="admin-posts">
    <div class="page-header">
      <h1>文章管理</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <Plus :size="18" />
        新建文章
      </button>
    </div>
    
    <div class="posts-table glass-card">
      <table>
        <thead>
          <tr>
            <th>标题</th>
            <th>分类</th>
            <th>状态</th>
            <th>浏览量</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td class="post-title-cell">
              <span v-if="post.is_top" class="top-tag">置顶</span>
              {{ post.title }}
            </td>
            <td>{{ post.category || '-' }}</td>
            <td>
              <span :class="['status-badge', post.is_published ? 'published' : 'draft']">
                {{ post.is_published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td>{{ post.views }}</td>
            <td>{{ formatDate(post.created_at) }}</td>
            <td class="actions">
              <button class="action-btn edit" @click="editPost(post)">
                <Edit :size="16" />
              </button>
              <button class="action-btn delete" @click="deletePost(post.id)">
                <Trash2 :size="16" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content glass-card" @click.stop>
        <div class="modal-header">
          <h2>{{ editingPost ? '编辑文章' : '新建文章' }}</h2>
          <button class="modal-close" @click="closeModal">
            <X :size="20" />
          </button>
        </div>
        
        <form class="post-form" @submit.prevent="submitPost">
          <div class="form-row">
            <div class="form-group">
              <label>标题</label>
              <input v-model="postForm.title" type="text" required placeholder="请输入文章标题" />
            </div>
            <div class="form-group">
              <label>别名 (slug)</label>
              <input v-model="postForm.slug" type="text" placeholder="URL别名" />
            </div>
          </div>
          
          <div class="form-group">
            <label>分类</label>
            <select v-model="postForm.category_id">
              <option value="">请选择分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>标签</label>
            <input v-model="postForm.tagsInput" type="text" placeholder="多个标签用逗号分隔" />
          </div>
          
          <div class="form-group">
            <label>摘要</label>
            <textarea v-model="postForm.excerpt" rows="3" placeholder="文章摘要"></textarea>
          </div>
          
          <div class="form-group">
            <label>内容</label>
            <textarea v-model="postForm.content" rows="10" placeholder="文章内容"></textarea>
          </div>
          
          <div class="form-row">
            <label class="checkbox-label">
              <input v-model="postForm.is_published" type="checkbox" />
              <span>发布文章</span>
            </label>
            <label class="checkbox-label">
              <input v-model="postForm.is_top" type="checkbox" />
              <span>置顶文章</span>
            </label>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn btn-primary">
              {{ editingPost ? '保存修改' : '发布文章' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Trash2, X } from 'lucide-vue-next'

const posts = ref([])
const categories = ref([])
const showCreateModal = ref(false)
const editingPost = ref(null)

const postForm = ref({
  title: '',
  slug: '',
  category_id: '',
  tagsInput: '',
  excerpt: '',
  content: '',
  is_published: false,
  is_top: false
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadPosts = () => {
  fetch('/api/admin/posts?per_page=100', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  })
    .then(res => res.json())
    .then(data => {
      posts.value = data.posts
    })
}

const loadCategories = () => {
  fetch('/api/categories')
    .then(res => res.json())
    .then(data => {
      categories.value = data
    })
}

const closeModal = () => {
  showCreateModal.value = false
  editingPost.value = null
  postForm.value = {
    title: '',
    slug: '',
    category_id: '',
    tagsInput: '',
    excerpt: '',
    content: '',
    is_published: false,
    is_top: false
  }
}

const editPost = (post) => {
  editingPost.value = post
  postForm.value = {
    title: post.title,
    slug: post.slug,
    category_id: post.category_id || '',
    tagsInput: post.tags.join(','),
    excerpt: post.excerpt || '',
    content: post.content,
    is_published: post.is_published,
    is_top: post.is_top
  }
  showCreateModal.value = true
}

const deletePost = (id) => {
  if (!confirm('确定要删除这篇文章吗？')) return
  
  fetch(`/api/posts/${id}`, {
    method: 'DELETE',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
  .then(res => res.json())
  .then(() => {
    loadPosts()
    window.dispatchEvent(new Event('blog:refreshStats'))
  })
}

const submitPost = () => {
  const tags = postForm.value.tagsInput.split(',').map(t => t.trim()).filter(t => t)
  
  const data = {
    title: postForm.value.title,
    slug: postForm.value.slug || postForm.value.title.toLowerCase().replace(/\s+/g, '-'),
    content: postForm.value.content,
    excerpt: postForm.value.excerpt,
    category_id: postForm.value.category_id || null,
    tags,
    is_published: postForm.value.is_published,
    is_draft: !postForm.value.is_published,
    is_top: postForm.value.is_top
  }
  
  const url = editingPost.value ? `/api/posts/${editingPost.value.id}` : '/api/posts'
  const method = editingPost.value ? 'PUT' : 'POST'
  
  fetch(url, {
    method,
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(() => {
    closeModal()
    loadPosts()
    window.dispatchEvent(new Event('blog:refreshStats'))
  })
}

onMounted(() => {
  loadPosts()
  loadCategories()
})
</script>

<style scoped>
.admin-posts {
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

.posts-table {
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
}

tbody td {
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

tbody tr:hover {
  background: rgba(255, 255, 255, 0.05);
}

.post-title-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.top-tag {
  background: var(--accent-color);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 13px;
}

.status-badge.published {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.status-badge.draft {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
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
  max-width: 800px;
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

.post-form {
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
.form-group select,
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

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 14px;
}

.checkbox-label input {
  width: auto;
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
  
  .posts-table {
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