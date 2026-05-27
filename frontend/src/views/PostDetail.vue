<template>
  <div class="post-detail">
    <article class="post-content glass-card">
      <header class="post-header">
        <span v-if="post.is_top" class="top-badge">
          <Pin :size="12" />
          置顶
        </span>
        <span class="category-tag">{{ post.category }}</span>
        <h1 class="post-title">{{ post.title }}</h1>
        <div class="post-meta">
          <span class="meta-item">
            <Calendar :size="14" />
            {{ formatDate(post.created_at) }}
          </span>
          <span class="meta-item">
            <Eye :size="14" />
            {{ post.views }}
          </span>
          <span class="meta-item">
            <Heart :size="14" />
            {{ post.likes }}
          </span>
        </div>
      </header>
      
      <div class="post-body" v-html="renderContent(post.content)"></div>
      
      <div class="post-tags">
        <span v-for="tag in post.tags" :key="tag" class="tag">
          <Tag :size="12" />
          {{ tag }}
        </span>
      </div>
      
      <div class="post-actions">
        <button 
          class="action-btn" 
          :class="{ liked: isLiked }"
          @click="handleLike"
        >
          <Heart :size="20" />
          <span>{{ post.likes }}</span>
        </button>
      </div>
    </article>
    
    <div class="comments-section glass-card">
      <h3 class="section-title">
        <MessageCircle :size="18" />
        评论 ({{ post.comments.length }})
      </h3>
      
      <div class="comment-form">
        <input 
          v-model="commentForm.author_name" 
          type="text" 
          placeholder="您的昵称"
          class="comment-input"
        />
        <input 
          v-model="commentForm.author_email" 
          type="email" 
          placeholder="您的邮箱（可选）"
          class="comment-input"
        />
        <textarea 
          v-model="commentForm.content" 
          placeholder="写下您的评论..."
          class="comment-textarea"
        ></textarea>
        <button class="btn btn-primary comment-submit" @click="submitComment">
          <Send :size="16" />
          发表评论
        </button>
      </div>
      
      <div class="comments-list">
        <div 
          v-for="comment in post.comments" 
          :key="comment.id" 
          class="comment-item"
        >
          <div class="comment-avatar">
            <User :size="32" />
          </div>
          <div class="comment-content">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author_name }}</span>
              <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p>{{ comment.content }}</p>
            <button class="reply-btn" @click="replyToComment(comment)">
              <Reply :size="14" />
              回复
            </button>
            
            <div v-if="comment.replies.length > 0" class="replies-list">
              <div 
                v-for="reply in comment.replies" 
                :key="reply.id" 
                class="reply-item"
              >
                <div class="reply-avatar">
                  <User :size="24" />
                </div>
                <div class="reply-content">
                  <div class="reply-header">
                    <span class="reply-author">{{ reply.author_name }}</span>
                    <span class="reply-time">{{ formatDate(reply.created_at) }}</span>
                  </div>
                  <p>{{ reply.content }}</p>
                </div>
              </div>
            </div>
            
            <div v-if="replyingTo === comment.id" class="reply-form">
              <textarea 
                v-model="replyContent" 
                placeholder="回复 {{ comment.author_name }}..."
                class="reply-textarea"
              ></textarea>
              <div class="reply-actions">
                <button class="btn btn-primary" @click="submitReply(comment.id)">回复</button>
                <button class="btn btn-secondary" @click="replyingTo = null">取消</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  Pin, Calendar, Eye, Heart, Tag,
  MessageCircle, Send, Reply, User 
} from 'lucide-vue-next'

const post = ref({
  id: 0,
  title: '',
  content: '',
  category: '',
  tags: [],
  views: 0,
  likes: 0,
  created_at: '',
  updated_at: '',
  comments: []
})

const isLiked = ref(false)
const replyingTo = ref(null)
const replyContent = ref('')

const commentForm = ref({
  author_name: '',
  author_email: '',
  content: ''
})

const renderContent = (content) => {
  return content.replace(/\n/g, '<br>')
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const handleLike = () => {
  fetch(`/api/posts/${post.value.id}/like`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
  .then(res => res.json())
  .then(data => {
    isLiked.value = data.liked
    if (data.liked) {
      post.value.likes++
    } else {
      post.value.likes--
    }
  })
}

const submitComment = () => {
  if (!commentForm.value.author_name || !commentForm.value.content) {
    alert('请填写昵称和评论内容')
    return
  }
  
  fetch('/api/comments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      post_id: post.value.id,
      author_name: commentForm.value.author_name,
      author_email: commentForm.value.author_email,
      content: commentForm.value.content
    })
  })
  .then(res => res.json())
  .then(() => {
    commentForm.value = { author_name: '', author_email: '', content: '' }
    loadPost()
  })
}

const replyToComment = (comment) => {
  replyingTo.value = replyingTo.value === comment.id ? null : comment.id
}

const submitReply = (parentId) => {
  if (!commentForm.value.author_name || !replyContent.value) {
    alert('请填写昵称和回复内容')
    return
  }
  
  fetch('/api/comments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      post_id: post.value.id,
      parent_id: parentId,
      author_name: commentForm.value.author_name,
      content: replyContent.value
    })
  })
  .then(res => res.json())
  .then(() => {
    replyContent.value = ''
    replyingTo.value = null
    loadPost()
  })
}

const loadPost = () => {
  const slug = window.location.pathname.split('/').pop()
  fetch(`/api/posts/${slug}`)
    .then(res => res.json())
    .then(data => {
      post.value = data
    })
}

onMounted(() => {
  loadPost()
})
</script>

<style scoped>
.post-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.post-content {
  padding: 26px;
}

.post-header {
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  padding-bottom: 20px;
}

.top-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--accent-color);
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 10px;
}

.category-tag {
  background: rgba(99, 102, 241, 0.2);
  color: var(--accent-color);
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 13px;
}

.post-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 20px 0 15px;
  line-height: 1.4;
}

.post-meta {
  display: flex;
  gap: 25px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
  font-size: 14px;
}

.post-body {
  line-height: 1.8;
  font-size: 15px;
  color: var(--text-primary);
}

.post-body p {
  margin-bottom: 1.5em;
}

.post-body h1, .post-body h2, .post-body h3 {
  margin: 1.5em 0 1em;
  font-weight: 600;
}

.post-body h1 { font-size: 1.5rem; }
.post-body h2 { font-size: 1.3rem; }
.post-body h3 { font-size: 1.1rem; }

.post-body code {
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.post-body pre {
  background: rgba(0, 0, 0, 0.3);
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}

.post-body blockquote {
  border-left: 4px solid var(--accent-color);
  padding-left: 15px;
  margin: 1em 0;
  color: var(--text-secondary);
  font-style: italic;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.tag {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(99, 102, 241, 0.15);
  color: var(--accent-color);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
}

.post-actions {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: var(--text-primary);
}

.action-btn.liked {
  color: #ef4444;
}

.comments-section {
  padding: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 25px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 30px;
}

.comment-input {
  width: 50%;
}

.comment-textarea {
  min-height: 100px;
  resize: vertical;
}

.comment-submit {
  align-self: flex-start;
  gap: 8px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 15px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

.comment-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: 600;
}

.comment-time {
  color: var(--text-muted);
  font-size: 13px;
}

.comment-content p {
  line-height: 1.6;
  color: var(--text-secondary);
}

.reply-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 10px;
  transition: color 0.3s ease;
}

.reply-btn:hover {
  color: var(--accent-color);
}

.replies-list {
  margin-top: 15px;
  padding-left: 20px;
  border-left: 2px solid rgba(255, 255, 255, 0.1);
}

.reply-item {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.reply-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.reply-content {
  flex: 1;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.reply-author {
  font-weight: 500;
  font-size: 13px;
}

.reply-time {
  color: var(--text-muted);
  font-size: 12px;
}

.reply-content p {
  font-size: 14px;
  line-height: 1.5;
}

.reply-form {
  margin-top: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.reply-textarea {
  min-height: 60px;
  resize: vertical;
  margin-bottom: 10px;
}

.reply-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .post-detail {
    padding: 10px;
  }
  
  .post-content {
    padding: 20px;
  }
  
  .post-title {
    font-size: 1.5rem;
  }
  
  .comment-input {
    width: 100%;
  }
}
</style>