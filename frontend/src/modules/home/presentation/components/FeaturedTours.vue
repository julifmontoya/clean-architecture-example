<script setup>
import { RouterLink } from "vue-router";

import { useFeaturedTours } from "../composables/useFeaturedTours";

const { tours, loading, error, getImage, goToDetails, reload } = useFeaturedTours();

const formatPrice = (value) => Number(value).toLocaleString("en-US");
</script>

<template>
    <section class="bg-slate-50 py-20">
        <div class="mx-auto max-w-7xl px-6">
            <!-- Header -->
            <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <p class="text-sm font-semibold uppercase tracking-wide text-blue-600">
                        Tours destacados
                    </p>

                    <h2 class="mt-1 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                        Experiencias que te encantarán
                    </h2>

                    <p class="mt-3 max-w-xl text-slate-500">
                        Descubre algunos de nuestros tours más populares y comienza a
                        planear tu próxima aventura.
                    </p>
                </div>

                <RouterLink
                    :to="{ name: 'tours' }"
                    class="inline-flex shrink-0 items-center gap-1 font-semibold text-blue-600 transition hover:text-blue-700"
                >
                    Ver todos los tours →
                </RouterLink>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <div
                    v-for="item in 3"
                    :key="item"
                    class="overflow-hidden rounded-2xl border border-slate-200 bg-white"
                >
                    <div class="h-52 animate-pulse bg-slate-200"></div>

                    <div class="space-y-3 p-5">
                        <div class="h-5 w-3/4 animate-pulse rounded bg-slate-200"></div>
                        <div class="h-4 w-1/2 animate-pulse rounded bg-slate-200"></div>
                        <div class="h-4 w-full animate-pulse rounded bg-slate-200"></div>
                        <div class="h-10 w-full animate-pulse rounded bg-slate-200"></div>
                    </div>
                </div>
            </div>

            <!-- Error -->
            <div
                v-else-if="error"
                class="mt-10 rounded-2xl border border-red-100 bg-red-50 px-6 py-16 text-center"
            >
                <p class="text-sm font-semibold text-red-600">{{ error }}</p>

                <button
                    type="button"
                    class="mt-4 rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-red-700"
                    @click="reload"
                >
                    Reintentar
                </button>
            </div>

            <!-- Empty -->
            <div
                v-else-if="tours.length === 0"
                class="mt-10 rounded-2xl border border-slate-200 bg-white px-6 py-16 text-center"
            >
                <p class="text-lg font-bold text-slate-900">
                    Aún no hay tours destacados
                </p>

                <p class="mt-2 text-sm text-slate-500">
                    Vuelve pronto para descubrir nuevas experiencias.
                </p>
            </div>

            <!-- Tour cards -->
            <div v-else class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <article
                    v-for="(tour, index) in tours"
                    :key="tour.id"
                    class="group flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl"
                >
                    <!-- Image -->
                    <div class="relative h-52 overflow-hidden">
                        <img
                            :src="getImage(index)"
                            :alt="tour.title"
                            class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                        />

                        <div
                            class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"
                        ></div>

                        <div class="absolute left-4 top-4">
                            <span
                                class="rounded-full bg-white px-3 py-1.5 text-xs font-bold text-slate-800 shadow-sm"
                            >
                                {{ tour.category.title }}
                            </span>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="flex flex-1 flex-col p-5">
                        <h3
                            class="line-clamp-2 min-h-[48px] text-lg font-bold leading-6 text-slate-900 transition group-hover:text-blue-600"
                        >
                            {{ tour.title }}
                        </h3>

                        <div class="mt-3 flex items-center gap-2 text-sm text-slate-500">
                            <svg
                                class="h-4 w-4"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <circle cx="12" cy="12" r="9" />
                                <path stroke-linecap="round" d="M12 7v5l3 2" />
                            </svg>

                            <span>
                                {{ tour.duration }}
                                {{ tour.duration === 1 ? "día" : "días" }}
                            </span>
                        </div>

                        <p class="mt-4 line-clamp-2 min-h-[42px] text-sm leading-5 text-slate-600">
                            {{ tour.description }}
                        </p>

                        <div class="mt-auto pt-5">
                            <div class="border-t border-slate-100 pt-4">
                                <p class="text-xs text-slate-400">Desde</p>

                                <p
                                    v-if="tour.min_price_adult !== null"
                                    class="text-2xl font-bold text-blue-600"
                                >
                                    US$ {{ formatPrice(tour.min_price_adult) }}
                                </p>

                                <p v-else class="text-2xl font-bold text-slate-500">
                                    Consultar
                                </p>
                            </div>

                            <button
                                type="button"
                                class="mt-4 w-full rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
                                @click="goToDetails(tour.id)"
                            >
                                Ver detalles →
                            </button>
                        </div>
                    </div>
                </article>
            </div>
        </div>
    </section>
</template>
