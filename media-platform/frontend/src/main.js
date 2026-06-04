import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomePage from './pages/HomePage.vue'
import ImagePage from './pages/ImagePage.vue'
import AudioPage from './pages/AudioPage.vue'
import VideoPage from './pages/VideoPage.vue'
import TasksPage from './pages/TasksPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/image', component: ImagePage },
  { path: '/audio', component: AudioPage },
  { path: '/video', component: VideoPage },
  { path: '/tasks', component: TasksPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
