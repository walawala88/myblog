<template>
  <div class="login-page">
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
        <div class="user-type-selection">
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
              <!-- Email Field -->
              <div class="form-group">
                <label for="email" class="form-label">Email</label>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  placeholder="you@example.com"
                  class="form-input"
                  autocomplete="off"
                  required
                  @focus="isTyping = true"
                  @blur="isTyping = false"
                />
                <p v-if="errors.email" class="error-message">{{ errors.email }}</p>
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
              <div class="form-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="rememberMe" class="checkbox" />
                  <span>Remember for 30 days</span>
                </label>
              </div>

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
            <div class="signup-link">
              Don't have an account? <a href="/signup">Sign Up</a>
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

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isTyping = ref(false)
const isLoading = ref(false)
const loginFailed = ref(false)
const loginSuccess = ref(false)
const errorMessage = ref('')
const errors = ref({
  email: '',
  password: ''
})

// 监听用户类型变化，重置表单
watch(userType, (newType) => {
  if(newType === 'visitor') {
    // 访客模式下重置表单数据
    email.value = ''
    password.value = ''
    rememberMe.value = false
    showPassword.value = false
    isTyping.value = false
    isLoading.value = false
    loginFailed.value = false
    loginSuccess.value = false
    errorMessage.value = ''
    errors.value = { email: '', password: '' }
  }
})

const validateForm = () => {
  errors.value = { email: '', password: '' }
  let isValid = true

  // 缓存正则表达式，避免每次都创建
  if (!email.value) {
    errors.value.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    errors.value.email = 'Please enter a valid email address'
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
    await new Promise(resolve => setTimeout(resolve, 1500))
    console.log('Login:', { email: email.value, password: password.value, rememberMe: rememberMe.value })
    if (email.value === 'admin@example.com' && password.value === 'admin123') {
      loginSuccess.value = true
      setTimeout(() => {
        loginSuccess.value = false
      }, 6000)
    } else {
      throw new Error('Invalid credentials')
    }
  } catch (error) {
    errorMessage.value = 'Invalid email or password. Please try again.'
    loginFailed.value = true
    setTimeout(() => {
      loginFailed.value = false
    }, 3000)
  } finally {
    isLoading.value = false
  }
}

const enterAsVisitor = () => {
  alert('欢迎以访客身份浏览博客！')
  // 这里可以添加跳转到博客主页的逻辑
}
</script>

<style scoped>
.login-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  max-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg,  #3a3a3a 20%, #2a2a2a 80%);
}

.left-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #252525 20%, #3c3b3b 80%); /* 更深的灰黑色渐变 */
  padding: 2rem;
  position: relative;
}

.characters-container {
  width: 100%;
  max-width: 400px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.right-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(25, 25, 25, 0.7);
  backdrop-filter: blur(10px);
}

.content-wrapper {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.user-type-selection {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 0.5rem;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 300px;
}

.user-type-option {
  flex: 1;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #aaa;
  text-align: center;
  font-size: 0.9rem;
}

.user-type-option.active {
  background: #0cabba;
  color: white;
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3);
}

.user-type-option:hover {
  background: rgba(79, 70, 229, 0.2);
  color: white;
}

.welcome-message {
  text-align: center;
  width: 100%;
}

.welcome-message h1 {
  font-size: 1.875rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #ffffff;
  margin: 0;
}

.visitor-section {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
}

.visitor-button {
  background: #ed6da8;
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(103, 39, 116, 0.3);
  width: 100%;
  max-width: 250px;
}

.visitor-button:hover {
  background: #be3191;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(37, 151, 222, 0.4);
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
  color: #cccccc;
}

.form-input {
  width: 100%;
  height: 3rem;
  padding: 0 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
  color: #ffffff;
  backdrop-filter: blur(10px);
}

.form-input::placeholder {
  color: #888888;
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.password-wrapper {
  position: relative;
}

.password-wrapper .form-input {
  padding-right: 2.5rem;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #ffffff;
}

.icon {
  width: 20px;
  height: 20px;
}

.error-message {
  font-size: 0.875rem;
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
  font-size: 0.875rem;
  cursor: pointer;
  color: #cccccc;
}

.checkbox {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
  accent-color: #6366f1;
}

.forgot-link {
  font-size: 0.875rem;
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.forgot-link:hover {
  text-decoration: underline;
}

.error-alert {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 0.5rem;
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
  font-weight: 500;
  border-radius: 0.5rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
  background: #4f46e5;
  color: white;
  border: none;
}

.submit-button:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
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
  transform: translateX(-8px);
}

.submit-button:hover:not(:disabled) .button-icon {
  transform: translateX(8px);
}

.signup-link {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.875rem;
  color: #aaaaaa;
}

.signup-link a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}

@media (max-width: 1024px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .left-section {
    display: none;
  }

  .right-section {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>