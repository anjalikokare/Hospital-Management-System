<template>
  <div class="auth-bg flex-center">
    <div class="login-card transition-fade" style="padding: 40px 30px; max-width: 380px;">
      <h2 class="page-title center" style="margin-bottom: 20px; font-size: 1.8rem;">Reschedule Appointment</h2>
      
      <div class="edit-form mt-20">
        <div class="form-group-vert" style="margin-bottom: 20px;">
          <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 8px;">New Date</label>
          <div class="input-group">
            <select v-model="date" class="form-input" style="padding: 12px 15px;">
              <option value="">Select available date</option>
              <option
                v-for="(a, i) in availability"
                :key="i"
                :value="a.date"
              >
                {{ a.date }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-group-vert" style="margin-bottom: 25px;">
          <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 8px;">New Time</label>
          <div class="input-group">
            <input type="time" v-model="time" class="form-input" style="padding: 12px 15px;" />
          </div>
        </div>

        <div class="actions-row-column" style="display: flex; flex-direction: column; gap: 15px;">
          <button class="btn-primary btn-full" style="padding: 14px; font-size: 1rem;" @click="save">
            Update Appointment
          </button>
          
          <div class="center mt-10">
            <p class="form-subtitle" style="font-size: 0.9rem; cursor: pointer; color: #6366f1; font-weight: 600;" @click="goBack">
              Cancel & Go Back
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  name: "PatientReschedule",

  data() {
    return {
      date: "",
      time: "",
      availability: []
    };
  },

  mounted() {
    this.loadAvailability();
  },

  methods: {
    async loadAvailability() {
      const appointmentId = this.$route.params.id;

      const res = await api.get(
        `/patient/appointment/${appointmentId}/availability`
      );

      this.availability = res.data;
    },

    async save() {
      try {
        const id = this.$route.params.id;

        await api.put(
          `/patient/appointment/${id}/reschedule`,
          {
            date: this.date,
            time: this.time
          }
        );

        alert("Appointment rescheduled successfully");
        this.$router.push("/patient/dashboard");
      } catch (err) {
        alert(
          err.response?.data?.message ||
          "Unable to reschedule appointment"
        );
      }
    },

    goBack() {
      this.$router.push("/patient/dashboard");
    }
  }
};
</script>

