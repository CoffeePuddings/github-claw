<template>
  <div class="home">
    <h1>🎬 多媒体处理平台</h1>
    <p class="subtitle">支持图片、音频和视频的压缩与格式转换</p>

    <div class="features">
      <div class="feature-card" @click="$router.push('/image')">
        <div class="icon">🖼️</div>
        <h3>图片处理</h3>
        <p>支持 PNG、JPG、WebP、GIF、BMP 等格式互转，可调节压缩质量</p>
      </div>

      <div class="feature-card" @click="$router.push('/audio')">
        <div class="icon">🎵</div>
        <h3>音频处理</h3>
        <p>支持 MP3、WAV、OGG、FLAC、AAC 等格式互转，可调节比特率</p>
      </div>

      <div class="feature-card" @click="$router.push('/video')">
        <div class="icon">🎬</div>
        <h3>视频处理</h3>
        <p>支持 MP4、AVI、MKV、WebM、MOV 等格式互转，可调节压缩率</p>
      </div>
    </div>

    <div class="tech-info">
      <h3>技术栈</h3>
      <ul>
        <li>前端：Vue 3 + Vue Router + Axios + Vite</li>
        <li>后端：Python Flask + SQLite</li>
        <li>媒体处理：Pillow (图片) + FFmpeg (音频/视频)</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem 0;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #666;
  font-size: 0.9rem;
}

.tech-info {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: left;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.tech-info h3 {
  margin-bottom: 1rem;
}

.tech-info li {
  padding: 0.3rem 0;
  color: #555;
}
</style>
