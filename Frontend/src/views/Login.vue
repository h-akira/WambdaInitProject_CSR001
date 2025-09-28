<template>
  <div class="login">
    <div class="login-card">
      <h1>ログインが必要です</h1>
      <p>このページは認証が必要です。ログインページにリダイレクトします。</p>
      <div class="loading">
        <div class="spinner"></div>
        <p>リダイレクト中...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  mounted() {
    // Redirect to backend login
    const nextUrl = this.$route.query.next || '/app/'
    window.location.href = `/accounts/login?next=${encodeURIComponent(nextUrl)}`
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
}

.login-card h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.login-card p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
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
</style>