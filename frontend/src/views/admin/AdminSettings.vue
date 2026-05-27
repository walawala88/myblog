<template>
  <div class="admin-settings">
    <div class="page-header">
      <h1>网站设置</h1>
    </div>
    
    <div class="settings-form glass-card">
      <div class="form-section">
        <h2 class="section-title">
          <Globe :size="20" />
          网站信息
        </h2>
        
        <div class="form-group">
          <label>网站名称</label>
          <input v-model="settings.site_name" type="text" placeholder="请输入网站名称" />
        </div>
        
        <div class="form-group">
          <label>网站简介</label>
          <textarea v-model="settings.site_description" rows="3" placeholder="请输入网站简介"></textarea>
        </div>
      </div>
      
      <div class="form-section">
        <h2 class="section-title">
          <User :size="20" />
          个人信息
        </h2>
        
        <div class="form-group">
          <label>昵称</label>
          <input v-model="settings.username" type="text" placeholder="请输入昵称" />
        </div>
        
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="settings.email" type="email" placeholder="请输入邮箱" />
        </div>
        
        <div class="form-group">
          <label>个人简介</label>
          <textarea v-model="settings.bio" rows="3" placeholder="请输入个人简介"></textarea>
        </div>
      </div>
      
      <div class="form-section">
        <h2 class="section-title">
          <Lock :size="20" />
          密码修改
        </h2>
        
        <div class="form-group">
          <label>当前密码</label>
          <input v-model="passwordForm.current_password" type="password" placeholder="请输入当前密码" />
        </div>
        
        <div class="form-group">
          <label>新密码</label>
          <input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码" />
        </div>
        
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" />
        </div>
      </div>
      
      <div class="form-actions">
        <button class="btn btn-secondary" @click="resetSettings">重置</button>
        <button class="btn btn-primary" @click="saveSettings">保存设置</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Globe, User, Lock } from 'lucide-vue-next'

const settings = ref({
  site_name: '',
  site_description: '',
  username: '',
  email: '',
  bio: ''
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const loadSettings = () => {
  fetch('/api/user', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  })
  .then(res => res.json())
  .then(data => {
    settings.value = {
      site_name: data.site_name || '',
      site_description: data.site_description || '',
      username: data.username || '',
      email: data.email || '',
      bio: data.bio || ''
    }
  })
}

const resetSettings = () => {
  loadSettings()
  passwordForm.value = {
    current_password: '',
    new_password: '',
    confirm_password: ''
  }
}

const saveSettings = () => {
  const userData = {
    username: settings.value.username,
    email: settings.value.email,
    bio: settings.value.bio,
    site_name: settings.value.site_name,
    site_description: settings.value.site_description
  }
  
  if (passwordForm.value.new_password) {
    if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
      alert('两次输入的密码不一致')
      return
    }
    userData.password = passwordForm.value.new_password
    userData.current_password = passwordForm.value.current_password
  }
  
  fetch('/api/user', {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(userData)
  })
  .then(res => res.json())
  .then(() => {
    alert('设置已保存')
    resetSettings()
  })
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.admin-settings {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.settings-form {
  padding: 30px;
}

.form-section {
  margin-bottom: 30px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--accent-color);
}

.form-group {
  margin-bottom: 15px;
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
  width: 50%;
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

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .form-group input,
  .form-group textarea {
    width: 100%;
  }
}
</style>