<template>
  <div class="admin-dashboard-wrapper auth-bg edit-doctor-page">
    <AppNavbar role="admin" />
    <div class="admin-page flex-center" style="padding: 40px 0;">
      <div class="login-card transition-fade" style="padding: 50px 35px; max-width: 380px;">
        <h2 class="page-title center" style="margin-bottom: 25px; font-size: 1.8rem;">Edit Doctor</h2>
        
        <form @submit.prevent="updateDoctor" class="edit-form mt-10">
          <div class="form-group-vert" style="margin-bottom: 25px;">
            <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 10px;">Department</label>
            <div class="input-group">
              <select v-model="form.specialization" required class="form-input" style="padding: 12px 15px;">
                <option value="" disabled>Select Department</option>
                <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
          </div>

          <div class="form-group-vert" style="margin-bottom: 35px;">
            <label class="bold-label" style="font-size: 0.9rem; margin-bottom: 10px;">Experience (Years)</label>
            <div class="input-group">
              <input 
                type="number" 
                v-model="form.experience_years" 
                required 
                min="0" 
                class="form-input" 
                style="padding: 12px 15px;"
                placeholder="Years of experience" />
            </div>
          </div>

          <button type="submit" class="btn-primary btn-full" style="padding: 14px; font-size: 1rem;">
            Update Doctor
          </button>
          
          <div class="center mt-30">
            <button type="button" class="btn-transparent-back text-primary" @click="$router.push('/admin/dashboard')" style="font-weight: 600; text-decoration: none; border:none; background:none; cursor:pointer; font-size: 0.9rem;">
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
  name: "EditDoctor",
  components: { AppNavbar },
  data() {
    return {
      form: { specialization: "", experience_years: 0 },
      specializations: [
        "Cardiologist", "Dentist", "General Physician", 
        "Neurologist", "Orthopedic Surgeon"
      ]
    };
  },
  mounted() {
    this.loadDoctor();
  },
  methods: {
    async loadDoctor() {
      const id = this.$route.params.id;
      try {
        const res = await api.get(`/admin/doctor/${id}`);
        this.form.specialization = res.data.specialization;
        this.form.experience_years = res.data.experience_years;
      } catch (err) {
        this.$router.push("/admin/dashboard");
      }
    },
    async updateDoctor() {
      try {
        await api.put(`/admin/doctor/${this.$route.params.id}`, this.form);
        alert("Doctor updated!");
        this.$router.push("/admin/dashboard");
      } catch (err) {
        alert("Update failed.");
      }
    }
  }
};
</script>
