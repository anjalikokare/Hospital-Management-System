<template>
  <div class="admin-page">
    <h2>Patient History</h2>
    <p>Patient: {{ $route.params.username }}</p>
    <p class="muted">
      Treatment history will be shown here.
    </p>
  </div>
</template>
<script>
export default {
  name: "DoctorPatientHistory"
};
</script>
