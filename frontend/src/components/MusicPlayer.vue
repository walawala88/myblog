<template>
  <div class="music-player">
    <div class="tonearm" :class="{ active: isPlaying }">
      <div class="tonearm-pivot"></div>
      <div class="tonearm-rod"></div>
      <div class="tonearm-head"></div>
    </div>

    <button 
      class="vinyl-btn" 
      @click="toggleMusic"
      :class="{ playing: isPlaying }"
    >
      <div class="vinyl-record">
        <div class="vinyl-center">
          <div class="vinyl-label"></div>
        </div>
        <div class="vinyl-grooves">
          <div v-for="i in 10" :key="i" class="groove"></div>
        </div>
        <div class="vinyl-sparkle" v-for="i in 6" :key="'sparkle-' + i" :style="{ '--delay': i * 0.2 + 's' }"></div>
      </div>
      <div class="music-indicator" v-if="isPlaying">
        <span class="wave"></span>
        <span class="wave"></span>
        <span class="wave"></span>
      </div>
    </button>

    <Transition name="volume-fade">
      <div v-if="isPlaying" class="volume-bar glass-panel">
        <input
          type="range"
          min="0"
          max="100"
          step="1"
          :value="volume"
          @input="setVolume"
          class="volume-slider"
        />
        <span class="volume-label">{{ volume }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isPlaying = ref(false)
const volume = ref(50)
const wasPlaying = ref(false)
let audio = null

onMounted(() => {
  audio = new Audio('/background.mp3')
  audio.loop = true
  audio.volume = volume.value / 100

  window.addEventListener('hobby:musicPlay', handleHobbyPlay)
  window.addEventListener('hobby:musicStop', handleHobbyStop)
})

onUnmounted(() => {
  window.removeEventListener('hobby:musicPlay', handleHobbyPlay)
  window.removeEventListener('hobby:musicStop', handleHobbyStop)
  if (audio) {
    audio.pause()
    audio = null
  }
})

const handleHobbyPlay = () => {
  wasPlaying.value = isPlaying.value
  if (isPlaying.value) {
    audio.pause()
    isPlaying.value = false
  }
}

const handleHobbyStop = () => {
  if (wasPlaying.value && audio) {
    audio.play().then(() => {
      isPlaying.value = true
      wasPlaying.value = false
    }).catch(() => {})
  }
}

const toggleMusic = () => {
  if (!audio) return

  if (isPlaying.value) {
    audio.pause()
    isPlaying.value = false
  } else {
    window.dispatchEvent(new Event('background:musicPlay'))
    audio.play().then(() => {
      isPlaying.value = true
    }).catch(err => {
      console.log('Audio play failed:', err)
    })
  }
}

const setVolume = (e) => {
  const v = parseInt(e.target.value)
  if (!isNaN(v)) {
    volume.value = v
    if (audio) {
      audio.volume = v / 100
    }
    e.target.style.setProperty('--volume-percent', `${v}%`)
  }
}
</script>

<style scoped>
.music-player {
  position: fixed;
  right: 40px;
  top: 100px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.tonearm {
  position: absolute;
  top: 2px;
  right: 44px;
  width: 56px;
  height: 32px;
  z-index: 1;
  transition: transform 0.4s ease;
  transform: rotate(25deg);
  transform-origin: right bottom;
  pointer-events: none;
}

.tonearm.active {
  transform: rotate(5deg);
}

.tonearm-pivot {
  position: absolute;
  right: -4px;
  bottom: -4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #e0e0e0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}

.tonearm-rod {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 56px;
  height: 3px;
  background: linear-gradient(to left, #e0e0e0 0%, #f5f5f5 40%, #d0d0d0 100%);
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.tonearm-head {
  position: absolute;
  left: -2px;
  bottom: -2px;
  width: 12px;
  height: 8px;
  background: linear-gradient(135deg, #f0f0f0, #ccc);
  border-radius: 2px 2px 4px 2px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.25);
}

.vinyl-btn {
  position: relative;
  width: 68px;
  height: 68px;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  transition: transform 0.3s ease;
  z-index: 2;
}

.vinyl-btn:hover {
  transform: scale(1.06);
}

.vinyl-record {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d0d0d 0%, #1f1f1f 30%, #2a2a2a 60%, #111 100%);
  box-shadow: 
    0 0 0 2px rgba(255, 255, 255, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.5),
    0 0 12px rgba(255, 255, 255, 0.04),
    inset 0 2px 10px rgba(255, 255, 255, 0.04),
    inset 0 -2px 10px rgba(0, 0, 0, 0.5);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow 0.3s ease;
}

.vinyl-btn:hover .vinyl-record {
  box-shadow: 
    0 0 0 2px rgba(255, 255, 255, 0.2),
    0 6px 25px rgba(0, 0, 0, 0.55),
    0 0 18px rgba(255, 255, 255, 0.08),
    inset 0 2px 10px rgba(255, 255, 255, 0.06),
    inset 0 -2px 10px rgba(0, 0, 0, 0.5);
}

.vinyl-btn.playing .vinyl-record {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.vinyl-center {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 50%, #f0f0f0 100%);
  box-shadow: 
    0 2px 5px rgba(0, 0, 0, 0.3),
    inset 0 1px 2px rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.vinyl-label {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #1a1a1a;
  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.1);
}

.vinyl-grooves {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  padding: 6px;
}

.groove {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.07);
}

.groove:nth-child(1) { width: 100%; height: 100%; }
.groove:nth-child(2) { width: 91%; height: 91%; margin: 4.5%; }
.groove:nth-child(3) { width: 82%; height: 82%; margin: 9%; }
.groove:nth-child(4) { width: 73%; height: 73%; margin: 13.5%; }
.groove:nth-child(5) { width: 64%; height: 64%; margin: 18%; }
.groove:nth-child(6) { width: 55%; height: 55%; margin: 22.5%; }
.groove:nth-child(7) { width: 46%; height: 46%; margin: 27%; }
.groove:nth-child(8) { width: 38%; height: 38%; margin: 31%; }
.groove:nth-child(9) { width: 34%; height: 34%; margin: 33%; }
.groove:nth-child(10) { width: 30%; height: 30%; margin: 35%; }

.vinyl-sparkle {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  animation: sparkle 2s ease-in-out infinite;
  animation-delay: var(--delay);
}

.vinyl-sparkle:nth-child(11) { top: 20%; left: 35%; }
.vinyl-sparkle:nth-child(12) { top: 30%; right: 25%; }
.vinyl-sparkle:nth-child(13) { bottom: 35%; left: 25%; }
.vinyl-sparkle:nth-child(14) { bottom: 25%; right: 35%; }
.vinyl-sparkle:nth-child(15) { top: 45%; left: 20%; }
.vinyl-sparkle:nth-child(16) { top: 55%; right: 20%; }

@keyframes sparkle {
  0%, 100% { opacity: 0; transform: scale(0.5); }
  50% { opacity: 1; transform: scale(1); }
}

.music-indicator {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 3px;
  align-items: flex-end;
  padding: 3px 7px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}

.wave {
  width: 3px;
  height: 8px;
  background: linear-gradient(to top, #4ade80, #22c55e);
  border-radius: 2px;
  animation: wave 0.8s ease-in-out infinite;
}

.wave:nth-child(1) { animation-delay: 0s; }
.wave:nth-child(2) { animation-delay: 0.2s; }
.wave:nth-child(3) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}

.volume-fade-enter-active,
.volume-fade-leave-active {
  transition: all 0.35s ease;
}

.volume-fade-enter-from,
.volume-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.volume-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  background: rgba(20, 20, 30, 0.75);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  white-space: nowrap;
}

.volume-slider {
  -webkit-appearance: none;
  width: 60px;
  height: 2px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.15);
  outline: none;
  cursor: pointer;
  background: linear-gradient(to right, #818cf8 var(--volume-percent, 50%), rgba(255, 255, 255, 0.15) var(--volume-percent, 50%));
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  box-shadow: 0 0 6px rgba(99, 102, 241, 0.4);
}

.volume-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.volume-label {
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.55);
  min-width: 20px;
  text-align: right;
}
</style>