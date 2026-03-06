<template>
  <div class="patient-dashboard-wrapper dashboard-bg">
    <AppNavbar role="patient" />
    <div class="patient-page">
      <h2 class="page-title">My Health Portal</h2>
      <div class="stats-row">
        <div class="stat-card blue-card" @click="currentTab = 'appointments'">
          <p>My Appointments</p>
          <h2>{{ appointments.length }}</h2>
        </div>
        <div class="stat-card blue-card" @click="currentTab = 'book'">
          <p>Available Doctors</p>
          <h2>{{ doctors.length }}</h2>
        </div>
        <div class="stat-card blue-card">
          <p>Account Status</p>
          <b>Active</b>
        </div>
      </div>
      <div class="tab-bar">
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'book' }"
          @click="currentTab = 'book'"
        >
          Book Appointment
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'appointments' }"
          @click="currentTab = 'appointments'"
        >
          My Schedule
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'history' }"
          @click="currentTab = 'history'"
        >
          Medical History
        </button>
      </div>
      <div class="tab-content transition-fade">
        <div v-if="currentTab === 'book'" class="section-card">
          <h3>Schedule a Consultation</h3>
          <p class="muted">Select your preferred doctor and time slot.</p>
          <div class="booking-container">
            <select v-model="form.doctor_id" class="premium-search">
              <option value="">Choose Doctor</option>
              <option v-for="d in doctors" :key="d.doctor_id" :value="d.doctor_id">
                {{ d.username }} ({{ d.specialization }})
              </option>
            </select>
            <select v-if="availableDates.length" v-model="form.date" class="premium-search">
              <option value="">Select Available Date</option>
              <option v-for="(d, i) in availableDates" :key="i" :value="d">
                {{ d }}
              </option>
            </select>
            <input type="time" class="premium-search" v-model="form.time" />
            <button class="btn-primary btn-full" @click="bookAppointment">
              Confirm Booking
            </button>
            <p v-if="message" class="success-text">{{ message }}</p>
            <p v-if="error" class="error-text">{{ error }}</p>
          </div>
        </div>
        <div v-if="currentTab === 'appointments'" class="section-card">
          <h3>My Upcoming Appointments</h3>
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
                <td colspan="6" class="center">No appointments found.</td>
              </tr>
              <tr v-for="(a, i) in appointments" :key="a.appointment_id">
                <td>{{ i + 1 }}</td>
                <td>{{ a.doctor_username }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td>
                  <span class="badge" :class="a.status === 'Cancelled' ? 'badge-danger' : 'badge-warning'">
                    {{ a.status }}
                  </span>
                </td>
                <td>
                  <div class="action-btns" v-if="a.status === 'Booked'" style="display: flex; gap: 10px; align-items: center;">
                    <button class="btn-warning btn-sm" @click="goToReschedule(a)">Reschedule</button>
                    <button class="btn-danger btn-sm" @click="cancelAppointment(a.appointment_id)">Cancel</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentTab === 'history'">
          <div class="section-card transition-fade">
            <h3>My Medical Records</h3>
            <table class="styled-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Date</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="history.length === 0">
                  <td colspan="5" class="center">No medical records found.</td>
                </tr>
                <tr v-for="(h, i) in history" :key="i">
                  <td>{{ i + 1 }}</td>
                  <td>{{ h.date }}</td>
                  <td>{{ h.diagnosis }}</td>
                  <td>{{ h.prescription }}</td>
                  <td>{{ h.notes }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="section-card transition-fade">
            <h3>Export Health Data</h3>
            <p class="muted mb-10">Export your complete treatment history as a CSV file directly to your email.</p>
            <div class="mt-10">
              <button 
                class="btn-primary" 
                @click="handleExport" 
                :disabled="exportLoading"
                style="padding: 12px 25px;"
              >
                {{ exportLoading ? 'Downloading...' : 'Download My Records (CSV)' }}
              </button>
              <p v-if="exportMessage" class="success-text mt-10">{{ exportMessage }}</p>
            </div>
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
  name: "PatientDashboard",
  components: { AppNavbar },
  data() {
    return {
      currentTab: 'book',
      doctors: [],
      availability: [],
      appointments: [],
      history: [],
      message: "",
      error: "",
      form: {
        doctor_id: "",
        date: "",
        time: "",
      },
      exportTaskId: null,
      exportStatus: "",
      downloadUrl: "",
      exportLoading: false,
      exportInterval: null,
      exportMessage: "",
    };
  },
  computed: {
    availableDates() {
      return this.availability
        .filter((a) => a.morning_slot || a.evening_slot)
        .map((a) => a.date);
    },
  },
  mounted() {
    this.loadDoctors();
  },
  watch: {
    "form.doctor_id"(val) {
      this.form.date = "";
      this.form.time = "";
      if (val) this.loadAvailability(val);
      else this.availability = [];
    },
    currentTab(newTab) {
      if (newTab === 'appointments') this.loadAppointments();
      if (newTab === 'history') this.loadHistory();
    }
  },
  methods: {
    async loadDoctors() {
      const res = await api.get("/patient/doctors");
      this.doctors = res.data;
    },
    async loadAvailability(id) {
      const res = await api.get(`/patient/doctor/${id}/availability`);
      this.availability = res.data;
    },
    async bookAppointment() {
      this.message = "";
      this.error = "";
      if (!this.form.doctor_id || !this.form.date || !this.form.time) {
        this.error = "Please select doctor, date and time";
        return;
      }
      try {
        await api.post("/patient/appointment", this.form);
        this.message = "Appointment booked successfully";
        this.form.date = "";
        this.form.time = "";
        this.loadAppointments();
      } catch (e) {
        this.error = e.response?.data?.message || "Booking failed";
      }
    },
    async loadAppointments() {
       const res = await api.get("/patient/appointments");
       this.appointments = res.data;
    },
    async loadHistory() {
       const res = await api.get("/patient/medical-history");
       this.history = res.data;
    },
    goToReschedule(a) {
      this.$router.push(`/patient/appointment/${a.appointment_id}/reschedule`);
    },
    async cancelAppointment(id) {
      await api.put(`/patient/appointment/${id}/cancel`);
      this.loadAppointments();
    },
    async handleExport() {
      if (this.exportLoading) return;
      this.exportLoading = true;
      this.exportMessage = "";
      try {
        const res = await api.get("/patient/export", { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'medical_records.csv');
        document.body.appendChild(link);
        link.click();
        this.exportMessage = "Records downloaded successfully!";
        this.exportLoading = false;
      } catch (err) {
        this.exportLoading = false;
        console.error("Download failed", err);
      }
    },
  },
};
</script>
