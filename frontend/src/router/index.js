import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PostDetail from '../views/PostDetail.vue'
import Category from '../views/Category.vue'
import Gallery from '../views/Gallery.vue'
import Honors from '../views/Honors.vue'
import MessageBoard from '../views/MessageBoard.vue'
import Admin from '../views/admin/Admin.vue'
import Login from '../views/Login.vue'
import AdminPosts from '../views/admin/AdminPosts.vue'
import AdminComments from '../views/admin/AdminComments.vue'
import AdminSettings from '../views/admin/AdminSettings.vue'
import AdminGallery from '../views/admin/AdminGallery.vue'
import AdminHonors from '../views/admin/AdminHonors.vue'
import AdminMubu from '../views/admin/AdminMubu.vue'
import MubuNotes from '../views/MubuNotes.vue'
import ParticleInteraction from '../views/ParticleInteraction.vue'
import ParticleView from '../views/ParticleView.vue'
import Hobbies from '../views/Hobbies.vue'
import AdminMovies from '../views/admin/AdminMovies.vue'
import AdminMusic from '../views/admin/AdminMusic.vue'
import Archive from '../views/Archive.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Home', component: Home },
  { path: '/post/:slug', name: 'PostDetail', component: PostDetail },
  { path: '/category/:id', name: 'Category', component: Category },
  { path: '/gallery', name: 'Gallery', component: Gallery },
  { path: '/honors', name: 'Honors', component: Honors },
  { path: '/mubu', name: 'MubuNotes', component: MubuNotes },
  { path: '/hobbies', name: 'Hobbies', component: Hobbies },
  { path: '/archive', name: 'Archive', component: Archive },
  { path: '/message', name: 'MessageBoard', component: MessageBoard },
  { path: '/particles', name: 'ParticleInteraction', component: ParticleInteraction },
  { path: '/particles/:name', name: 'ParticleView', component: ParticleView },
  { 
    path: '/admin', 
    name: 'Admin', 
    component: Admin,
    children: [
      { path: '', name: 'AdminPosts', component: AdminPosts },
      { path: 'comments', name: 'AdminComments', component: AdminComments },
      { path: 'gallery', name: 'AdminGallery', component: AdminGallery },
      { path: 'honors', name: 'AdminHonors', component: AdminHonors },
      { path: 'mubu', name: 'AdminMubu', component: AdminMubu },
      { path: 'movies', name: 'AdminMovies', component: AdminMovies },
      { path: 'music', name: 'AdminMusic', component: AdminMusic },
      { path: 'settings', name: 'AdminSettings', component: AdminSettings }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('token')
  const isVisitor = localStorage.getItem('visitor')
  
  if (to.path.startsWith('/admin')) {
    if (!isLoggedIn) {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/' || to.path.startsWith('/category') || to.path === '/gallery' || to.path === '/honors' || to.path === '/mubu' || to.path === '/hobbies' || to.path === '/archive' || to.path === '/message' || to.path.startsWith('/particles')) {
    if (!isLoggedIn && !isVisitor) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router