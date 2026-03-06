<template>
  <nav class="navbar">
    <div class="logo-container" @click="goHome">
      <img src="../assets/1235896.jpeg" alt="HMS Logo" class="nav-logo" />
      <span class="logo-text">MEDCARE HMS</span>
    </div>
    <div class="nav-right">
      <button class="nav-btn" @click="goHome">
        Home
      </button>
      <button
        v-if="userRole === 'patient'"
        class="nav-btn"
        @click="goEditProfile">
        Edit Profile
      </button>
      <button class="nav-btn logout" @click="logout">
        Logout
      </button>
    </div>
  </nav>
</template>
<script>
export default {
  name: "AppNavbar",
  data() {
    return {
      userRole: localStorage.getItem("role")
    };
  },
  methods: {
    goHome() {
      const role = localStorage.getItem("role");
      if (role === "admin") this.$router.push("/admin/dashboard");
      else if (role === "doctor") this.$router.push("/doctor/dashboard");
      else this.$router.push("/patient/dashboard");
    },

    goEditProfile() {
      this.$router.push("/patient/edit-profile");
    },

    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    }
  }
};
</script>

