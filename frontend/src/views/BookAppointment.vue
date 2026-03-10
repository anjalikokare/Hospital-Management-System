<template>
  <div class="dashboard-bg flex-center">
    <div class="login-card">
      <h2>Book Appointment</h2>
      <div class="input-group">
        <select v-model="doctorId">
          <option disabled value="">Select Doctor</option>
          <option v-for="d in doctors" :key="d.doctor_id" :value="d.doctor_id">
            {{ d.username }} — {{ d.specialization }}
          </option>
        </select>
      </div>
      <div class="input-group">
        <input type="date" v-model="date" :min="todayDate" />
      </div>
      <div class="input-group">
        <input type="time" v-model="time" />
      </div>
      <button class="login-btn" @click="bookAppointment">
        Book Appointment
      </button>
      <p v-if="msg" class="success-text">{{ msg }}</p>
      <p v-if="error" class="error-text">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
export default {
  name: "BookAppointment",
  data() {
    return {
      doctors: [],
      doctorId: "",
      date: "",
      time: "",
      msg: "",
      error: ""
    };
  },
  computed: {
    todayDate() {
      return new Date().toISOString().split("T")[0];
    }
  },

  mounted() {
    this.fetchDoctors();
  },

  methods: {
    async fetchDoctors() {
      const res = await api.get("/patient/doctors");
      this.doctors = res.data;
    },

    async bookAppointment() {
      this.msg = "";
      this.error = "";

      try {
        await api.post("/patient/appointment", {
          doctor_id: this.doctorId,
          date: this.date,
          time: this.time
        });

        this.msg = "Appointment booked successfully!";
        setTimeout(() => this.$router.push("/patient/dashboard"), 1500);

      } catch (e) {
        this.error = e.response?.data?.message || "Failed";
      }
    }
  }
};
</script>

