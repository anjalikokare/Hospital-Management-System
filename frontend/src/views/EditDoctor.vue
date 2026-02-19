<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Edit Doctor</h2>
      <div class="input-group">
        <input
          type="text"
          placeholder="Specialization"
          v-model="form.specialization"/>
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
      }
    };
  },

  mounted() {
    this.loadDoctor();
  },

  methods: {
    async loadDoctor() {
      const doctorId = this.$route.params.id;
      const res = await api.get("/admin/doctors");
      const doctor = res.data.find(d => d.doctor_id == doctorId);

      if (doctor) {
        this.form.specialization = doctor.specialization;
        this.form.experience_years = doctor.experience_years;
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
