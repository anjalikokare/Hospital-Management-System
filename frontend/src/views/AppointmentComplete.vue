<template>
  <div class="doctor-dashboard-wrapper auth-bg">
    <AppNavbar role="doctor" />
    <div class="admin-page flex-center bg-light">
      <div class="section-card narrow-card transition-fade">
        <h2 class="page-title center">Treatment Details</h2>
        <p class="center form-subtitle">Please enter the diagnosis and prescription for this session before marking it as completed.</p>
        
        <form @submit.prevent="submitTreatment" class="edit-form">
          <div class="form-group-vert">
            <label class="bold-label">Diagnosis</label>
            <textarea
              placeholder="e.g. Viral Fever, Common Cold..."
              v-model="diagnosis"
              rows="3"
              class="form-input textarea-input"
              required
            ></textarea>
          </div>
          
          <div class="form-group-vert">
            <label class="bold-label">Prescription</label>
            <textarea
              placeholder="e.g. Paracetamol 500mg, Rest for 2 days..."
              v-model="prescription"
              rows="3"
              class="form-input textarea-input"
              required
            ></textarea>
          </div>
          
          <div class="form-group-vert last">
            <label class="bold-label">Additional Notes (Optional)</label>
            <textarea
              placeholder="Any extra advice for the patient..."
              v-model="notes"
              rows="2"
              class="form-input textarea-input"
            ></textarea>
          </div>
          
          <div class="actions-row">
            <button type="submit" class="btn-primary flex-1">
              Save & Mark Completed
            </button>
            <button type="button" class="btn-danger-outline" @click="$router.push('/doctor/dashboard')">
              Cancel
            </button>
          </div>
          <p v-if="error" class="error-text center mt-15">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  name: "AppointmentComplete",
  components: { AppNavbar },
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

