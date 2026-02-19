<template>
  <div class="page">
    <AppNavbar role="patient" />
    <div class="section-card">
      <h3>Edit Profile</h3>
      <input
        class="search"
        placeholder="Contact Number"
        v-model="patient.contact"/>
      <input
        class="search"
        type="number"
        placeholder="Age"
        v-model="patient.age" />
      <select class="search" v-model="patient.gender">
        <option value="">Select Gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
      <input
        class="search"
        placeholder="Address"
        v-model="patient.address" />
      <button class="btn-primary" @click="saveProfile">
        Save Changes
      </button>
      <p v-if="message" class="success-text">
        {{ message }}
      </p>
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
