<template>
  <div class="protected">
    <div class="protected-card">
      <h1>🔒 保護されたページ</h1>
      <p>おめでとうございます！認証に成功しました。</p>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>データを読み込み中...</p>
      </div>

      <div v-else-if="apiData" class="api-data">
        <h2>API レスポンス</h2>
        <div class="response-card">
          <h3>{{ apiData.message }}</h3>
          <div class="details">
            <p><strong>ステータス:</strong> {{ apiData.status }}</p>
            <p><strong>ユーザー:</strong> {{ apiData.data?.user }}</p>
            <p><strong>メッセージ:</strong> {{ apiData.data?.greeting }}</p>
            <p><strong>タイムスタンプ:</strong> {{ formatDate(apiData.data?.timestamp) }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="error">
        <h3>❌ エラーが発生しました</h3>
        <p>{{ error }}</p>
        <button @click="fetchData" class="btn btn-primary">再試行</button>
      </div>

      <div class="actions">
        <router-link to="/" class="btn btn-secondary">ホームに戻る</router-link>
        <button @click="refreshData" class="btn btn-primary">データ更新</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Protected',
  data() {
    return {
      loading: true,
      apiData: null,
      error: null
    }
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      this.error = null

      try {
        const response = await fetch('/api/hello')

        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`)
        }

        this.apiData = await response.json()
      } catch (error) {
        console.error('API call failed:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    async refreshData() {
      await this.fetchData()
    },
    formatDate(timestamp) {
      if (!timestamp) return 'N/A'
      return new Date(timestamp).toLocaleString('ja-JP')
    }
  }
}
</script>

<style scoped>
.protected {
  max-width: 800px;
  margin: 0 auto;
}

.protected-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.protected-card h1 {
  color: #27ae60;
  margin-bottom: 1rem;
  font-size: 2.5rem;
}

.protected-card > p {
  color: #7f8c8d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.api-data {
  margin: 2rem 0;
}

.api-data h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.response-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  border-left: 4px solid #3498db;
  text-align: left;
}

.response-card h3 {
  color: #3498db;
  margin-bottom: 1rem;
}

.details {
  display: grid;
  gap: 0.5rem;
}

.details p {
  margin: 0;
}

.error {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c33;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}
</style>