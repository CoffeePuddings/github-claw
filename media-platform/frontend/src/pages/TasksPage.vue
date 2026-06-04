<template>
  <div class="tasks-page">
    <h2>📋 任务记录</h2>
    <p class="desc">查看所有处理任务历史</p>

    <button class="btn-refresh" @click="loadTasks">刷新</button>

    <div v-if="tasks.length === 0" class="empty">
      <p>暂无任务记录</p>
    </div>

    <div v-else class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-card">
        <div class="task-header">
          <span class="task-type">{{ getTypeIcon(task.media_type) }} {{ task.media_type }}</span>
          <span :class="['status', task.status]">{{ getStatusText(task.status) }}</span>
        </div>
        <div class="task-body">
          <p><strong>文件:</strong> {{ task.filename }}</p>
          <p><strong>操作:</strong> {{ task.operation }} → {{ task.target_format }}</p>
          <p><strong>时间:</strong> {{ task.created_at }}</p>
        </div>
        <div v-if="task.status === 'completed' && task.output_path" class="task-footer">
          <a :href="getDownloadLink(task.output_path)" class="btn-download-sm">下载</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getTasks, getDownloadUrl } from '../api.js'

export default {
  name: 'TasksPage',
  data() {
    return {
      tasks: []
    }
  },
  mounted() {
    this.loadTasks()
  },
  methods: {
    async loadTasks() {
      try {
        this.tasks = await getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    },
    getTypeIcon(type) {
      const icons = { image: '🖼️', audio: '🎵', video: '🎬' }
      return icons[type] || '📄'
    },
    getStatusText(status) {
      const texts = { pending: '等待中', processing: '处理中', completed: '已完成', failed: '失败' }
      return texts[status] || status
    },
    getDownloadLink(outputPath) {
      const filename = outputPath.split('/').pop()
      return getDownloadUrl(filename)
    }
  }
}
</script>

<style scoped>
.tasks-page { padding: 1rem 0; }
h2 { margin-bottom: 0.5rem; }
.desc { color: #666; margin-bottom: 1.5rem; }

.btn-refresh {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 1.5rem;
}

.empty {
  text-align: center;
  padding: 3rem;
  color: #999;
  background: white;
  border-radius: 12px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-card {
  background: white;
  border-radius: 10px;
  padding: 1.2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.task-type { font-weight: 600; }

.status {
  padding: 0.2rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}
.status.completed { background: #c6f6d5; color: #22543d; }
.status.failed { background: #fed7d7; color: #c53030; }
.status.processing { background: #fefcbf; color: #744210; }
.status.pending { background: #e2e8f0; color: #4a5568; }

.task-body p {
  margin: 0.3rem 0;
  font-size: 0.9rem;
  color: #555;
}

.task-footer { margin-top: 0.8rem; }

.btn-download-sm {
  background: #48bb78;
  color: white;
  text-decoration: none;
  padding: 0.4rem 1rem;
  border-radius: 5px;
  font-size: 0.85rem;
}
</style>
