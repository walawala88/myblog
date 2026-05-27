<template>
  <div class="admin-comments">
    <div class="page-header">
      <h1>评论管理</h1>
    </div>
    
    <div class="comments-list glass-card">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="comment-author">{{ comment.author_name }}</span>
          <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
          <button class="delete-btn" @click="deleteComment(comment.id)">
            <Trash2 :size="16" />
            删除
          </button>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <div v-if="comment.replies && comment.replies.length > 0" class="replies">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
            <span class="reply-author">{{ reply.author_name }}:</span>
            <span class="reply-content">{{ reply.content }}</span>
            <button class="delete-btn small" @click="deleteComment(reply.id)">
              <Trash2 :size="14" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Trash2 } from 'lucide-vue-next'

const comments = ref([])

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const loadComments = () => {
  fetch('/api/comments')
    .then(res => res.json())
    .then(data => {
      comments.value = data
    })
}

const deleteComment = (id) => {
  if (!confirm('确定要删除这条评论吗？')) return
  
  fetch(`/api/comments/${id}`, {
    method: 'DELETE',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
  .then(res => res.json())
  .then(() => {
    loadComments()
  })
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.admin-comments {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.comments-list {
  padding: 20px;
}

.comment-item {
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  margin-bottom: 15px;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
}

.comment-author {
  font-weight: 600;
}

.comment-time {
  color: var(--text-muted);
  font-size: 13px;
}

.delete-btn {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background: rgba(239, 68, 68, 0.2);
  border: none;
  border-radius: 6px;
  color: #ef4444;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.delete-btn.small {
  padding: 4px 8px;
  font-size: 12px;
}

.comment-content {
  color: var(--text-secondary);
  line-height: 1.6;
}

.replies {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.reply-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}

.reply-author {
  font-weight: 500;
  color: var(--accent-color);
}

.reply-content {
  flex: 1;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>