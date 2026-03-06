<template>
  <div class="admin-dashboard-wrapper auth-bg edit-profile-page">
    <AppNavbar role="patient" />
    <div class="admin-page flex-center bg-light">
      <div class="section-card narrow-card transition-fade">
        <h2 class="page-title center">Edit Profile</h2>
        <p class="center form-subtitle">Keep your contact and personal information up to date.</p>
        
        <form @submit.prevent="saveProfile" class="edit-form">
          <div class="form-group-vert">
            <label class="bold-label">Contact Number</label>
            <div class="input-group">
              <input
                class="form-input-transparent"
                placeholder="e.g. +91 9876543210"
                v-model="patient.contact"
                required />
            </div>
          </div>
          
          <div class="form-group-vert">
            <label class="bold-label">Age</label>
            <div class="input-group">
              <input
                class="form-input-transparent"
                type="number"
                placeholder="Enter your age"
                v-model="patient.age"
                required />
            </div>
          </div>
          
          <div class="form-group-vert">
            <label class="bold-label">Gender</label>
            <div class="input-group">
              <select class="form-input-transparent" v-model="patient.gender" required>
                <option value="" disabled>Select Gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
          </div>
          
          <div class="form-group-vert last">
            <label class="bold-label">Address</label>
            <div class="input-group" style="align-items: flex-start; padding-top: 10px;">
              <textarea
                class="form-input-transparent"
                placeholder="Enter your full address"
                v-model="patient.address"
                rows="2"
                required></textarea>
            </div>
          </div>
          
          <button type="submit" class="btn-primary btn-full">
            Save Profile Changes
          </button>
          
          <p v-if="message" class="success-text center mt-15">
            {{ message }}
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";
export default {
  name: "EditProfile",
  components: { AppNavbar },

  data() {
    return {
      message: "",
      patient: {
        contact: "",
        age: "",
        gender: "",
        address: ""
      }
    };
  },

  mounted() {
    this.loadProfile();
  },

  methods: {
    async loadProfile() {
      try {
        const res = await api.get("/patient/profile");
        this.patient = res.data;
      } catch (e) {
        console.log("Unable to load profile");
      }
    },

    async saveProfile() {
      try {
        await api.put("/patient/profile", this.patient);
        this.message = "Profile updated successfully";
      } catch (e) {
        alert("Profile update failed");
      }
    }
  }
};
</script>

