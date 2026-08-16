<script setup>
import { useTourList } from "../composables/useTourList";

const {
    route,
    tours,
    loading,
    favorites,
    toggleFavorite,
    getImage,
    goToDetails,
} = useTourList();
</script>

<template>
    <main class="min-h-screen bg-slate-50">
        <!-- Page header -->
        <section class="border-b border-slate-200 bg-white">
            <div class="mx-auto max-w-7xl px-6 py-8">
                <div class="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <p class="text-sm font-semibold uppercase tracking-wide text-blue-600">
                            Explora nuevos destinos
                        </p>

                        <h1 class="mt-1 text-3xl font-bold tracking-tight text-slate-900">
                            Tours y experiencias
                        </h1>

                        <p class="mt-2 text-slate-500">
                            Encuentra experiencias únicas para tu próximo viaje.
                        </p>
                    </div>

                    <div v-if="route.query.title" class="rounded-xl bg-blue-50 px-4 py-3 text-sm text-blue-700">
                        Buscando:
                        <span class="font-bold">
                            "{{ route.query.title }}"
                        </span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Content -->
        <section class="mx-auto max-w-7xl px-6 py-8">
            <!-- Toolbar -->
            <div v-if="!loading && tours.length" class="mb-6 flex items-center justify-between">
                <p class="text-sm font-medium text-slate-700">
                    Resultados encontrados
                    <span class="font-bold text-slate-900">
                        ({{ tours.length }})
                    </span>
                </p>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <div v-for="item in 6" :key="item" class="overflow-hidden rounded-2xl border border-slate-200 bg-white">
                    <div class="h-52 animate-pulse bg-slate-200"></div>

                    <div class="space-y-3 p-5">
                        <div class="h-5 w-3/4 animate-pulse rounded bg-slate-200"></div>

                        <div class="h-4 w-1/2 animate-pulse rounded bg-slate-200"></div>

                        <div class="h-4 w-full animate-pulse rounded bg-slate-200"></div>

                        <div class="h-10 w-full animate-pulse rounded bg-slate-200"></div>
                    </div>
                </div>
            </div>

            <!-- Empty -->
            <div v-else-if="tours.length === 0"
                class="rounded-2xl border border-slate-200 bg-white px-6 py-20 text-center">
                <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-2xl">
                    🔎
                </div>

                <h2 class="mt-5 text-xl font-bold text-slate-900">
                    No encontramos tours
                </h2>

                <p class="mt-2 text-sm text-slate-500">
                    Intenta buscar otro destino o término.
                </p>
            </div>

            <!-- Tour grid -->
            <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <article v-for="(tour, index) in tours" :key="tour.id"
                    class="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
                    <!-- Image -->
                    <div class="relative h-52 overflow-hidden">
                        <img :src="getImage(index)" :alt="tour.title"
                            class="h-full w-full object-cover transition duration-500 group-hover:scale-105" />

                        <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent">
                        </div>

                        <!-- Category -->
                        <div class="absolute left-4 top-4">
                            <span class="rounded-full bg-white px-3 py-1.5 text-xs font-bold text-slate-800 shadow-sm">
                                {{ tour.category.title }}
                            </span>
                        </div>

                        <!-- Favorite -->
                        <button type="button"
                            class="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-black/20 text-white backdrop-blur transition hover:bg-white hover:text-red-500"
                            @click="toggleFavorite(tour.id)">
                            <svg class="h-5 w-5" :class="favorites.includes(tour.id)
                                ? 'fill-red-500 text-red-500'
                                : 'fill-transparent'
                                " viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 000-7.78z" />
                            </svg>
                        </button>
                    </div>

                    <!-- Content -->
                    <div class="p-5">
                        <!-- Title -->
                        <h2
                            class="line-clamp-2 min-h-[48px] text-lg font-bold leading-6 text-slate-900 transition group-hover:text-blue-600">
                            {{ tour.title }}
                        </h2>

                        <!-- Duration -->
                        <div class="mt-3 flex items-center gap-2 text-sm text-slate-500">
                            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="9" />

                                <path stroke-linecap="round" d="M12 7v5l3 2" />
                            </svg>

                            <span>
                                {{ tour.duration }}
                                {{ tour.duration === 1 ? "día" : "días" }}
                            </span>
                        </div>

                        <!-- Description -->
                        <p class="mt-4 line-clamp-2 min-h-[42px] text-sm leading-5 text-slate-600">
                            {{ tour.description }}
                        </p>

                        <!-- Included -->
                        <div v-if="tour.included_not_included?.included?.length"
                            class="mt-5 border-t border-slate-100 pt-4">
                            <p class="text-sm font-semibold text-slate-900">
                                Incluye
                            </p>

                            <ul class="mt-2 space-y-1">
                                <li v-for="item in tour.included_not_included.included.slice(
                                    0,
                                    2
                                )" :key="item" class="flex gap-2 text-xs text-slate-500">
                                    <span class="text-emerald-500">✓</span>

                                    <span class="line-clamp-1">
                                        {{ item }}
                                    </span>
                                </li>
                            </ul>
                        </div>

                        <!-- Price + action -->
                        <div class="mt-5 flex items-end justify-between border-t border-slate-100 pt-5">
                            <div>
                                <p class="text-xs text-slate-400">
                                    Desde
                                </p>

                                <p v-if="tour.min_price_adult !== null" class="text-xl font-bold text-blue-600">
                                    ${{ tour.min_price_adult }}
                                </p>

                                <p v-else class="text-sm font-semibold text-slate-500">
                                    Consultar precio
                                </p>
                            </div>

                            <button type="button" @click="goToDetails(tour.id)"
                                class="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700">
                                Ver detalles
                            </button>
                        </div>
                    </div>
                </article>
            </div>
        </section>
    </main>
</template>