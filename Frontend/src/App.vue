<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">WAMBDA CSR001</router-link>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <router-link to="/protected">Protected</router-link>
          <template v-if="authStatus && authStatus.authenticated">
            <a href="/accounts/profile" class="account-link">
              <span class="user-icon">👤</span> {{ authStatus.username }}
            </a>
            <button @click="logout" class="logout-btn">Logout</button>
          </template>
          <template v-else>
            <button @click="login" class="login-btn">Login</button>
          </template>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      authStatus: null
    }
  },
  async mounted() {
    await this.checkAuthStatus()
    this.handleRedirectAfterLogin()
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
    logout() {
      window.location.href = '/accounts/logout'
    },
    login() {
      window.location.href = '/accounts/login'
    },
    handleRedirectAfterLogin() {
      // Check if there's a 'next' parameter in the URL
      const urlParams = new URLSearchParams(window.location.search)
      const nextPath = urlParams.get('next')

      if (nextPath && this.authStatus && this.authStatus.authenticated) {
        // Remove the 'next' parameter from URL and navigate to the target path
        const url = new URL(window.location)
        url.searchParams.delete('next')
        window.history.replaceState({}, '', url.pathname + url.search)

        // Navigate to the target path using Vue Router
        this.$router.push(nextPath)
      }
    }
  }
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
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-links a.router-link-active {
  background-color: #3498db;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c0392b;
}

.login-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #2980b9;
}

.account-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.account-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-icon {
  font-size: 1.2rem;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}
</style>