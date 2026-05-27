<template>
  <div class="login-page">
    <!-- Video Background - Always at the bottom -->
    <div class="video-background">
      <video autoplay muted loop playsinline>
        <source src="/lv_0_20260525143810.mp4" type="video/mp4">
      </video>
      <div class="video-overlay"></div>
    </div>

    <!-- Main Login Container - 70% of screen -->
    <div class="login-container glass-card">
      <!-- Left Section: Animated Characters -->
      <div class="left-section">
        <div class="characters-container">
          <AnimatedCharacters
            :isTyping="isTyping"
            :showPassword="showPassword"
            :passwordLength="password.length"
            :loginFailed="loginFailed"
            :loginSuccess="loginSuccess"
          />
        </div>
      </div>

      <!-- Right Section: User Type Selection and Login Form -->
      <div class="right-section">
        <div class="content-wrapper">
          <!-- User Type Selection -->
          <div class="user-type-selection glass-panel">
            <div 
              class="user-type-option"
              :class="{ active: userType === 'visitor' }"
              @click="userType = 'visitor'"
            >
              游客
            </div>
            <div 
              class="user-type-option"
              :class="{ active: userType === 'admin' }"
              @click="userType = 'admin'"
            >
              管理员
            </div>
          </div>

          <!-- Welcome Message -->
          <div class="welcome-message">
            <h1>Welcome to my blog</h1>
          </div>

          <!-- Visitor Mode - Direct Access Button -->
          <div v-if="userType === 'visitor'" class="visitor-section">
            <button @click="enterAsVisitor" class="visitor-button">
              <span class="button-text">游客免登录进入</span>
            </button>
          </div>

          <!-- Admin Mode - Full Login Form -->
          <div v-else-if="userType === 'admin'" class="admin-login-section">
            <div class="form-wrapper">
              <!-- Login Form -->
              <form @submit.prevent="handleSubmit" class="login-form">
                <!-- Username Field -->
                <div class="form-group">
                  <label for="username" class="form-label">Username</label>
                  <input
                    id="username"
                    v-model="username"
                    type="text"
                    placeholder="admin"
                    class="form-input"
                    autocomplete="off"
                    required
                    @focus="isTyping = true"
                    @blur="isTyping = false"
                  />
                  <p v-if="errors.username" class="error-message">{{ errors.username }}</p>
                </div>

                <!-- Password Field -->
                <div class="form-group">
                  <label for="password" class="form-label">Password</label>
                  <div class="password-wrapper">
                    <input
                      id="password"
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="••••••••"
                      class="form-input"
                      required
                    />
                    <button
                      type="button"
                      @click="showPassword = !showPassword"
                      class="password-toggle"
                    >
                      <svg v-if="showPassword" class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                      <svg v-else class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                        <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                        <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                        <line x1="2" x2="22" y1="2" y2="22"/>
                      </svg>
                    </button>
                  </div>
                  <p v-if="errors.password" class="error-message">{{ errors.password }}</p>
                </div>

                <!-- Remember Me -->
                <!-- <div class="form-options">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="rememberMe" class="checkbox" />
                    <span>Remember for 30 days</span>
                  </label>
                </div> -->

                <!-- Error Alert -->
                <div v-if="errorMessage" class="error-alert">
                  {{ errorMessage }}
                </div>

                <!-- Submit Button -->
                <button
                  type="submit"
                  class="submit-button"
                  :disabled="isLoading"
                >
                  <span class="button-text">{{ isLoading ? 'Signing in...' : 'Log in' }}</span>
                  <svg class="button-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14"/>
                    <path d="m12 5 7 7-7 7"/>
                  </svg>
                </button>
              </form>

              <!-- Sign Up Link -->
              <!-- <div class="signup-link">
                Don't have an account? <a href="/signup">Sign Up</a>
              </div> -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import AnimatedCharacters from './AnimatedCharacters.vue'

// 用户类型默认为访客，确保首次访问时能看到动画
const userType = ref('visitor')

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isTyping = ref(false)
const isLoading = ref(false)
const loginFailed = ref(false)
const loginSuccess = ref(false)
const errorMessage = ref('')
const errors = ref({
  username: '',
  password: ''
})

// 监听用户类型变化，重置表单
watch(userType, (newType) => {
  if(newType === 'visitor') {
    // 访客模式下重置表单数据
    username.value = ''
    password.value = ''
    rememberMe.value = false
    showPassword.value = false
    isTyping.value = false
    isLoading.value = false
    loginFailed.value = false
    loginSuccess.value = false
    errorMessage.value = ''
    errors.value = { username: '', password: '' }
  }
})

const validateForm = () => {
  errors.value = { username: '', password: '' }
  let isValid = true

  if (!username.value) {
    errors.value.username = 'Username is required'
    isValid = false
  }

  if (!password.value) {
    errors.value.password = 'Password is required'
    isValid = false
  } else if (password.value.length < 6) {
    errors.value.password = 'Password must be at least 6 characters'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errorMessage.value = ''
  loginFailed.value = false
  loginSuccess.value = false

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      localStorage.setItem('token', data.access_token)
      loginSuccess.value = true
      setTimeout(() => {
        window.location.href = '/admin'
      }, 1500)
    } else {
      throw new Error(data.message || 'Login failed')
    }
  } catch (error) {
    errorMessage.value = 'Invalid username or password. Please try again.'
    loginFailed.value = true
    setTimeout(() => {
      loginFailed.value = false
    }, 3000)
  } finally {
    isLoading.value = false
  }
}

const enterAsVisitor = () => {
  localStorage.setItem('visitor', 'true')
  window.location.href = '/'
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.video-background video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(10, 10, 15, 0.4) 0%,
    rgba(10, 10, 15, 0.3) 50%,
    rgba(10, 10, 20, 0.4) 100%
  );
}

.login-container {
  position: relative;
  z-index: 1;
  width: 70%;
  max-width: 900px;
  min-height: 480px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  overflow: hidden;
}

.left-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  background: rgba(0, 0, 0, 0.08);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  overflow: hidden;
}

.characters-container {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.characters-container :deep(.animated-characters-container) {
  transform: scale(0.5);
  transform-origin: center center;
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
}

.content-wrapper {
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.user-type-selection {
  display: flex;
  gap: 0.5rem;
  padding: 0.375rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 280px;
}

.user-type-option {
  flex: 1;
  padding: 0.625rem 1rem;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-type-option.active {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.user-type-option:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
}

.welcome-message {
  text-align: center;
  width: 100%;
}

.welcome-message h1 {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.visitor-section {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.visitor-button {
  background: linear-gradient(135deg, #ed6da8, #be3191);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(237, 109, 168, 0.3);
  width: 100%;
  max-width: 220px;
}

.visitor-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(237, 109, 168, 0.4);
}

.admin-login-section {
  width: 100%;
}

.form-wrapper {
  width: 100%;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}

.form-input {
  width: 100%;
  height: 3rem;
  padding: 0 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
  color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(99, 102, 241, 0.6);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: rgba(255, 255, 255, 0.9);
}

.icon {
  width: 20px;
  height: 20px;
}

.error-message {
  font-size: 0.8125rem;
  color: #ef4444;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.6);
}

.checkbox {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
  accent-color: #6366f1;
}

.forgot-link {
  font-size: 0.8125rem;
  color: rgba(99, 102, 241, 0.8);
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  text-decoration: underline;
}

.error-alert {
  padding: 0.75rem;
  font-size: 0.8125rem;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 0.75rem;
}

.submit-button {
  position: relative;
  width: 100%;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 0.75rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
  background: linear-gradient(135deg, #d678b2, #b7439a);
  color: white;
  border: none;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(224, 70, 229, 0.4);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-text {
  transition: transform 0.3s;
}

.button-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s;
}

.submit-button:hover:not(:disabled) .button-text {
  transform: translateX(-6px);
}

.submit-button:hover:not(:disabled) .button-icon {
  transform: translateX(6px);
}

.signup-link {
  margin-top: 1.75rem;
  text-align: center;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.5);
}

.signup-link a {
  color: rgba(99, 102, 241, 0.8);
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}

@media (max-width: 1024px) {
  .login-container {
    width: 90%;
    grid-template-columns: 1fr;
  }

  .left-section {
    display: none;
  }

  .right-section {
    padding: 2rem;
  }
}

@media (max-width: 640px) {
  .login-container {
    width: 95%;
    padding: 1.5rem;
  }

  .content-wrapper {
    gap: 1.25rem;
  }

  .welcome-message h1 {
    font-size: 1.5rem;
  }
}
</style>