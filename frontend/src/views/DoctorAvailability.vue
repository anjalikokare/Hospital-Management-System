<template>
  <div class="admin-page">
    <h2>Update Availability</h2>
    <form class="form-card">
      <label>Date</label>
      <input type="date" />
      <label>Time Slot</label>
      <input type="text" placeholder="10:00 - 12:00" />
      <button class="btn-primary">Save Availability</button>
    </form>
  </div>
</template>
<script>
export default {
  name: "DoctorAvailability"
};
</script>

