<template>
  <div class="page">
    <AppNavbar role="doctor" />
    <div class="section-card">
      <h2>Medical History for {{ $route.params.username }}</h2>
      
      <div v-if="history.length === 0" class="section-card center">
        <p>No history records found.</p>
      </div>

      <div v-else class="history-list">
        <div v-for="(h, i) in history" :key="i" class="big-history-box" style="margin-bottom: 20px; width: 100%;">
          <div class="history-content">
            <p><span>Date:</span> {{ h.date }}</p>
            <p><span>Diagnosis:</span> {{ h.diagnosis }}</p>
            <p><span>Prescription:</span> {{ h.prescription }}</p>
            <p><span>Notes:</span> {{ h.notes }}</p>
          </div>
        </div>
      </div>
      
      <button class="btn-primary" @click="$router.back()" style="margin-top: 20px;">
        ← Back
      </button>
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
