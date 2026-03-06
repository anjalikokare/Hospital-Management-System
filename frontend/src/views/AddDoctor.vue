<template>
  <div class="admin-dashboard-wrapper auth-bg">
    <AppNavbar role="admin" />
    <div class="admin-page flex-center bg-light">
      <div class="section-card narrow-card transition-fade">
        <h2 class="page-title center">Add New Doctor</h2>
        <p class="center form-subtitle">Register a new healthcare professional to the system.</p>
        
        <form @submit.prevent="addDoctor" class="edit-form">
          <div class="form-group-vert">
            <label class="bold-label">Username</label>
            <div class="input-group">
              <input type="text" placeholder="Enter username" v-model="form.username" class="form-input-transparent" required />
            </div>
          </div>

          <div class="form-group-vert">
            <label class="bold-label">Email Address</label>
            <div class="input-group">
              <input type="email" placeholder="Enter email" v-model="form.email" class="form-input-transparent" required />
            </div>
          </div>

          <div class="form-group-vert">
            <label class="bold-label">Password</label>
            <div class="input-group">
              <input type="password" placeholder="Create password" v-model="form.password" class="form-input-transparent" required />
            </div>
          </div>

          <div class="form-group-vert">
            <label class="bold-label">Specialization</label>
            <div class="input-group">
              <select v-model="form.specialization" class="premium-select select-transparent" required>
                <option value="" disabled>Select Specialization</option>
                <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
          </div>

          <div class="form-group-vert last">
            <label class="bold-label">Experience (Years)</label>
            <div class="input-group">
              <input type="number" placeholder="Years of experience" v-model="form.experience_years" class="form-input-transparent" required />
            </div>
          </div>

          <button type="submit" class="btn-primary btn-full mt-10">
            Register Doctor
          </button>
          
          <div class="center mt-15">
            <router-link to="/admin/dashboard" class="back-link text-primary" style="font-weight: 600; text-decoration: none;">Back to Dashboard</router-link>
          </div>
        </form>
      </div>
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
        "Dentist",
        "General Physician",
        "Neurologist",
        "Orthopedic Surgeon"
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



