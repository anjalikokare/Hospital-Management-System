<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Login</h2>
      <div class="input-group">
        <input
          type="text"
          placeholder="Username"
          v-model="username"/>
        <span class="icon">👤</span>
      </div>
      <div class="input-group">
        <input
          type="password"
          placeholder="Password"
          v-model="password"/>
        <span class="icon">🔒</span>
      </div>
      <button class="login-btn" @click="login">
        Login
      </button>
      <p v-if="error" class="error-text">{{ error }}</p>
      <p class="register-text">
        Don’t have an account?<router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      error: ""
    };
  },
  methods: {
    async login() {
      this.error = "";
      try {
        const response = await api.post("/auth/login", {
          username: this.username,
          password: this.password
        });

        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("role", response.data.role);

        if (response.data.role === "admin") {
          this.$router.push("/admin/dashboard");
        } else if (response.data.role === "doctor") {
          this.$router.push("/doctor/dashboard");
        } else {
          this.$router.push("/patient/dashboard");
        }
      } catch (err) {
        this.error = "Invalid username or password";
      }
    }
  }
};
</script>

