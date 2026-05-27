<template>
  <div class="hobbies-page">
    <div class="page-header glass-card">
      <h1 class="page-title"><Film :size="28" />观影记录</h1>
      <p class="page-desc">记录看过的每一部好电影</p>
    </div>

    <div v-if="movies.length === 0" class="empty-state glass-card">
      <Film :size="64" />
      <h3>暂无电影</h3>
      <p>管理员可以在后台添加电影</p>
    </div>

    <div v-else class="movies-grid">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="movie-card glass-card"
        @click="selectedMovie = movie"
      >
        <div class="movie-poster">
          <img :src="movie.poster" :alt="movie.title" />
          <div class="movie-rating-badge">
            <Star :size="12" />
            <span>{{ movie.rating }}</span>
          </div>
        </div>
        <div class="movie-info">
          <h3 class="movie-title">{{ movie.title }}</h3>
          <div class="movie-meta">
            <span class="meta-item"><User :size="13" />{{ movie.director }}</span>
            <span class="meta-item"><Calendar :size="13" />{{ movie.year }}</span>
          </div>
          <span class="movie-genre">{{ movie.genre }}</span>
          <p class="movie-summary">{{ truncate(movie.description, 80) }}</p>
        </div>
      </div>
    </div>

    <div v-if="selectedMovie" class="popup-overlay" @click.self="selectedMovie = null">
      <div class="popup-card">
        <button class="popup-close" @click="selectedMovie = null">
          <X :size="20" />
        </button>
        <div class="popup-body">
          <div class="popup-image-side">
            <img :src="selectedMovie.poster" :alt="selectedMovie.title" />
          </div>
          <div class="popup-info">
            <div class="popup-info-header">
              <Film :size="28" class="popup-icon" />
              <h2 class="popup-title">{{ selectedMovie.title }}</h2>
            </div>
            <div class="popup-meta-list">
              <div class="popup-meta-item">
                <User :size="16" />
                <span>{{ selectedMovie.director }}</span>
              </div>
              <div class="popup-meta-item">
                <Calendar :size="16" />
                <span>{{ selectedMovie.year }}</span>
              </div>
              <div class="popup-meta-item">
                <Clock :size="16" />
                <span>{{ selectedMovie.genre }}</span>
              </div>
              <div class="popup-meta-item rating-item">
                <Star :size="16" />
                <span class="rating-value">{{ selectedMovie.rating }}</span>
              </div>
            </div>
            <p class="popup-summary">{{ selectedMovie.description }}</p>
            <div v-if="selectedMovie.review" class="popup-review">
              <h4 class="review-label">影评</h4>
              <p>{{ selectedMovie.review }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-header glass-card">
      <h1 class="page-title"><Music :size="28" />音乐收藏</h1>
      <p class="page-desc">喜欢的旋律，随时聆听</p>
    </div>

    <div v-if="musicList.length === 0" class="empty-state glass-card">
      <Music :size="64" />
      <h3>暂无音乐</h3>
      <p>管理员可以在后台添加音乐</p>
    </div>

    <div v-else class="music-section glass-card">
      <div class="music-player-area">
        <div class="cover-area">
          <img
            v-if="currentTrack?.cover_path"
            :src="currentTrack.cover_path"
            :alt="currentTrack.title"
            class="cover-img"
            :class="{ spinning: isMusicPlaying }"
          />
          <div v-else class="vinyl-default" :class="{ spinning: isMusicPlaying }">
            <div class="vinyl-disc">
              <div class="vinyl-center-dot"></div>
              <div v-for="i in 8" :key="i" class="vinyl-groove-ring"></div>
            </div>
          </div>
        </div>
        <div class="track-info-display">
          <h3 class="track-title">{{ currentTrack?.title || '选择一首歌曲' }}</h3>
          <p class="track-artist">{{ currentTrack?.artist || '&nbsp;' }}</p>
        </div>
      </div>

      <div class="song-list">
        <div
          v-for="song in musicList"
          :key="song.id"
          class="song-item"
          :class="{ active: currentTrack?.id === song.id }"
          @click="playSong(song)"
        >
          <div class="song-item-left">
            <span class="song-index">{{ song.id }}</span>
            <div class="song-item-info">
              <span class="song-item-title">{{ song.title }}</span>
              <span class="song-item-artist">{{ song.artist }}</span>
            </div>
          </div>
          <div class="song-item-right">
            <Pause v-if="currentTrack?.id === song.id && isMusicPlaying" :size="16" class="song-play-icon" />
            <Play v-else :size="16" class="song-play-icon" />
          </div>
        </div>
      </div>

      <div class="audio-controls">
        <button class="ctrl-btn" @click="prevTrack" :disabled="!currentTrack">
          <SkipBack :size="18" />
        </button>
        <button class="ctrl-btn ctrl-play" @click="togglePlay" :disabled="!currentTrack">
          <Pause v-if="isMusicPlaying" :size="22" />
          <Play v-else :size="22" />
        </button>
        <button class="ctrl-btn" @click="nextTrack" :disabled="!currentTrack">
          <SkipForward :size="18" />
        </button>

        <div class="progress-area">
          <span class="time-label">{{ formatTime(currentTime) }}</span>
          <input
            type="range"
            class="progress-bar"
            min="0"
            :max="duration || 0"
            :value="currentTime"
            @input="seekTo"
          />
          <span class="time-label">{{ formatTime(duration) }}</span>
        </div>

        <div class="volume-area">
          <Volume2 :size="16" class="volume-icon" />
          <input
            type="range"
            class="volume-slider"
            min="0"
            max="100"
            :value="volume"
            @input="setVolume"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Film, Music, Play, Pause, SkipForward, SkipBack, Volume2, Star, X, Clock, User, Calendar } from 'lucide-vue-next'

const movies = ref([])
const selectedMovie = ref(null)
const musicList = ref([])
const currentTrack = ref(null)
const isMusicPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(70)

let audio = null

onMounted(() => {
  fetch('/api/movies')
    .then(r => r.json())
    .then(d => { movies.value = d })
    .catch(() => {})

  fetch('/api/music')
    .then(r => r.json())
    .then(d => { musicList.value = d })
    .catch(() => {})

  window.addEventListener('background:musicPlay', handleBackgroundPlay)
})

onUnmounted(() => {
  stopAudio()
  window.removeEventListener('background:musicPlay', handleBackgroundPlay)
})

const handleBackgroundPlay = () => {
  if (isMusicPlaying.value) {
    audio.pause()
    isMusicPlaying.value = false
    currentTime.value = 0
  }
}

const truncate = (text, maxLen) => {
  if (!text) return ''
  return text.length > maxLen ? text.slice(0, maxLen) + '...' : text
}

const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

const stopAudio = () => {
  if (audio) {
    audio.pause()
    audio.removeEventListener('timeupdate', onTimeUpdate)
    audio.removeEventListener('loadedmetadata', onLoaded)
    audio.removeEventListener('ended', onEnded)
    audio = null
  }
  isMusicPlaying.value = false
  currentTime.value = 0
  duration.value = 0
  window.dispatchEvent(new Event('hobby:musicStop'))
}

const createAudio = (src) => {
  stopAudio()
  audio = new Audio(src)
  audio.volume = volume.value / 100
  audio.addEventListener('timeupdate', onTimeUpdate)
  audio.addEventListener('loadedmetadata', onLoaded)
  audio.addEventListener('ended', onEnded)
}

const onTimeUpdate = () => {
  if (audio) currentTime.value = audio.currentTime
}

const onLoaded = () => {
  if (audio) duration.value = audio.duration
}

const onEnded = () => {
  isMusicPlaying.value = false
  currentTime.value = 0
  window.dispatchEvent(new Event('hobby:musicStop'))
}

const playSong = (song) => {
  if (!song.file_path) return

  if (currentTrack.value?.id === song.id) {
    togglePlay()
    return
  }

  currentTrack.value = song
  createAudio(song.file_path)

  audio.play().then(() => {
    isMusicPlaying.value = true
    window.dispatchEvent(new Event('hobby:musicPlay'))
  }).catch(() => {})
}

const togglePlay = () => {
  if (!audio) return

  if (isMusicPlaying.value) {
    audio.pause()
    isMusicPlaying.value = false
    window.dispatchEvent(new Event('hobby:musicStop'))
  } else {
    audio.play().then(() => {
      isMusicPlaying.value = true
      window.dispatchEvent(new Event('hobby:musicPlay'))
    }).catch(() => {})
  }
}

const prevTrack = () => {
  if (!currentTrack.value || musicList.value.length === 0) return
  const idx = musicList.value.findIndex(s => s.id === currentTrack.value.id)
  const prev = idx <= 0 ? musicList.value[musicList.value.length - 1] : musicList.value[idx - 1]
  playSong(prev)
}

const nextTrack = () => {
  if (!currentTrack.value || musicList.value.length === 0) return
  const idx = musicList.value.findIndex(s => s.id === currentTrack.value.id)
  const next = idx >= musicList.value.length - 1 ? musicList.value[0] : musicList.value[idx + 1]
  playSong(next)
}

const seekTo = (e) => {
  const t = parseFloat(e.target.value)
  if (audio && !isNaN(t)) {
    audio.currentTime = t
    currentTime.value = t
  }
}

const setVolume = (e) => {
  const v = parseInt(e.target.value)
  if (!isNaN(v)) {
    volume.value = v
    if (audio) audio.volume = v / 100
    e.target.style.setProperty('--volume-percent', `${v}%`)
  }
}
</script>

<style scoped>
.hobbies-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 100vh;
}

.page-header {
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}
.page-desc {
  color: var(--text-secondary);
  margin: 0;
}

.empty-state {
  padding: 60px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.empty-state h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0;
}
.empty-state p {
  color: var(--text-secondary);
  margin: 0;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.movie-card {
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
}

.movie-poster {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
}
.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.movie-card:hover .movie-poster img {
  transform: scale(1.08);
}

.movie-rating-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 12px;
  color: #fbbf24;
  font-size: 0.85rem;
  font-weight: 700;
  border: 1px solid rgba(251, 191, 36, 0.25);
}

.movie-info {
  padding: 16px 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.movie-title {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.movie-meta {
  display: flex;
  gap: 16px;
  font-size: 0.8rem;
  color: var(--text-secondary);
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}
.movie-genre {
  display: inline-block;
  padding: 3px 10px;
  background: rgba(99, 102, 241, 0.15);
  border-radius: 6px;
  font-size: 0.75rem;
  color: #a5b4fc;
  width: fit-content;
}
.movie-summary {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.popup-overlay {
  position: fixed;
  inset: 0;
  z-index: 1500;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.popup-card {
  position: relative;
  max-width: 880px;
  width: 100%;
  max-height: 85vh;
}
.popup-close {
  position: absolute;
  top: 14px;
  right: 14px;
  z-index: 10;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.popup-close:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: rotate(90deg);
}

.popup-body {
  display: flex;
  background: rgba(15, 15, 30, 0.75);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}
.popup-image-side {
  width: 45%;
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 380px;
  max-height: 75vh;
  overflow: hidden;
}
.popup-image-side img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.popup-info {
  flex: 1;
  padding: 36px 30px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  overflow-y: auto;
  max-height: 75vh;
}
.popup-info-header {
  display: flex;
  align-items: center;
  gap: 14px;
}
.popup-icon {
  color: #a5b4fc;
  flex-shrink: 0;
}
.popup-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.popup-meta-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.popup-meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}
.popup-meta-item.rating-item {
  color: #fbbf24;
  font-weight: 600;
}
.rating-value {
  font-size: 1rem;
}

.popup-summary {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.9rem;
  line-height: 1.7;
  margin: 0;
}

.popup-review {
  margin-top: 4px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.review-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #a5b4fc;
  margin: 0 0 8px;
}
.popup-review p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.88rem;
  line-height: 1.8;
  margin: 0;
}

.music-section {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.music-player-area {
  display: flex;
  align-items: center;
  gap: 24px;
}

.cover-area {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 50%;
  overflow: hidden;
}
.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.15);
}
.cover-img.spinning {
  animation: coverSpin 8s linear infinite;
}

.vinyl-default {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a1a2e 0%, #2a2a3e 50%, #1a1a2e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.vinyl-default.spinning {
  animation: coverSpin 8s linear infinite;
}
.vinyl-disc {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.vinyl-center-dot {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0e0e0, #c0c0c0);
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), inset 0 1px 2px rgba(255, 255, 255, 0.6);
}
.vinyl-groove-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.06);
}
.vinyl-groove-ring:nth-child(2) { width: 92%; height: 92%; }
.vinyl-groove-ring:nth-child(3) { width: 84%; height: 84%; }
.vinyl-groove-ring:nth-child(4) { width: 76%; height: 76%; }
.vinyl-groove-ring:nth-child(5) { width: 68%; height: 68%; }
.vinyl-groove-ring:nth-child(6) { width: 60%; height: 60%; }
.vinyl-groove-ring:nth-child(7) { width: 52%; height: 52%; }
.vinyl-groove-ring:nth-child(8) { width: 44%; height: 44%; }
.vinyl-groove-ring:nth-child(9) { width: 40%; height: 40%; }

@keyframes coverSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.track-info-display {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}
.track-title {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.track-artist {
  font-size: 0.88rem;
  color: var(--text-secondary);
  margin: 0;
}

.song-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 240px;
  overflow-y: auto;
}
.song-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.song-item:hover {
  background: rgba(255, 255, 255, 0.06);
}
.song-item.active {
  background: rgba(99, 102, 241, 0.15);
}
.song-item-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}
.song-index {
  font-size: 0.8rem;
  color: var(--text-muted);
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}
.song-item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.song-item-title {
  font-size: 0.9rem;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.song-item-artist {
  font-size: 0.78rem;
  color: var(--text-muted);
}
.song-item-right {
  flex-shrink: 0;
  margin-left: 12px;
}
.song-play-icon {
  color: var(--text-secondary);
}
.song-item.active .song-play-icon {
  color: #818cf8;
}

.audio-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.ctrl-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}
.ctrl-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
}
.ctrl-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.ctrl-play {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}
.ctrl-play:hover:not(:disabled) {
  background: linear-gradient(135deg, #818cf8, #a78bfa);
}

.progress-area {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}
.time-label {
  font-size: 0.7rem;
  color: var(--text-muted);
  min-width: 32px;
  text-align: center;
  flex-shrink: 0;
}
.progress-bar {
  -webkit-appearance: none;
  appearance: none;
  flex: 1;
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.12);
  outline: none;
  cursor: pointer;
  min-width: 0;
}
.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #818cf8;
  border: 2px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  box-shadow: 0 0 8px rgba(99, 102, 241, 0.4);
}
.progress-bar::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.volume-area {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}
.volume-icon {
  color: var(--text-secondary);
  flex-shrink: 0;
}
.volume-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 70px;
  height: 2px;
  border-radius: 2px;
  background: linear-gradient(to right, #818cf8 var(--volume-percent, 70%), rgba(255, 255, 255, 0.12) var(--volume-percent, 70%));
  outline: none;
  cursor: pointer;
}
.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #818cf8;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  box-shadow: 0 0 6px rgba(99, 102, 241, 0.3);
}
.volume-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

@media (max-width: 768px) {
  .movies-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }
  .movie-poster {
    height: 220px;
  }
  .popup-body {
    flex-direction: column;
    max-width: 95vw;
  }
  .popup-image-side {
    width: 100%;
    min-height: 220px;
    max-height: 300px;
  }
  .popup-info {
    padding: 24px 20px;
  }
  .popup-title {
    font-size: 1.15rem;
  }

  .music-section {
    padding: 20px;
  }
  .music-player-area {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .cover-area {
    width: 100px;
    height: 100px;
  }
  .volume-area {
    display: none;
  }
  .progress-area {
    gap: 4px;
  }
}

@media (max-width: 480px) {
  .movies-grid {
    grid-template-columns: 1fr;
  }
}
</style>