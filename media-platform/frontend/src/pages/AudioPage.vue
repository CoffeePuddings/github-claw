<template>
  <div class="media-page">
    <h2>🎵 音频压缩与格式转换</h2>
    <p class="desc">支持 MP3、WAV、OGG、FLAC、AAC 格式</p>

    <div class="upload-section">
      <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
        <input type="file" ref="fileInput" @change="handleFileSelect" accept="audio/*" hidden>
        <div v-if="!uploadedFile">
          <p class="upload-icon">🎵</p>
          <p>点击或拖拽音频文件到此处上传</p>
        </div>
        <div v-else class="file-info">
          <p>✅ {{ uploadedFile.filename }}</p>
          <p class="file-size">大小: {{ formatSize(uploadedFile.file_size) }}</p>
        </div>
      </div>
    </div>

    <div v-if="uploadedFile" class="options-section">
      <div class="option-group">
        <label>目标格式：</label>
        <select v-model="targetFormat">
          <option value="mp3">MP3</option>
          <option value="wav">WAV</option>
          <option value="ogg">OGG</option>
          <option value="flac">FLAC</option>
          <option value="aac">AAC</option>
        </select>
      </div>
      <div class="option-group">
        <label>比特率 (kbps)：</label>
        <select v-model.number="quality">
          <option :value="64">64 kbps</option>
          <option :value="96">96 kbps</option>
          <option :value="128">128 kbps</option>
          <option :value="192">192 kbps</option>
          <option :value="256">256 kbps</option>
          <option :value="320">320 kbps</option>
        </select>
      </div>
      <button class="btn-process" @click="startProcess" :disabled="processing">
        {{ processing ? '处理中...' : '开始处理' }}
      </button>
    </div>

    <div v-if="result" class="result-section">
      <h3>✅ 处理完成</h3>
      <p>输入大小: {{ formatSize(result.input_size) }}</p>
      <p>输出大小: {{ formatSize(result.output_size) }}</p>
      <p>压缩比: {{ result.compression_ratio }}%</p>
      <a :href="downloadUrl" class="btn-download">下载文件</a>
    </div>

    <div v-if="error" class="error-section">
      <p>❌ {{ error }}</p>
    </div>
  </div>
</template>

<script>
import { uploadFile, processFile, getDownloadUrl } from '../api.js'

export default {
  name: 'AudioPage',
  data() {
    return {
      uploadedFile: null,
      targetFormat: 'mp3',
      quality: 128,
      processing: false,
      result: null,
      error: null
    }
  },
  computed: {
    downloadUrl() {
      return this.result ? getDownloadUrl(this.result.output_file) : ''
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    async handleFileSelect(e) {
      const file = e.target.files[0]
      if (file) await this.upload(file)
    },
    async handleDrop(e) {
      const file = e.dataTransfer.files[0]
      if (file) await this.upload(file)
    },
    async upload(file) {
      this.error = null
      this.result = null
      try {
        this.uploadedFile = await uploadFile(file)
      } catch (err) {
        this.error = err.response?.data?.error || '上传失败'
      }
    },
    async startProcess() {
      this.processing = true
      this.error = null
      this.result = null
      try {
        this.result = await processFile(
          this.uploadedFile.stored_name,
          this.targetFormat,
          this.quality
        )
      } catch (err) {
        this.error = err.response?.data?.error || '处理失败'
      } finally {
        this.processing = false
      }
    },
    formatSize(bytes) {
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
    }
  }
}
</script>

<style scoped>
.media-page { padding: 1rem 0; }
h2 { margin-bottom: 0.5rem; }
.desc { color: #666; margin-bottom: 2rem; }

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;
  background: white;
}
.upload-area:hover { border-color: #667eea; }
.upload-icon { font-size: 3rem; margin-bottom: 1rem; }
.file-info { color: #333; }
.file-size { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }

.options-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.option-group {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.option-group label { min-width: 140px; font-weight: 500; }
.option-group select { flex: 1; }
select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.btn-process {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: opacity 0.3s;
}
.btn-process:hover { opacity: 0.9; }
.btn-process:disabled { opacity: 0.5; cursor: not-allowed; }

.result-section {
  background: #f0fff4;
  border: 1px solid #c6f6d5;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1.5rem;
}
.result-section h3 { color: #22543d; margin-bottom: 0.5rem; }
.result-section p { margin: 0.3rem 0; }

.btn-download {
  display: inline-block;
  background: #48bb78;
  color: white;
  text-decoration: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  margin-top: 1rem;
}

.error-section {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  color: #c53030;
}
</style>
