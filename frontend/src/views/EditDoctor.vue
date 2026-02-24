<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Edit Doctor</h2>
      <div class="input-group">
        <select
          v-model="form.specialization"
          class="specialization-select"
          required>
          <option value="" disabled>-- Select Specialization --</option>
          <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div class="input-group">
        <input
          type="number"
          placeholder="Experience (Years)"
          v-model="form.experience_years"/>
      </div>
      <button class="login-btn" @click="updateDoctor">
        Update Doctor
      </button>
      <router-link to="/admin/dashboard" class="register-text">
        ← Back to Dashboard
      </router-link>
    </div>
  </div>
</template>
<script>
import api from "../services/api";
export default {
  name: "EditDoctor",
  data() {
    return {
      form: {
        specialization: "",
        experience_years: 0
      },
      specializations: [
        "Cardiologist",
        "Dermatologist",
        "General Physician",
        "Neurologist",
        "Orthopedic Surgeon",
        "Pediatrician",
        "Psychiatrist",
        "Surgeon"
      ]
    };
  },

  mounted() {
    this.loadDoctor();
  },

  methods: {
    async loadDoctor() {
      const doctorId = this.$route.params.id;
      try {
        const res = await api.get(`/admin/doctor/${doctorId}`);
        const doctor = res.data;
        this.form.specialization = doctor.specialization;
        this.form.experience_years = doctor.experience_years;
      } catch (err) {
        alert("Failed to load doctor details");
      }
    },

    async updateDoctor() {
      const doctorId = this.$route.params.id;

      try {
        await api.put(`/admin/doctor/${doctorId}`, this.form);
        alert("Doctor updated successfully");
        this.$router.push("/admin/dashboard");
      } catch (err) {
        alert("Failed to update doctor");
      }
    }
  }
};
</script>
