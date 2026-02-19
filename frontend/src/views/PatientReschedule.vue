<template>
  <div class="reschedule-page">
    <div class="reschedule-card">
      <h2>Reschedule Appointment</h2>

      <!-- DATE DROPDOWN -->
      <div class="form-group">
        <label>New Date</label>
        <select v-model="date">
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

      <!-- TIME INPUT -->
      <div class="form-group">
        <label>New Time</label>
        <input type="time" v-model="time" />
      </div>

      <div class="actions">
        <button class="btn-save" @click="save">
          Save
        </button>
        <button class="btn-cancel" @click="goBack">
          Cancel
        </button>
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

        alert("Appointment rescheduled successfully ✅");
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
