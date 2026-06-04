import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 600000
})

export async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

export async function processFile(storedName, targetFormat, quality, operation = 'convert') {
  const response = await api.post('/process', {
    stored_name: storedName,
    target_format: targetFormat,
    quality: quality,
    operation: operation
  })
  return response.data
}

export async function downloadFile(filename) {
  const response = await api.get(`/download/${filename}`, {
    responseType: 'blob'
  })
  return response.data
}

export async function getTasks() {
  const response = await api.get('/tasks')
  return response.data
}

export function getDownloadUrl(filename) {
  return `/api/download/${filename}`
}
