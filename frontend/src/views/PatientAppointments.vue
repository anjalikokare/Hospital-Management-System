<template>
  <div class="dashboard-bg">
    <AppNavbar role="patient" />
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
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";
export default {
  name: "PatientAppointments",
  components: {
    AppNavbar
  },
  data() {
    return {
      appointments: [],
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
      this.$router.push(`/patient/appointment/${a.appointment_id}/reschedule`);
    },

  }
};
</script>


