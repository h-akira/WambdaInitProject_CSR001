<template>
  <div class="home">
    <div class="hero">
      <h1>WAMBDA CSR001 Sample</h1>
      <p class="subtitle">Vue.js + WAMBDA のサンプルアプリケーション</p>
    </div>

    <div class="content">
      <div class="welcome-card">
        <h2>Welcome!</h2>
        <p>このサンプルアプリケーションでは以下の機能を体験できます：</p>
        <ul>
          <li>Vue.js SPA (Single Page Application)</li>
          <li>WAMBDA バックエンド API</li>
          <li>AWS Cognito 認証</li>
          <li>保護されたページアクセス</li>
        </ul>
      </div>

      <div class="auth-status" v-if="authStatus">
        <h3>認証状況</h3>
        <div v-if="authStatus.authenticated" class="authenticated">
          <p>✅ ログイン済み</p>
          <p>ユーザー: {{ authStatus.username }}</p>
          <router-link to="/protected" class="btn btn-primary">
            保護されたページへ
          </router-link>
        </div>
        <div v-else class="not-authenticated">
          <p>❌ 未ログイン</p>
          <button @click="goToLogin" class="btn btn-primary">ログイン</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      authStatus: null
    }
  },
  async mounted() {
    await this.checkAuthStatus()
  },
  methods: {
    async checkAuthStatus() {
      try {
        const response = await fetch('/accounts/status')
        this.authStatus = await response.json()
      } catch (error) {
        console.error('Auth status check failed:', error)
        this.authStatus = { authenticated: false }
      }
    },
    goToLogin() {
      window.location.href = '/accounts/login'
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.content {
  display: grid;
  gap: 2rem;
}

.welcome-card, .auth-status {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.welcome-card h2, .auth-status h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.welcome-card ul {
  margin-left: 1.5rem;
  margin-top: 1rem;
}

.welcome-card li {
  margin-bottom: 0.5rem;
}

.authenticated {
  color: #27ae60;
}

.not-authenticated {
  color: #e74c3c;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
</style>