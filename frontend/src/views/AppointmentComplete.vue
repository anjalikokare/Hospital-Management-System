<template>
  <div class="complete-page">
    <div class="login-card">
      <h2>Complete Appointment</h2>
      <div class="input-group">
        <textarea
          placeholder="Enter diagnosis"
          v-model="diagnosis"
          rows="3"
        ></textarea>
      </div>
      <div class="input-group">
        <textarea
          placeholder="Enter prescription"
          v-model="prescription"
          rows="3"
        ></textarea>
      </div>
      <div class="input-group">
        <textarea
          placeholder="Additional notes"
          v-model="notes"
          rows="3"
        ></textarea>
      </div>
      <button class="login-btn" @click="submitTreatment">
        Save & Complete
      </button>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
export default {
  name: "AppointmentComplete",
  data() {
    return {
      diagnosis: "",
      prescription: "",
      notes: "",
      error: ""
    };
  },

  methods: {
    async submitTreatment() {
  this.error = "";

  try {
    await api.post(
      `/doctor/appointment/${this.$route.params.id}/treatment`,
      {
        diagnosis: this.diagnosis,
        prescription: this.prescription,
        notes: this.notes
      }
    );

    alert("Appointment completed successfully");
    this.$router.push("/doctor/dashboard");

  } catch (err) {
  if (err.response && err.response.status === 409) {
    this.error = "This appointment is already completed"
  } else {
    this.error = "Something went wrong"
  }
}
}

}
};
</script>
