<template>
  <div class="admin-page">
    <h2 class="page-title">My Appointments</h2>
    <div class="section-card">
      <table class="styled-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Doctor</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="appointments.length === 0">
            <td colspan="6" class="center">No appointments</td>
          </tr>
          <tr v-for="(a, i) in appointments" :key="a.appointment_id">
            <td>{{ i + 1 }}</td>
            <td>{{ a.doctor_username }}</td>
            <td>{{ a.date }}</td>
            <td>{{ a.time }}</td>
            <td>
              <span
                class="badge"
                :class="a.status === 'Booked' ? 'active' : 'blocked'">
                {{ a.status }}
              </span>
            </td>
            <td>
              <button
                v-if="a.status === 'Booked'"
                class="btn-warning btn-sm"
                @click="openReschedule(a)">
                Reschedule
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="showReschedule" class="reschedule-box">
      <h3>Reschedule Appointment</h3>
      <label>New Date</label>
      <input type="date" v-model="newDate" />
      <label>New Time</label>
      <input type="time" v-model="newTime" />
      <div class="reschedule-actions">
        <button class="btn-success" @click="submitReschedule">
          Save
        </button>
        <button class="btn-secondary" @click="showReschedule = false">
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
export default {
  name: "PatientAppointments",
  data() {
    return {
      appointments: [],
      showReschedule: false,
      selectedAppointment: null,
      newDate: "",
      newTime: ""
    };
  },

  mounted() {
    this.fetchAppointments();
  },

  methods: {
    async fetchAppointments() {
      const res = await api.get("/patient/appointments");
      this.appointments = res.data;
    },

    openReschedule(a) {
      this.selectedAppointment = a;
      this.newDate = a.date;
      this.newTime = a.time;
      this.showReschedule = true;
    },

    async submitReschedule() {
      try {
        await api.put(
          `/patient/appointment/${this.selectedAppointment.appointment_id}/reschedule`,
          {
            date: this.newDate,
            time: this.newTime
          }
        );

        alert("Appointment rescheduled successfully");
        this.showReschedule = false;
        this.fetchAppointments();
      } catch (err) {
        alert(
          err.response?.data?.message ||
          "Unable to reschedule appointment"
        );
      }
    }
  }
};
</script>

