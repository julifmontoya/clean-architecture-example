<script setup>
import { RouterView } from "vue-router";
import Footer from "@/app/components/Footer.vue";
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <RouterView class="flex-1" />
    <Footer />
  </div>
</template>
