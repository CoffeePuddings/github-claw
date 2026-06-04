<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">🎬 多媒体处理平台</div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/image">图片处理</router-link>
        <router-link to="/audio">音频处理</router-link>
        <router-link to="/video">视频处理</router-link>
        <router-link to="/tasks">任务记录</router-link>
      </div>
    </nav>
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f7fa;
  color: #333;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background: rgba(255,255,255,0.2);
  color: white;
}

.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}
</style>
