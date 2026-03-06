<template>
  <div class="admin-dashboard-wrapper auth-bg edit-patient-page">
    <AppNavbar role="admin" />
    <div class="admin-page flex-center" style="padding: 20px 0;">
      <div class="login-card transition-fade" style="padding: 25px 30px; max-width: 360px;">
        <h2 class="page-title center" style="margin-bottom: 10px; font-size: 1.5rem;">Edit Patient</h2>
        <p class="center form-subtitle" style="margin-bottom: 15px; font-size: 0.85rem;">Update patient information.</p>
        
        <form @submit.prevent="updatePatient" class="edit-form">
          <div class="form-group-vert" style="margin-bottom: 8px;">
            <label class="bold-label" style="font-size: 0.8rem;">Username</label>
            <div class="input-group">
              <input type="text" v-model="form.username" disabled class="form-input" style="padding: 8px 12px; opacity: 0.7;" />
            </div>
          </div>

          <div class="form-group-vert" style="margin-bottom: 8px;">
            <label class="bold-label" style="font-size: 0.8rem;">Email Address</label>
            <div class="input-group">
              <input type="email" v-model="form.email" required class="form-input" style="padding: 8px 12px;" />
            </div>
          </div>

          <div class="form-group-vert" style="margin-bottom: 8px;">
            <label class="bold-label" style="font-size: 0.8rem;">Contact Number</label>
            <div class="input-group">
              <input type="text" v-model="form.contact" required class="form-input" style="padding: 8px 12px;" />
            </div>
          </div>

          <div class="form-group-vert" style="margin-bottom: 8px;">
            <label class="bold-label" style="font-size: 0.8rem;">Age</label>
            <div class="input-group">
              <input type="number" v-model="form.age" required class="form-input" style="padding: 8px 12px;" />
            </div>
          </div>

          <div class="form-group-vert last" style="margin-bottom: 15px;">
            <label class="bold-label" style="font-size: 0.8rem;">Gender</label>
            <div class="input-group">
              <select v-model="form.gender" required class="form-input" style="padding: 8px 12px;">
                <option value="" disabled>Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <button type="submit" class="btn-primary btn-full" :disabled="loading" style="padding: 10px; font-size: 0.9rem;">
            {{ loading ? "Saving..." : "Update Patient" }}
          </button>
          
          <div class="center mt-10">
            <button type="button" class="btn-transparent-back text-primary" @click="$router.push('/admin/dashboard')" style="font-weight: 600; border:none; background:none; cursor:pointer; font-size: 0.85rem;">
              Back to Dashboard
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";
import AppNavbar from "../components/AppNavbar.vue";

export default {
  name: "EditPatient",
  components: { AppNavbar },
  data() {
    return {
      loading: false,
      form: { username: "", email: "", contact: "", age: "", gender: "" }
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    try {
      const res = await api.get(`/admin/patient/${id}`);
      this.form = res.data;
    } catch (err) {
      this.$router.push("/admin/dashboard");
    }
  },
  methods: {
    async updatePatient() {
      this.loading = true;
      try {
        await api.put(`/admin/patient/${this.$route.params.id}`, this.form);
        alert("Patient updated!");
        this.$router.push("/admin/dashboard");
      } catch (err) {
        alert("Failed to update.");
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
