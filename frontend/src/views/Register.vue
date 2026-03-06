<template>
  <div class="auth-bg flex-center">
    <div class="login-card transition-fade" style="padding: 40px 30px; max-width: 380px;">
      <h2 class="page-title center" style="margin-bottom: 15px; font-size: 1.8rem;">Register</h2>
            
      <form @submit.prevent="register" class="edit-form mt-10">
        <div class="form-group-vert" style="margin-bottom: 12px;">
          <label class="bold-label" style="font-size: 0.85rem; margin-bottom: 4px;">Username</label>
          <div class="input-group">
            <input type="text" placeholder="Username" v-model="username" class="form-input" style="padding: 10px 15px;" required />
          </div>
        </div>

        <div class="form-group-vert" style="margin-bottom: 12px;">
          <label class="bold-label" style="font-size: 0.85rem; margin-bottom: 4px;">Email Address</label>
          <div class="input-group">
            <input type="email" placeholder="Email" v-model="email" class="form-input" style="padding: 10px 15px;" required />
          </div>
        </div>

        <div class="form-group-vert" style="margin-bottom: 12px;">
          <label class="bold-label" style="font-size: 0.85rem; margin-bottom: 4px;">Contact Number</label>
          <div class="input-group">
            <input type="text" placeholder="Phone" v-model="contact" class="form-input" style="padding: 10px 15px;" required />
          </div>
        </div>

        <div class="form-group-vert" style="margin-bottom: 12px;">
          <label class="bold-label" style="font-size: 0.85rem; margin-bottom: 4px;">Password</label>
          <div class="input-group">
            <input type="password" placeholder="Password" v-model="password" class="form-input" style="padding: 10px 15px;" required />
          </div>
        </div>

        <div class="form-group-vert" style="margin-bottom: 18px;">
          <label class="bold-label" style="font-size: 0.85rem; margin-bottom: 4px;">Confirm Password</label>
          <div class="input-group">
            <input type="password" placeholder="Confirm" v-model="confirmPassword" class="form-input" style="padding: 10px 15px;" required />
          </div>
        </div>
          
        <button type="submit" class="btn-primary btn-full" style="padding: 12px; font-size: 1rem;">
          Register
        </button>
        
        <p v-if="error" class="error-text center mt-10" style="font-size: 0.8rem;">{{ error }}</p>
        <p v-if="success" class="success-text center mt-10" style="font-size: 0.8rem;">{{ success }}</p>
        
        <div class="center mt-15">
          <p class="form-subtitle" style="font-size: 0.9rem; margin-bottom: 0;">
            Already have an account? 
            <router-link to="/login" class="text-primary" style="font-weight: 600; text-decoration: none;">Login</router-link>
          </p>
        </div>
      </form>
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

