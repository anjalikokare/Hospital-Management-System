<template>
  <div class="admin-dashboard-wrapper">
    <AppNavbar role="admin" />
    <div class="admin-page">
      <h2 class="page-title">Admin Dashboard</h2>

      <div class="stats-row">
        <div class="stat-card">
          <p>Total Doctors 👨‍⚕️</p>
          <h2>{{ stats.total_doctors }}</h2>
        </div>
        <div class="stat-card">
          <p>Total Patients 🧑‍🤝‍🧑</p>
          <h2>{{ stats.total_patients }}</h2>
        </div>
        <div class="stat-card">
          <p>Total Appointments 📅</p>
          <h2>{{ stats.total_appointments }}</h2>
        </div>
      </div>

      <!-- Doctor Management -->
      <div class="section-card">
        <div class="section-header">
          <h4>Doctor Management</h4>
          <div class="header-actions">
            <button class="btn-secondary" @click="runDailyReminders">
               🔔 Send Daily Reminders
            </button>
            <button class="btn-primary" @click="$router.push('/admin/add-doctor')">
              + Add Doctor
            </button>
          </div>
        </div>

        <input
          class="search"
          placeholder="Search by specialization"
          v-model="doctorSearch"
          @input="fetchDoctors"/>

        <table class="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Specialization</th>
              <th>Experience</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="doctors.length === 0">
              <td colspan="7" class="center">No doctors found</td>
            </tr>
            <tr v-for="(d, i) in doctors" :key="d.doctor_id">
              <td>{{ i + 1 }}</td>
              <td>{{ d.username }}</td>
              <td>{{ d.email }}</td>
              <td>{{ d.specialization }}</td>
              <td>{{ d.experience_years }}</td>
              <td>
                <span :class="d.is_active ? 'badge active' : 'badge blocked'">
                  {{ d.is_active ? "Active" : "Blocked" }}
                </span>
              </td>
              <td class="action-cell">
                <button class="icon-btn edit" @click="editDoctor(d.doctor_id)">
                  ✏️
                </button>
                <button
                  :class="d.is_active ? 'btn-danger' : 'btn-success'"
                  @click="toggleUser(d.user_id)"
                >
                  {{ d.is_active ? "Block" : "Unblock" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="section-card">
        <h4>Patient Management</h4>
        <input
          class="search"
          placeholder="Search patient by name"
          v-model="patientSearch"
          @input="fetchPatients"/>

        <table class="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Contact</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr v-if="patients.length === 0">
              <td colspan="9" class="center">No patients found</td>
            </tr>

            <tr v-for="(p, i) in patients" :key="p.patient_id">
              <td>{{ i + 1 }}</td>
              <td>{{ p.username }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.contact || "-" }}</td>
              <td>
                <span :class="p.is_active ? 'badge active' : 'badge blocked'">
                  {{ p.is_active ? "Active" : "Blocked" }}
                </span>
              </td>
              <td>
                <button :class="p.is_active ? 'btn-danger' : 'btn-success'" @click="toggleUser(p.user_id)">
                  {{ p.is_active ? "Block" : "Unblock" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Appointment Management -->
      <div class="section-card">
        <h4>Appointment Management</h4>
        <table class="styled-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Doctor</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="appointments.length === 0">
              <td colspan="5" class="center">No appointments found</td>
            </tr>
            <tr v-for="(a, i) in appointments" :key="a.appointment_id">
              <td>{{ i + 1 }}</td>
              <td>{{ a.patient_username }}</td>
              <td>{{ a.doctor_username }}</td>
              <td>{{ a.appointment_date }}</td>
              <td>
                <span class="badge active">{{ a.status }}</span>
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
  name: "AdminDashboard",
  components: { AppNavbar },
  data() {
    return {
      stats: {
        total_doctors: 0,
        total_patients: 0,
        total_appointments: 0,
      },
      doctors: [],
      patients: [],
      appointments: [],
      doctorSearch: "",
      patientSearch: "",
      reportReady: false,
    };
  },

  mounted() {
    this.fetchStats();
    this.fetchDoctors();
    this.fetchPatients();
    this.fetchAppointments();
  },

  methods: {
    async fetchStats() {
      const res = await api.get("/admin/dashboard");
      this.stats = res.data;
    },

    async fetchDoctors() {
      const res = await api.get("/admin/doctors", {
        params: { specialization: this.doctorSearch },
      });
      this.doctors = res.data;
    },

    async fetchPatients() {
      const res = await api.get("/admin/patients", {
        params: { username: this.patientSearch },
      });
      this.patients = res.data;
    },

    async fetchAppointments() {
      const res = await api.get("/admin/appointments");
      this.appointments = res.data;
    },

    async toggleUser(userId) {
      if (!confirm("Are you sure?")) return;
      await api.put(`/admin/user/${userId}`);
      this.fetchDoctors();
      this.fetchPatients();
    },

    editDoctor(doctorId) {
      this.$router.push(`/admin/edit-doctor/${doctorId}`);
    },
    async runDailyReminders() {
      try {
        await api.post("/admin/run-daily-reminders");
        alert("Daily reminders job triggered. Check the celery worker terminal for email logs.");
      } catch (err) {
        alert("Failed to trigger reminders");
      }
    },
  },
};
</script>
