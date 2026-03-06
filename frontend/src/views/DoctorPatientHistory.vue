<template>
  <div class="doctor-dashboard-wrapper auth-bg flex-center">
    <div class="login-card transition-fade" style="max-width: 500px;">
      <h2 class="page-title center">Patient History: {{ $route.params.username }}</h2>
      
      <div v-if="history.length === 0" class="center mt-30">
        <p class="form-subtitle">No consultation records found.</p>
      </div>

      <div v-else class="mt-20">
        <div v-for="(h, i) in history" :key="i" class="history-entry mb-20">
          <p class="mb-5"><strong class="text-primary">Date:</strong> {{ h.date }}</p>
          
          <div class="mb-10">
            <p class="bold-label mb-2">Diagnosis</p>
            <p class="muted-text">{{ h.diagnosis }}</p>
          </div>

          <div class="mb-10">
            <p class="bold-label mb-2">Prescription</p>
            <p class="muted-text">{{ h.prescription }}</p>
          </div>

          <div v-if="h.notes" class="mb-10">
            <p class="bold-label mb-2">Doctor's Notes</p>
            <p class="small-text italic">{{ h.notes }}</p>
          </div>
          
          <hr v-if="i !== history.length - 1" class="simple-hr" />
        </div>
      </div>

      <div class="center mt-30">
        <button class="btn-primary" @click="$router.back()">
          Back to Dashboard
        </button>
      </div>
    </div>
  </div>
</template>



<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  name: "DoctorPatientHistory",
  components: { AppNavbar },
  data() {
    return {
      history: []
    };
  },
  mounted() {
    this.fetchHistory();
  },
  methods: {
    async fetchHistory() {
      const username = this.$route.params.username;
      try {
        const res = await api.get(`/doctor/patient/${username}/history`);
        this.history = res.data;
      } catch (err) {
        alert("Failed to load patient history");
      }
    }
  }
};
</script>

