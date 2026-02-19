<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Add Doctor</h2>
      <div class="input-group">
        <input
          type="text"
          placeholder="Username"
          v-model="form.username"
          required/>
        <span class="icon">👤</span>
      </div>
      <div class="input-group">
        <input
          type="email"
          placeholder="Email"
          v-model="form.email"
          required/>
        <span class="icon">📧</span>
      </div>
      <div class="input-group">
        <input
          type="password"
          placeholder="Password"
          v-model="form.password"
          required/>
        <span class="icon">🔒</span>
      </div>
      <div class="input-group">
        <select
          v-model="form.specialization"
          class="specialization-select"
          required>
          <option value="" disabled>-- Select Specialization --</option>
          <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
        </select>
        <span class="icon">🩺</span>
      </div>
      <div class="input-group">
        <input
          type="number"
          placeholder="Experience (Years)"
          v-model="form.experience_years"/>
        <span class="icon">📅</span>
      </div>
      <button class="login-btn" @click="addDoctor">
        Add Doctor
      </button>
      <p class="register-text">
        <router-link to="/admin/dashboard">← Back to Dashboard</router-link>
      </p>
    </div>
  </div>
</template>
<script>
import api from "../services/api";

export default {
  name: "AddDoctor",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        specialization: "",
        experience_years: 0,
        department_id: 1
      },
      specializations: [
        "Cardiologist",
        "Dermatologist",
        "Endocrinologist",
        "Gastroenterologist",
        "General Physician",
        "Gynecologist",
        "Hematologist",
        "Nephrologist",
        "Neurologist",
        "Oncologist",
        "Ophthalmologist",
        "Orthopedic Surgeon",
        "Pediatrician",
        "Psychiatrist",
        "Pulmonologist",
        "Radiologist",
        "Rheumatologist",
        "Surgeon",
        "Urologist",
        "ENT Specialist"
      ]
    };
  },

  methods: {
    async addDoctor() {
      try {
        await api.post("/admin/doctor", this.form);
        alert("Doctor added successfully");
        this.$router.push("/admin/dashboard");
      } catch (err) {
        alert(err.response?.data?.message || "Failed to add doctor");
      }
    }
  }
};
</script>
