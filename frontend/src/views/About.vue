<template>
  <div class="about-page">
    <div class="page-content glass-card">
      <div class="about-header">
        <div class="avatar-large">
          <User :size="64" />
        </div>
        <h1 class="page-title">关于我</h1>
        <p class="page-subtitle">热爱生活，热爱技术</p>
      </div>
      
      <div class="about-sections">
        <section class="section glass-panel">
          <h2 class="section-title">
            <UserCircle :size="20" />
            个人简介
          </h2>
          <div class="section-content">
            <p>大家好，我是一名热爱技术的开发者。</p>
            <p>多年来，我一直致力于探索技术的边界，从前端开发到后端架构，从云计算到人工智能，都保持着浓厚的兴趣。</p>
            <p>这个博客是我记录技术心得、生活感悟的地方，希望能和大家一起交流分享。</p>
          </div>
        </section>
        
        <section class="section glass-panel">
          <h2 class="section-title">
            <Briefcase :size="20" />
            工作经历
          </h2>
          <div class="timeline">
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>高级前端工程师</h3>
                <span class="timeline-time">2022 - 至今</span>
                <p>负责公司核心产品的前端架构设计和开发</p>
              </div>
            </div>
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>全栈开发工程师</h3>
                <span class="timeline-time">2019 - 2022</span>
                <p>参与多个大型项目的全栈开发工作</p>
              </div>
            </div>
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <h3>初级前端工程师</h3>
                <span class="timeline-time">2017 - 2019</span>
                <p>从基础开始学习，积累开发经验</p>
              </div>
            </div>
          </div>
        </section>
        
        <section class="section glass-panel">
          <h2 class="section-title">
            <Code :size="20" />
            技术栈
          </h2>
          <div class="tech-stack">
            <div v-for="tech in techStack" :key="tech.name" class="tech-item">
              <div class="tech-icon">{{ tech.icon }}</div>
              <span class="tech-name">{{ tech.name }}</span>
            </div>
          </div>
        </section>
        
        <section class="section glass-panel">
          <h2 class="section-title">
            <Mail :size="20" />
            联系方式
          </h2>
          <div class="contact-info">
            <div class="contact-item">
              <Mail :size="18" />
              <span>email@example.com</span>
            </div>
            <div class="contact-item">
              <Github :size="18" />
              <span>github.com/username</span>
            </div>
            <div class="contact-item">
              <Twitter :size="18" />
              <span>@username</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { User, UserCircle, Briefcase, Code, Mail, Github, Twitter } from 'lucide-vue-next'

const techStack = ref([
  { name: 'JavaScript', icon: 'JS' },
  { name: 'TypeScript', icon: 'TS' },
  { name: 'Vue.js', icon: 'Vue' },
  { name: 'React', icon: 'React' },
  { name: 'Node.js', icon: 'Node' },
  { name: 'Python', icon: 'Py' },
  { name: 'Flask', icon: 'Flask' },
  { name: 'MySQL', icon: 'SQL' },
  { name: 'Docker', icon: 'Docker' },
  { name: 'AWS', icon: 'AWS' }
])
</script>

<style scoped>
.about-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-content {
  padding: 32px;
}

.about-header {
  text-align: center;
  margin-bottom: 40px;
}

.avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 20px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.page-subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
}

.about-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section {
  padding: 25px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--accent-color);
}

.section-content p {
  line-height: 1.8;
  color: var(--text-secondary);
  margin-bottom: 15px;
}

.timeline {
  position: relative;
  padding-left: 20px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: rgba(99, 102, 241, 0.3);
}

.timeline-item {
  position: relative;
  margin-bottom: 30px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -24px;
  top: 5px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--accent-color);
  border: 3px solid rgba(99, 102, 241, 0.2);
}

.timeline-content h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.timeline-time {
  color: var(--text-muted);
  font-size: 13px;
  display: block;
  margin-bottom: 8px;
}

.timeline-content p {
  color: var(--text-secondary);
  font-size: 14px;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(99, 102, 241, 0.1);
  padding: 8px 15px;
  border-radius: 8px;
}

.tech-icon {
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-color);
}

.tech-name {
  font-size: 14px;
  color: var(--text-secondary);
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 15px;
}

.contact-item svg {
  color: var(--accent-color);
}

@media (max-width: 768px) {
  .about-page {
    padding: 10px;
  }
  
  .page-content {
    padding: 20px;
  }
}
</style>