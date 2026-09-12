<script setup>
import { RouterLink } from "vue-router";

import { useTourDetails } from "../composables/useTourDetails";
import TourBookingCalculator from "../components/TourBookingCalculator.vue";

const { tour, loading, error } = useTourDetails();
</script>

<template>
    <main class="min-h-screen bg-gray-50">
        <!-- Loading -->
        <div
            v-if="loading"
            class="flex min-h-screen items-center justify-center"
        >
            <p class="text-gray-500">Cargando tour...</p>
        </div>

        <!-- Error -->
        <div
            v-else-if="error"
            class="flex min-h-screen items-center justify-center"
        >
            <p class="text-red-500">{{ error }}</p>
        </div>

        <!-- Tour -->
        <div v-else-if="tour" class="mx-auto max-w-6xl px-6 py-10">

            <!-- Breadcrumb -->
            <div class="mb-6 flex flex-wrap items-center gap-1 text-sm text-gray-500">
                <RouterLink
                    :to="{ name: 'tours' }"
                    class="hover:text-blue-600 hover:underline"
                >
                    Tours
                </RouterLink>

                <span>/</span>

                <RouterLink
                    :to="{ name: 'tours', query: { category: tour.category.title } }"
                    class="hover:text-blue-600 hover:underline"
                >
                    {{ tour.category.title }}
                </RouterLink>

                <span>/</span>

                <span class="text-gray-700">{{ tour.title }}</span>
            </div>

            <!-- Header -->
            <section class="rounded-2xl bg-white p-8 shadow-sm">
                <div
                    class="flex flex-col gap-8 md:flex-row md:items-start md:justify-between"
                >
                    <div class="max-w-3xl">

                        <span
                            class="inline-block rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700"
                        >
                            {{ tour.category.title }}
                        </span>

                        <h1
                            class="mt-4 text-4xl font-bold tracking-tight text-gray-900"
                        >
                            {{ tour.title }}
                        </h1>

                        <p class="mt-4 text-lg leading-8 text-gray-600">
                            {{ tour.description }}
                        </p>

                        <div class="mt-6 flex items-center gap-6 text-sm text-gray-600">
                            <div>
                                <span class="font-semibold text-gray-900">
                                    {{ tour.duration }}
                                </span>
                                días
                            </div>
                        </div>

                    </div>

                    <!-- Booking calculator -->
                    <TourBookingCalculator :tour="tour" />
                </div>
            </section>

            <!-- Itinerary -->
            <section class="mt-8 rounded-2xl bg-white p-8 shadow-sm">

                <h2 class="text-2xl font-bold text-gray-900">
                    Itinerario
                </h2>

                <div class="mt-8 space-y-8">

                    <div
                        v-for="day in tour.itinerary_days"
                        :key="day.day"
                        class="flex gap-5"
                    >
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600 font-bold text-white"
                        >
                            {{ day.day }}
                        </div>

                        <div>
                            <h3 class="text-lg font-semibold text-gray-900">
                                Día {{ day.day }}
                            </h3>

                            <p class="mt-2 leading-7 text-gray-600">
                                {{ day.description }}
                            </p>
                        </div>
                    </div>

                </div>
            </section>

            <!-- Included / Not Included -->
            <section class="mt-8 grid gap-8 md:grid-cols-2">

                <!-- Included -->
                <div class="rounded-2xl bg-white p-8 shadow-sm">

                    <h2 class="text-2xl font-bold text-gray-900">
                        ¿Qué incluye?
                    </h2>

                    <ul class="mt-6 space-y-4">
                        <li
                            v-for="item in tour.included_not_included.included"
                            :key="item"
                            class="flex gap-3 text-gray-600"
                        >
                            <span class="font-bold text-green-600">✓</span>
                            <span>{{ item }}</span>
                        </li>
                    </ul>

                </div>

                <!-- Not Included -->
                <div class="rounded-2xl bg-white p-8 shadow-sm">

                    <h2 class="text-2xl font-bold text-gray-900">
                        ¿Qué no incluye?
                    </h2>

                    <ul class="mt-6 space-y-4">
                        <li
                            v-for="item in tour.included_not_included.not_included"
                            :key="item"
                            class="flex gap-3 text-gray-600"
                        >
                            <span class="font-bold text-red-500">×</span>
                            <span>{{ item }}</span>
                        </li>
                    </ul>

                </div>

            </section>

        </div>
    </main>
</template>