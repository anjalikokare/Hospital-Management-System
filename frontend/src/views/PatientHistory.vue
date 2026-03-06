<template>
  <div class="dashboard-bg flex-center">
    <div class="big-history-box">
      <h2 class="title">Patient History</h2>
      <p v-if="history.length === 0" class="empty">
        No treatment history found
      </p>
      <div v-else>
        <div
          v-for="(h, i) in history"
          :key="i"
          class="history-content">
          <p><span>Date:</span> {{ h.date }}</p>
          <p><span>Diagnosis:</span> {{ h.diagnosis }}</p>
          <p><span>Prescription:</span> {{ h.prescription }}</p>
          <p><span>Notes:</span> {{ h.notes }}</p>
          <hr v-if="i !== history.length - 1" />
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import api from "../services/api";
export default {
  data() {
    return {
      history: []
    };
  },
  async mounted() {
    const username = this.$route.params.username;
    const res = await api.get(
      `/doctor/patient/${username}/history`
    );
    this.history = res.data;
  }
};
</script>

