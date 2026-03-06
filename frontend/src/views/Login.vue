<template>
  <div class="auth-bg flex-center">
    <div class="login-card transition-fade" style="padding: 40px 30px; max-width: 380px;">
      <h2 class="page-title center" style="margin-bottom: 20px; font-size: 1.8rem;">Login</h2>
      
      <form @submit.prevent="login" class="edit-form mt-10">
        <div class="form-group-vert" style="margin-bottom: 20px;">
          <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 8px;">Username</label>
          <div class="input-group">
            <input
              type="text"
              placeholder="Username"
              v-model="username"
              class="form-input"
              style="padding: 12px 15px;"
              required />
          </div>
        </div>
        
        <div class="form-group-vert" style="margin-bottom: 25px;">
          <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 8px;">Password</label>
          <div class="input-group">
            <input
              type="password"
              placeholder="Password"
              v-model="password"
              class="form-input"
              style="padding: 12px 15px;"
              required />
          </div>
        </div>
        
        <button type="submit" class="btn-primary btn-full" style="padding: 14px; font-size: 1rem;">
          Login Account
        </button>
        
        <p v-if="error" class="error-text center mt-15" style="font-size: 0.85rem;">{{ error }}</p>
        
        <div class="center mt-25">
          <p class="form-subtitle" style="font-size: 0.9rem; margin-bottom: 0;">
            Don't have an account? 
            <router-link to="/register" class="text-primary" style="font-weight: 600; text-decoration: none;">Register Now</router-link>
          </p>
        </div>
      </form>
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


