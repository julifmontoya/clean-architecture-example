<script setup>
import { RouterView } from "vue-router";
import Navbar from "@/app/components/Navbar.vue";
import Footer from "@/app/components/Footer.vue";
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <Navbar />
    <RouterView class="flex-1" />
    <Footer />
  </div>
</template>
