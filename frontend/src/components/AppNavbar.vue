<template>
  <nav class="navbar">
    <div class="nav-left">
      <h3>HMS</h3>
    </div>
    <div class="nav-right">
      <button class="nav-btn" @click="goHome">
        Home
      </button>
      <button class="nav-btn" @click="goEditProfile">
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
