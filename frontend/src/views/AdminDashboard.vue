<template>
  <div class="admin-dashboard-wrapper dashboard-bg">
    <AppNavbar role="admin" />
    <div class="admin-page">
      <h2 class="page-title">Admin Command Center</h2>
      <div class="stats-row">
        <div class="stat-card blue-card">
          <p>Total Doctors</p>
          <h2>{{ stats.total_doctors }}</h2>
        </div>
        <div class="stat-card blue-card">
          <p>Total Patients</p>
          <h2>{{ stats.total_patients }}</h2>
        </div>
        <div class="stat-card blue-card" @click="currentTab = 'appointments'">
          <p>Total Appointments</p>
          <h2>{{ stats.total_appointments }}</h2>
        </div>
      </div>
      <div class="tab-bar">
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'doctors' }"
          @click="currentTab = 'doctors'"
        >
          Doctor Management
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'patients' }"
          @click="currentTab = 'patients'"
        >
          Patient Management
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'appointments' }"
          @click="currentTab = 'appointments'"
        >
          Appointment Log
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'add-doctor' }"
          @click="currentTab = 'add-doctor'"
        >
          Add Doctor
        </button>
      </div>
      <div class="tab-content transition-fade">
        <div v-if="currentTab === 'doctors'" class="section-card">
          <div class="section-header">
            <h4>Doctor Directory</h4>
          </div>
          <select
            class="premium-search"
            v-model="doctorSearch"
            @change="fetchDoctors">
            <option value="">All Specializations (Filter)</option>
            <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
          </select>
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
                  <button class="icon-btn edit" @click="editDoctor(d.doctor_id)" title="Edit Doctor">
                    Edit
                  </button>
                  <button
                    :class="d.is_active ? 'icon-btn block-btn' : 'icon-btn unblock-btn'"
                    @click="toggleUser(d.user_id)"
                    :title="d.is_active ? 'Block Doctor' : 'Unblock Doctor'"
                  >
                    {{ d.is_active ? "Block" : "Unblock" }}
                  </button>
                  <button class="icon-btn delete-btn" @click="deleteUser(d.user_id)" title="Remove Doctor">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentTab === 'patients'" class="section-card">
          <h4>Patient Registry</h4>
          <input
            class="premium-search"
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
                <td colspan="6" class="center">No patients found</td>
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
                <td class="action-cell">
                  <button class="icon-btn edit" @click="editPatient(p.patient_id)" title="Edit Patient">
                    Edit
                  </button>
                  <button 
                    :class="p.is_active ? 'icon-btn block-btn' : 'icon-btn unblock-btn'" 
                    @click="toggleUser(p.user_id)"
                    :title="p.is_active ? 'Block Patient' : 'Unblock Patient'"
                  >
                    {{ p.is_active ? "Block" : "Unblock" }}
                  </button>
                  <button class="icon-btn delete-btn" @click="deleteUser(p.user_id)" title="Remove Patient">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="currentTab === 'appointments'" class="section-card">
          <h4>Master Appointment Schedule</h4>
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
        <div v-if="currentTab === 'add-doctor'" class="section-card transition-fade">
          <h4>Register New Doctor</h4>
          <div class="input-groups add-doctor-form">
            <div class="input-group">
              <input type="text" placeholder="Username" v-model="doctorForm.username" required />
            </div>
            <div class="input-group">
              <input type="email" placeholder="Email" v-model="doctorForm.email" required />
            </div>
            <div class="input-group">
              <input type="password" placeholder="Password" v-model="doctorForm.password" required />
            </div>
            <div class="input-group">
              <select v-model="doctorForm.specialization" class="premium-select" required>
                <option value="" disabled>Select Specialization</option>
                <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="input-group">
              <input type="number" placeholder="Experience (Years)" v-model="doctorForm.experience_years" />
            </div>
            <button class="btn-primary btn-primary-large" @click="addDoctor">
              Register Doctor
            </button>
          </div>
        </div>
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
      currentTab: 'doctors',
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
      doctorForm: {
        username: "",
        email: "",
        password: "",
        specialization: "",
        experience_years: 0,
        department_id: 1
      },
      specializations: [
        "Cardiologist", "Dentist", "General Physician", 
        "Neurologist", "Orthopedic Surgeon"
      ]
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
    editPatient(patientId) {
      this.$router.push(`/admin/edit-patient/${patientId}`);
    },
    async deleteUser(userId) {
      if (!confirm("Are you sure?")) return;
      try {
        await api.delete(`/admin/user/${userId}`);
        alert("User removed successfully");
        this.fetchDoctors();
        this.fetchPatients();
        this.fetchStats();
      } catch (err) {
        alert("Failed to remove user");
      }
    },
    async addDoctor() {
      try {
        await api.post("/admin/doctor", this.doctorForm);
        alert("Doctor added successfully");
        this.currentTab = 'doctors';
        this.fetchDoctors();
        this.fetchStats();
        this.doctorForm = {
          username: "", email: "", password: "", specialization: "", experience_years: 0, department_id: 1
        };
      } catch (err) {
        alert(err.response?.data?.message || "Failed to add doctor");
      }
    },
  },
};
</script>

