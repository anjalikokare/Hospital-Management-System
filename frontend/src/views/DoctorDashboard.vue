<template>
  <div class="doctor-dashboard-wrapper dashboard-bg">
    <AppNavbar role="doctor" />
    <div class="doctor-page">
      <h2 class="page-title">Doctor Workspace</h2>
      <div class="stats-row">
        <div class="stat-card blue-card">
          <p>Today’s Appointments</p>
          <h2>{{ stats.today }}</h2>
        </div>
        <div class="stat-card blue-card" @click="currentTab = 'patients'">
          <p>Assigned Patients</p>
          <h2>{{ stats.patients }}</h2>
        </div>
        <div class="stat-card blue-card" @click="currentTab = 'appointments'">
          <p>Upcoming (7 Days)</p>
          <h2>{{ stats.upcoming }}</h2>
        </div>
      </div>
      <div class="tab-bar">
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'appointments' }"
          @click="currentTab = 'appointments'"
        >
          My Appointments
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'patients' }"
          @click="currentTab = 'patients'"
        >
          Assigned Patients
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'availability' }"
          @click="currentTab = 'availability'"
        >
          Set Availability
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'reports' }"
          @click="currentTab = 'reports'"
        >
          Export Report
        </button>
      </div>
      <div class="tab-content">
        <div v-if="currentTab === 'appointments'" class="section-card transition-fade">
          <h3>My Upcoming Appointments</h3>
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
                    class="badge"
                    :class="{ 'badge-success': a.status === 'Completed', 'badge-danger': a.status === 'Cancelled', 'badge-warning': a.status === 'Booked' }">
                    {{ a.status }}
                  </span>
                </td>
                <td>
                  <div class="action-container">
                    <div class="action-btns" v-if="a.status === 'Booked'" style="display: flex; gap: 10px;">
                      <button class="btn-success btn-sm" @click="completeAppointment(a.appointment_id)">
                        Complete
                      </button>
                      <button class="btn-danger btn-sm" @click="cancelAppointment(a.appointment_id)">
                        Cancel
                      </button>
                    </div>
                    <span v-else-if="a.status === 'Completed'" class="text-success fw-bold">
                      Processed
                    </span>
                    <span v-else>-</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentTab === 'patients'" class="section-card transition-fade">
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
                <td colspan="4" class="center">No patients found</td>
              </tr>
              <tr v-for="(p, i) in patients" :key="p.name">
                <td>{{ i + 1 }}</td>
                <td>{{ p.name }}</td>
                <td>{{ p.last_visit }}</td>
                <td>
                  <button class="btn-primary btn-sm" @click="viewHistory(p.name)">View History</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentTab === 'availability'" class="section-card transition-fade center">
          <h3 class="mb-10">Manage Availability</h3>
          <p class="muted mb-30">Select date and slots for next 7 days.</p>
          <div class="availability-form">
            <div class="form-group-flex-center mb-20" style="display: flex; justify-content: center; align-items: center; gap: 15px;">
              <label class="bold-label" style="white-space: nowrap;">Select Date:</label>
              <input type="date" v-model="availabilityForm.date" class="form-input" style="max-width: 250px;" />
            </div>
            <div class="slot-options mt-20" style="text-align: left; display: inline-block;">
              <label class="d-block mb-10">
                <input type="checkbox" v-model="availabilityForm.morning_slot" />
                <span class="ml-10">Morning Slot (9 AM - 1 PM)</span>
              </label>
              <label class="d-block mb-10">
                <input type="checkbox" v-model="availabilityForm.evening_slot" />
                <span class="ml-10">Evening Slot (4 PM - 8 PM)</span>
              </label>
            </div>
            <div class="mt-30">
              <button class="btn-primary" style="width: 100%; max-width: 350px;" @click="updateAvailability">
                Save Availability
              </button>
            </div>
          </div>
        </div>
        <div v-if="currentTab === 'reports'" class="section-card transition-fade center">
          <h3 class="mb-10">Monthly Activity Report</h3>
          <p class="muted mb-30">Receive your appointment summary via email.</p>
          <div class="availability-form">
            <p class="small-text mb-20">The report will be sent as a CSV attachment to your registered email address.</p>
            <button class="btn-primary" style="width: 100%; max-width: 350px;" @click="generateReport" :disabled="loadingReport">
              {{ loadingReport ? 'Processing...' : 'Send Report to My Email' }}
            </button>
            <p v-if="reportMsg" class="success-text mt-15">{{ reportMsg }}</p>
            <p v-if="reportError" class="error-text mt-15">{{ reportError }}</p>
          </div>
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
      currentTab: 'appointments',
      loadingReport: false,
      stats: { today: 0, patients: 0, upcoming: 0 },
      appointments: [],
      patients: [],
      reportMsg: "",
      reportError: "",
      availabilityForm: {
        date: "",
        morning_slot: false,
        evening_slot: false,
      },
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.fetchAppointments();
    },
    async fetchAppointments() {
      const res = await api.get("/doctor/appointments");
      this.appointments = res.data;
      this.calculateStats();
      this.preparePatients();
    },
    async generateReport() {
      try {
        this.loadingReport = true;
        this.reportMsg = "Processing report...";
        this.reportError = "";
        await api.post("/doctor/monthly-report/generate");
        this.reportMsg = "Activity report has been sent to your email!";
      } catch (e) {
        this.reportMsg = "";
        this.reportError = e.response?.data?.message || "Sending failed.";
      } finally {
        this.loadingReport = false;
      }
    },
    calculateStats() {
      const todayStr = new Date().toISOString().split("T")[0];
      this.stats.today = this.appointments.filter(a => a.date === todayStr).length;
      this.stats.upcoming = this.appointments.filter(a => a.status === 'Booked').length;
    },
    preparePatients() {
      const map = {};
      this.appointments.forEach((a) => {
        if (!map[a.patient]) {
          map[a.patient] = { name: a.patient, last_visit: a.date };
        }
      });
      this.patients = Object.values(map);
      this.stats.patients = this.patients.length;
    },
    viewHistory(username) {
      this.$router.push(`/doctor/patient-history/${username}`);
    },
    completeAppointment(id) {
       this.$router.push(`/doctor/appointment/${id}/complete`);
    },
    async cancelAppointment(id) {
       if(!confirm("Cancel this appointment?")) return;
       await api.get(`/appointment/cancel/${id}`);
       this.fetchAppointments();
    },
    async updateAvailability() {
      try {
        if (!this.availabilityForm.date) return alert("Select date");
        await api.post("/doctor/availability", this.availabilityForm);
        alert("Availability saved!");
        this.availabilityForm = { date: "", morning_slot: false, evening_slot: false };
      } catch (err) {
        alert("Failed to save.");
      }
    },
  },
};
</script>

