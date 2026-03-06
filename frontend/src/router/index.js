import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import DoctorDashboard from "../views/DoctorDashboard.vue";
import PatientDashboard from "../views/PatientDashboard.vue";
import AddDoctor from "../views/AddDoctor.vue";
import EditDoctor from "../views/EditDoctor.vue";
import EditPatient from "../views/EditPatient.vue";
import EditProfile from "../views/EditProfile.vue";
import BookAppointment from "../views/BookAppointment.vue";
import PatientAppointments from "../views/PatientAppointments.vue";
import PatientHistory from "../views/PatientHistory.vue";
import PatientReschedule from "../views/PatientReschedule.vue";
import AppointmentCancel from "../views/AppointmentCancel.vue";
import AppointmentComplete from "../views/AppointmentComplete.vue";
import DoctorAvailability from "../views/DoctorAvailability.vue";
import DoctorPatientHistory from "../views/DoctorPatientHistory.vue";

const routes = [
    { path: "/", redirect: "/login" },
    { path: "/login", component: Login },
    { path: "/register", component: Register },
    { path: "/admin/dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" } },
    { path: "/admin/add-doctor", component: AddDoctor, meta: { requiresAuth: true, role: "admin" } },
    { path: "/admin/edit-doctor/:id", component: EditDoctor, meta: { requiresAuth: true, role: "admin" } },
    { path: "/admin/edit-patient/:id", component: EditPatient, meta: { requiresAuth: true, role: "admin" } },
    { path: "/doctor/dashboard", component: DoctorDashboard, meta: { requiresAuth: true, role: "doctor" } },
    { path: "/doctor/availability", component: DoctorAvailability, meta: { requiresAuth: true, role: "doctor" } },
    { path: "/doctor/patient-history/:username", component: DoctorPatientHistory, meta: { requiresAuth: true, role: "doctor" } },
    { path: "/doctor/appointment/:id/complete", component: AppointmentComplete, meta: { requiresAuth: true, role: "doctor" } },
    { path: "/doctor/appointment/:id/cancel", component: AppointmentCancel, meta: { requiresAuth: true, role: "doctor" } },
    { path: "/patient/dashboard", component: PatientDashboard, meta: { requiresAuth: true, role: "patient" } },
    { path: "/patient/book-appointment", component: BookAppointment, meta: { requiresAuth: true, role: "patient" } },
    { path: "/patient/appointments", component: PatientAppointments, meta: { requiresAuth: true, role: "patient" } },
    { path: "/patient/history", component: PatientHistory, meta: { requiresAuth: true, role: "patient" } },
    { path: "/patient/appointment/:id/reschedule", component: PatientReschedule, meta: { requiresAuth: true, role: "patient" } },
    { path: "/patient/edit-profile", component: EditProfile, meta: { requiresAuth: true, role: "patient" } },
    { path: "/admin", redirect: "/admin/dashboard" },
    { path: "/doctor", redirect: "/doctor/dashboard" },
    { path: "/patient", redirect: "/patient/dashboard" },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    if (to.meta.requiresAuth && !token) {
        next("/login");
    } else if (to.meta.role && role && to.meta.role !== role) {
        if (role === "admin") next("/admin/dashboard");
        else if (role === "doctor") next("/doctor/dashboard");
        else if (role === "patient") next("/patient/dashboard");
        else next("/login");
    } else {
        next();
    }
});

export default router;

