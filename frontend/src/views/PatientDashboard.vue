<template>
  <div class="patient-dashboard-wrapper">
    <AppNavbar role="patient" />
    <div class="patient-page">
      <h2 class="page-title">Patient Dashboard</h2>
      <div class="stats-row">
        <div class="stat-card">
          <p>My Appointments 📅</p>
          <h2>{{ appointments.length }}</h2>
        </div>
        <div class="stat-card">
          <p>Doctors 👨‍⚕️</p>
          <h2>{{ doctors.length }}</h2>
        </div>
        <div class="stat-card">
          <p>Status ✅</p>
          <b>Active</b>
        </div>
      </div>
      <div class="section-card action-buttons">
        <button class="btn-primary" @click="toggleBook">
          Book Appointment
        </button>
        <button class="btn-success" @click="toggleAppointments">
          My Appointments
        </button>
        <button class="btn-success" @click="toggleHistory">
          My Medical History
        </button>
      </div>
      <div v-if="showBook" class="section-card">
        <h3>Book Appointment</h3>
        <select v-model="form.doctor_id" class="search">
          <option value="">Select Doctor</option>
          <option v-for="d in doctors" :key="d.doctor_id" :value="d.doctor_id">
            {{ d.username }} ({{ d.specialization }})
          </option>
        </select>
        <select v-if="availableDates.length" v-model="form.date" class="search">
          <option value="">Select Available Date</option>
          <option v-for="(d, i) in availableDates" :key="i" :value="d">
            {{ d }}
          </option>
        </select>
        <input type="time" class="search" v-model="form.time" />
        <button class="btn-primary" @click="bookAppointment">
          Confirm Booking
        </button>
        <p v-if="message" class="success-text">{{ message }}</p>
        <p v-if="error" class="error-text">{{ error }}</p>
      </div>
      <div v-if="showAppointments" class="section-card">
        <h3>My Appointments</h3>
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
              <td><span class="btn-warn">{{ a.status }}</span></td>
              <td>
                <button
                  v-if="a.status === 'Booked'"
                  class="btn-warning btn-sm mr-2"
                  @click="goToReschedule(a)"
                >
                  Reschedule
                </button>
                <button
                  v-if="a.status === 'Booked'"
                  class="btn-danger btn-sm"
                  @click="cancelAppointment(a.appointment_id)">
                  Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="showHistory" class="section-card">
        <h3>My Medical History</h3>
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
              <td colspan="5" class="center">No medical history</td>
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
        <div class="section-card export-section">
          <h3>Export Treatment History</h3>
          <button class="btn-primary" @click="startExport">Export CSV</button>
          <button
            v-if="exportTaskId"
            class="btn-success ml-2"
            @click="checkExportStatus"
          >
            Check Export Status
          </button>

          <p v-if="exportStatus" class="info-text">
            Status: {{ exportStatus }}
          </p>

          <a
            v-if="downloadUrl"
            :href="downloadUrl"
            class="btn-success"
            download>
            Download CSV
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  name: "PatientDashboard",
  components: { AppNavbar },
  data() {
    return {
      doctors: [],
      availability: [],
      appointments: [],
      history: [],
      showBook: false,
      showAppointments: false,
      showHistory: false,
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
  },

  methods: {
    toggleBook() {
      this.showBook = !this.showBook;
      this.showAppointments = false;
      this.showHistory = false;
    },

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
      } catch (e) {
        this.error = e.response?.data?.message || "Booking failed";
      }
    },

    async toggleAppointments() {
      this.showAppointments = !this.showAppointments;
      this.showBook = false;
      this.showHistory = false;
      if (this.showAppointments) {
        const res = await api.get("/patient/appointments");
        this.appointments = res.data;
      }
    },

    async toggleHistory() {
      this.showHistory = !this.showHistory;
      this.showBook = false;
      this.showAppointments = false;
      if (this.showHistory) {
        const res = await api.get("/patient/medical-history");
        this.history = res.data;
      }
    },

    goToReschedule(a) {
      this.$router.push(`/patient/appointment/${a.appointment_id}/reschedule`);
    },

    async cancelAppointment(id) {
      await api.put(`/patient/appointment/${id}/cancel`);
      const res = await api.get("/patient/appointments");
      this.appointments = res.data;
    },
    async startExport() {
  try {
    const res = await api.post("/patient/export"); 
    this.exportTaskId = res.data.task_id;
    this.exportStatus = "Started... please wait.";
    this.downloadUrl = "";
  } catch (err) {
    console.error(err.response?.data || err.message);
    this.exportStatus = "Failed to start export.";
  }
},

    async checkExportStatus() {
      if (!this.exportTaskId) return;

      try {
        const res = await api.get(`/patient/export/${this.exportTaskId}`);
        this.exportStatus = res.data.state;

        if (res.data.state === "SUCCESS" && res.data.file) {
        this.downloadUrl = `http://127.0.0.1:5000/${res.data.file}`;
          this.exportStatus = "Completed ✅";
        }
      } catch (err) {
        console.error(err);
        this.exportStatus = "Error checking export status.";
      }
    },
  },
};
</script>

