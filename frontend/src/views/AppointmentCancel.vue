<template>
  <div class="doctor-dashboard-wrapper dashboard-bg">
    <AppNavbar role="doctor" />
    <div class="complete-page">
      <div class="login-card">
        <h2>Cancel Appointment</h2>
        <div class="input-group">
          <textarea
            placeholder="Reason for cancellation"
            v-model="reason"
            rows="3"
          ></textarea>
        </div>
        <button class="login-btn" @click="cancel">
          Confirm Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  components: { AppNavbar },
  data() {
    return { reason: "" };
  },
  methods: {
    async cancel() {
      const id = this.$route.params.id;

      await api.put(
        `/doctor/appointment/${id}/status`,
        { status: "Cancelled" }
      );

      this.$router.push("/doctor/dashboard");
    }
  }
};
</script>

