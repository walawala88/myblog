<template>
  <main class="main-content">
    <div class="page-header glass-card">
      <h1 class="page-title"><MessageSquare :size="28" />留言板</h1>
      <p class="page-desc">来都来了，说点什么吧</p>
    </div>
    
    <form class="message-form glass-card" @submit.prevent="submitMessage">
      <div class="form-row">
        <input v-model="form.name" type="text" placeholder="你的名字" class="form-input" maxlength="30" required />
        <input v-model="form.email" type="email" placeholder="你的邮箱（可选）" class="form-input" />
      </div>
      <textarea v-model="form.content" placeholder="写下你想说的话..." rows="4" class="form-textarea" maxlength="500" required></textarea>
      <div class="form-footer">
        <span class="char-count">{{ form.content.length }}/500</span>
        <button type="submit" class="btn btn-primary"><Send :size="16" />发送留言</button>
      </div>
      <div v-if="submitSuccess" class="success-message">留言发送成功！</div>
      <div v-if="submitError" class="error-message">{{ submitError }}</div>
    </form>
    
    <div class="messages-list">
      <div v-for="msg in messages" :key="msg.id" class="message-card glass-card">
        <div class="message-header">
          <div class="user-info">
            <div class="user-avatar"><User :size="20" /></div>
            <div>
              <span class="user-name">{{ msg.name }}</span>
              <span class="message-time">{{ formatDate(msg.created_at) }}</span>
            </div>
          </div>
        </div>
        <p class="message-content">{{ msg.content }}</p>
      </div>
      
      <div v-if="messages.length === 0" class="empty-state">
        <MessageSquare :size="48" />
        <h3>暂无留言</h3>
        <p>成为第一个留言的人吧！</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, MessageSquare, Send } from 'lucide-vue-next'

const messages = ref([])
const submitSuccess = ref(false)
const submitError = ref('')

const form = ref({
  name: '',
  email: '',
  content: ''
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const submitMessage = () => {
  if (!form.value.content.trim()) return
  submitSuccess.value = false
  submitError.value = ''
  
  fetch('/api/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      submitError.value = data.error
    } else {
      submitSuccess.value = true
      form.value = { name: '', email: '', content: '' }
      messages.value.unshift({
        id: Date.now(),
        name: data.name || '匿名',
        content: data.content || form.value.content,
        created_at: new Date().toISOString()
      })
      setTimeout(() => { submitSuccess.value = false }, 3000)
    }
  })
}

onMounted(() => {
  fetch('/api/messages').then(r => r.json()).then(d => { messages.value = d.reverse() })
})
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

.page-header { padding: 30px; display: flex; flex-direction: column; gap: 8px; }
.page-title { display: flex; align-items: center; gap: 12px; font-size: 1.8rem; font-weight: 700; margin: 0; }
.page-desc { color: var(--text-secondary); margin: 0; }

.message-form { padding: 24px; display: flex; flex-direction: column; gap: 16px; }
.form-row { display: flex; gap: 12px; }
.form-input, .form-textarea { width: 100%; padding: 12px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; color: var(--text-primary); font-size: 14px; outline: none; }
.form-input:focus, .form-textarea:focus { border-color: var(--accent-color); }
.form-textarea { resize: vertical; min-height: 100px; }
.form-footer { display: flex; justify-content: space-between; align-items: center; }
.char-count { font-size: 0.8rem; color: var(--text-muted); }
.success-message { padding: 10px; background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); border-radius: 8px; color: #22c55e; font-size: 0.9rem; }
.error-message { padding: 10px; background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; color: #ef4444; font-size: 0.9rem; }

.messages-list { display: flex; flex-direction: column; gap: 16px; }
.message-card { padding: 20px; }
.message-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.user-info { display: flex; align-items: center; gap: 10px; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; }
.user-name { font-weight: 600; font-size: 0.95rem; display: block; }
.message-time { font-size: 0.75rem; color: var(--text-muted); }
.message-content { color: var(--text-secondary); line-height: 1.6; margin: 0; font-size: 0.95rem; }

.empty-state { padding: 40px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 12px; }
.empty-state h3 { font-size: 1.3rem; font-weight: 600; margin: 0; }
.empty-state p { color: var(--text-secondary); margin: 0; }

@media (max-width: 640px) {
  .main-content { padding-left: 16px; padding-right: 16px; gap: 16px; }
  .form-row { flex-direction: column; }
}
</style>