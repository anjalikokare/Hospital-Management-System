<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Register</h2>
      <div class="input-group">
        <input
          type="text"
          placeholder="Username"
          v-model="username" />
        <span class="icon">👤</span>
      </div>
      <div class="input-group register-email">
        <input
          type="email"
          placeholder="Email"
          v-model="email"/>
        <span class="icon">📧</span>
      </div>
      <div class="input-group">
        <input
          type="text"
          placeholder="Contact Number"
          v-model="contact" />
        <span class="icon">📞</span>
      </div>
      <div class="input-group">
        <input
          type="password"
          placeholder="Password"
          v-model="password"/>
        <span class="icon">🔒</span>
      </div>
      <div class="input-group register-confirm">
        <input
          type="password"
          placeholder="Confirm Password"
          v-model="confirmPassword"/>
        <span class="icon">🔒</span>
      </div>
      <button class="login-btn" @click="register">
        Register
      </button>
      <p v-if="error" class="error-text">{{ error }}</p>
      <p v-if="success" class="success-text">{{ success }}</p>
      <p class="register-text">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
export default {
  name: "Register",
  data() {
    return {
      username: "",
      email: "",
      contact: "",
      password: "",
      confirmPassword: "",
      error: "",
      success: ""
    };
  },

  methods: {
    async register() {
      this.error = "";
      this.success = "";

      if (
        !this.username ||
        !this.email ||
        !this.contact ||
        !this.password
      ) {
        this.error = "All fields are required";
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match";
        return;
      }

      try {
        await api.post("/auth/register", {
          username: this.username,
          email: this.email,
          contact: this.contact,
          password: this.password,
          role: "patient"
        });

        this.success = "Registration successful. Please login.";

        setTimeout(() => {
          this.$router.push("/login");
        }, 1500);

      } catch (err) {
        this.error = "Registration failed. Try again.";
      }
    }
  }
};
</script>
