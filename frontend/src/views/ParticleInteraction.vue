<template>
  <div class="particle-page">
    <h1 class="page-title">粒子互动</h1>
    <p class="page-desc">选择一个粒子场景，体验沉浸式交互</p>

    <div class="cards">
      <div class="card glass-card" @click="go('flower-butterfly')">
        <div class="card-icon">🦋</div>
        <h2>花朵蝴蝶文字</h2>
        <p>花朵绽放、蝴蝶飞舞、文字粒子变形，手势控制形态切换</p>
      </div>

      <div class="card glass-card" @click="go('silk-flower')">
        <div class="card-icon">🌸</div>
        <h2>昙花</h2>
        <p>液态丝绸花朵，手势驱动的粒子绽放与泼溅</p>
      </div>

      <div class="card glass-card" @click="go('landscape')">
        <div class="card-icon">🏔️</div>
        <h2>千里江山图</h2>
        <p>赛博山水，35万粒子构建的数字江山，手势控制山峦起伏</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const go = (name) => {
  router.push(`/particles/${name}`)
}
</script>

<style scoped>
.particle-page {
  padding: 60px 24px 40px;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--text-primary);
}

.page-desc {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0 0 48px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  width: 100%;
}

.card {
  padding: 36px 24px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.35s ease;
  text-align: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.card h2 {
  font-size: 1.15rem;
  font-weight: 600;
  margin: 0 0 10px;
  color: var(--text-primary);
}

.card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .cards {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 1.6rem;
  }
}
</style>
