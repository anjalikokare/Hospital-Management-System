<template>
  <div class="doctor-dashboard-wrapper">
    <AppNavbar role="doctor" />
    <div class="doctor-page">
      <h2 class="page-title">Doctor Dashboard</h2>
      <div class="stats-row">
        <div class="stat-card">
          <p>Today’s Appointments 📅</p>
          <h2>{{ stats.today }}</h2>
        </div>
        <div class="stat-card">
          <p>Total Patients 🧑‍🤝‍🧑</p>
          <h2>{{ stats.patients }}</h2>
        </div>
      </div>
      <div class="section-card">
        <div class="section-header">
          <h3>📄 Monthly Reports</h3>
          <button class="btn-primary" @click="downloadMonthlyReport">📊 Generate Report</button>
        </div>
        <p class="muted">View and download your monthly performance reports (PDF)</p>
        
        <ul class="report-list" style="margin-top:20px;">
          <li v-if="reports.length === 0" class="report-item">No reports generated yet.</li>
          <li v-for="report in reports" :key="report" class="report-item">
             📄 {{ report }}
             <a :href="ROOT_URL + '/static/reports/' + report" target="_blank" class="view-link">View Report</a>
          </li>
        </ul>
      </div>
      <div class="section-card">
        <h3>My Appointments</h3>

        <table class="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="appointments.length === 0">
              <td colspan="6" class="center">No appointments found</td>
            </tr>
            <tr v-for="(a, i) in appointments" :key="a.appointment_id">
              <td>{{ i + 1 }}</td>
              <td>{{ a.patient }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>
                <span
                  class="btn-warn"
                  :class="{ 'active': a.status === 'Completed', 'blocked': a.status === 'Cancelled' }">
                  {{ a.status }}
                </span>
              </td>
              <td>
                <button
                  v-if="a.status === 'Booked'"
                  class="btn-success btn-sm"
                  @click="$router.push(`/doctor/appointment/${a.appointment_id}/complete`)">
                  Complete
                </button>
                <button
                  v-if="a.status === 'Booked'"
                  class="btn-danger btn-sm"
                  @click="$router.push(`/doctor/appointment/${a.appointment_id}/cancel`)">
                  Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="section-card">
        <h3>My Patients</h3>
        <table class="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Patient Name</th>
              <th>Last Visit</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="patients.length === 0">
              <td colspan="4" class="center">No patients yet</td>
            </tr>
            <tr v-for="(p, i) in patients" :key="p.name">
              <td>{{ i + 1 }}</td>
              <td>{{ p.name }}</td>
              <td>{{ p.last_visit }}</td>
              <td>
                <button
                  class="btn-primary btn-sm"
                  @click="viewHistory(p.name)">
                  View History
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="section-card">
        <h3>My Availability (Next 7 Days)</h3>
        <p class="muted">Select date and available slots.</p>

        <div class="availability-form">
          <label>Date</label>
          <input type="date" v-model="availabilityForm.date" />

          <div class="slot-options">
            <label>
              <input type="checkbox" v-model="availabilityForm.morning_slot" />
              Morning Slot
            </label>
            <label>
              <input type="checkbox" v-model="availabilityForm.evening_slot" />
              Evening Slot
            </label>
          </div>

          <button class="btn-primary" @click="updateAvailability">
            Save Availability
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api, { ROOT_URL } from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  name: "DoctorDashboard",
  components: { AppNavbar },

  data() {
    return {
      ROOT_URL,
      stats: { today: 0, patients: 0 },
      appointments: [],
      patients: [],
      reportMsg: "",
      reports: [],
      availabilityForm: {
        date: "",
        morning_slot: false,
        evening_slot: false,
      },
    };
  },

  mounted() {
    this.fetchAppointments();
    this.fetchReports();
  },

  methods: {
    async fetchAppointments() {
      const res = await api.get("/doctor/appointments");
      this.appointments = res.data;
      this.calculateStats();
      this.preparePatients();
    },

    async downloadMonthlyReport() {
      try {
        this.reportMsg = "Generating report...";
        await api.post("/doctor/monthly-report/generate");
        this.reportMsg = "Report generated successfully!";
        this.fetchReports();
      } catch (e) {
        this.reportMsg = e.response?.data?.message || "Report generation failed.";
      }
    },

    async fetchReports() {
      try {
        const res = await api.get("/doctor/reports");
        this.reports = res.data;
      } catch (err) {
        console.error("Failed to fetch reports");
      }
    },

    calculateStats() {
      const today = new Date().toISOString().split("T")[0];
      this.stats.today = this.appointments.filter(
        (a) => a.date === today
      ).length;
    },

    preparePatients() {
      const map = {};
      this.appointments.forEach((a) => {
        if (!map[a.patient]) {
          map[a.patient] = {
            name: a.patient,
            last_visit: a.date,
          };
        }
      });
      this.patients = Object.values(map);
      this.stats.patients = this.patients.length;
    },

    viewHistory(username) {
      this.$router.push(`/doctor/patient-history/${username}`);
    },

    async updateAvailability() {
      try {
        if (!this.availabilityForm.date) {
          alert("Please select date");
          return;
        }

        await api.post("/doctor/availability", this.availabilityForm);
        alert("Availability updated successfully ✅");

        this.availabilityForm = {
          date: "",
          morning_slot: false,
          evening_slot: false,
        };
      } catch (err) {
        alert("Failed to update availability");
      }
    },
  },
};
</script>

<style scoped>
.doctor-dashboard-wrapper {
  display: flex;
  flex-direction: column;
}
</style>
