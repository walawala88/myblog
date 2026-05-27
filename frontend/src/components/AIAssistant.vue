<template>
  <div>
    <button class="ai-btn" @click="showChat = true">
      <div class="ai-btn-inner">
        <Bot :size="22" />
      </div>
    </button>

    <Teleport to="body">
      <Transition name="overlay-fade">
        <div v-if="showChat" class="ai-overlay" @click.self="showChat = false">
          <div class="ai-panel glass-card">
            <div class="ai-panel-header">
              <div class="ai-header-left">
                <div class="ai-avatar-bot"><img src="/avatar.jpg" alt="ZHH" /></div>
                <div>
                  <h3>ZHH</h3>
                  <span class="ai-status">INTJ | CS 学生</span>
                </div>
              </div>
              <button class="ai-close" @click="showChat = false">
                <X :size="18" />
              </button>
            </div>

            <div class="ai-messages" ref="msgContainer">
              <div class="ai-msg bot">
                <div class="msg-avatar bot-icon">
                  <img src="/avatar.jpg" alt="ZHH" />
                </div>
                <div class="msg-bubble glass-card ai-intro">
                  <p>你好。我是 ZHH，一名计算机科学与技术专业学生，欢迎与我对话。</p>
                </div>
              </div>
              <div v-for="(msg, i) in messages" :key="i" :class="['ai-msg', msg.type]">
                <div v-if="msg.type === 'bot'" class="msg-avatar bot-icon">
                  <img src="/avatar.jpg" alt="AI" />
                </div>
                <div v-else class="msg-avatar user-avatar">
                  <span>我</span>
                </div>
                <div class="msg-bubble glass-card">
                  <p>{{ msg.content }}</p>
                </div>
              </div>
              <div v-if="typing" class="ai-typing">
                <div class="msg-avatar bot-icon">
                  <img src="/avatar.jpg" alt="AI" />
                </div>
                <div class="msg-bubble glass-card typing-bubble">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>

            <div class="ai-input-area">
              <input
                ref="inputRef"
                v-model="input"
                placeholder="输入消息..."
                class="ai-input glass-card"
                @keyup.enter="send"
              />
              <button class="ai-send" @click="send" :disabled="!input.trim()">
                <Send :size="18" />
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { Bot, X, Send } from 'lucide-vue-next'
import axios from 'axios'

const emit = defineEmits(['update:visible'])
const showChat = ref(false)
const input = ref('')
const messages = ref([])
const typing = ref(false)
const msgContainer = ref(null)
const inputRef = ref(null)

watch(showChat, v => {
  emit('update:visible', v)
})

const send = async () => {
  const text = input.value.trim()
  if (!text) return
  messages.value.push({ type: 'user', content: text })
  input.value = ''
  await nextTick()
  scrollDown()

  typing.value = true
  try {
    const res = await axios.post('/api/chat', { message: text })
    messages.value.push({ type: 'bot', content: res.data.reply })
  } catch {
    messages.value.push({ type: 'bot', content: '网络异常，请稍后再试。' })
  }
  typing.value = false
  await nextTick()
  scrollDown()
}

const scrollDown = () => {
  if (msgContainer.value) msgContainer.value.scrollTop = msgContainer.value.scrollHeight
}

watch(showChat, v => {
  if (v) {
    document.body.style.overflow = 'hidden'
    setTimeout(() => inputRef.value?.focus(), 350)
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
.ai-btn {
  position: fixed;
  right: 40px;
  top: 275px;
  z-index: 50;
  border: none;
  cursor: pointer;
  padding: 0;
  background: none;
  transition: transform 0.3s ease;
}

.ai-btn:hover {
  transform: scale(1.08);
}

.ai-btn-inner {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.25);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c7d2fe;
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
}

.ai-btn:hover .ai-btn-inner {
  background: rgba(99, 102, 241, 0.35);
  border-color: rgba(255,255,255,0.25);
  color: white;
}

.ai-overlay {
  position: fixed;
  inset: 0;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 0;
}

.overlay-fade-enter-active { transition: all 0.3s ease; }
.overlay-fade-leave-active { transition: all 0.25s ease; }
.overlay-fade-enter-from, .overlay-fade-leave-to { opacity: 0; }
.overlay-fade-enter-from .ai-panel { transform: translateY(20px) scale(0.97); }
.overlay-fade-leave-to .ai-panel { transform: translateY(10px) scale(0.98); }

.ai-panel {
  width: 70%;
  max-width: 70%;
  min-width: 400px;
  height: 70vh;
  display: flex;
  flex-direction: column;
  background: rgba(25, 25, 40, 0.55);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(0,0,0,0.3);
}

.ai-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.ai-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.ai-avatar-bot {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.15);
  overflow: hidden;
}

.ai-avatar-bot img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ai-panel-header h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
}

.ai-status {
  font-size: 0.75rem;
  color: #22c55e;
}

.ai-close {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.06);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.ai-close:hover {
  background: rgba(255,255,255,0.12);
  color: var(--text-primary);
}

.ai-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px 100px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.ai-intro {
  align-self: flex-start;
  padding: 16px 20px;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 75%;
}

.ai-intro p { margin: 6px 0; }

.ai-msg {
  display: flex;
  gap: 12px;
  animation: msgIn 0.25s ease;
}

@keyframes msgIn { from { opacity: 0; transform: translateY(8px); } }

.ai-msg.user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  overflow: hidden;
  border: 2px solid rgba(255,255,255,0.15);
}

.msg-avatar.bot-icon {
  background: rgba(99, 102, 241, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a5b4fc;
}

.msg-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
}

.msg-bubble {
  max-width: 70%;
  padding: 14px 18px;
  border-radius: 20px;
  font-size: 0.95rem;
  line-height: 1.6;
  position: relative;
}

.ai-msg.bot .msg-bubble {
  border-bottom-left-radius: 6px;
  background: rgba(255,255,255,0.06);
}

.ai-msg.user .msg-bubble {
  border-bottom-right-radius: 6px;
  background: rgba(99,102,241,0.2);
}

.msg-bubble p { margin: 0; }

.ai-typing {
  display: flex;
  gap: 12px;
}

.typing-bubble {
  padding: 14px 18px;
  display: flex;
  gap: 6px;
}

.typing-bubble span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-secondary);
  animation: dotBounce 1.4s infinite ease-in-out;
}

.typing-bubble span:nth-child(2) { animation-delay: 0.2s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotBounce {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.ai-input-area {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.ai-input {
  flex: 1;
  padding: 14px 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 24px;
  color: var(--text-primary);
  font-size: 0.95rem;
  outline: none;
  transition: all 0.3s ease;
}

.ai-input:focus {
  border-color: rgba(99,102,241,0.4);
  background: rgba(255,255,255,0.1);
}

.ai-input::placeholder { color: var(--text-muted); }

.ai-send {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.ai-send:hover:not(:disabled) { transform: scale(1.05); }
.ai-send:disabled { opacity: 0.4; cursor: not-allowed; }

@media (max-width: 768px) {
  .ai-overlay { padding: 16px; }
  .ai-panel { 
    max-width: 100%; 
    max-height: 90vh; 
    border-radius: 20px;
  }
  .ai-btn { top: auto; right: 16px; bottom: 16px; }
  .ai-btn-inner { width: 46px; height: 46px; }
  .msg-bubble { max-width: 75%; }
}

@media (max-width: 480px) {
  .ai-panel-header { padding: 16px 20px; }
  .ai-messages { padding: 16px 20px; }
  .ai-input-area { padding: 16px 20px; }
  .ai-avatar-bot { width: 38px; height: 38px; }
  .msg-avatar { width: 36px; height: 36px; }
}
</style>