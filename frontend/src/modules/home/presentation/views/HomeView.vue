<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const search = ref("");

const handleSearch = () => {
    router.push({
        name: "tours",
        query: {
            title: search.value,
        },
    });
};
</script>

<template>
    <main class="min-h-screen bg-slate-50">
        <section class="relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-600 via-indigo-600 to-violet-700"></div>

            <div class="relative mx-auto flex min-h-[520px] max-w-6xl flex-col items-center justify-center px-6 text-center">
                <span
                    class="mb-5 rounded-full bg-white/15 px-4 py-2 text-sm font-medium text-white backdrop-blur"
                >
                    Descubre tu próxima aventura
                </span>

                <h1
                    class="max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl"
                >
                    Encuentra el tour perfecto
                    <span class="text-blue-200">para tu próximo viaje</span>
                </h1>

                <p class="mt-5 max-w-2xl text-lg text-blue-100">
                    Explora experiencias inolvidables, destinos y tours
                    diseñados para tu próxima aventura.
                </p>

                <form
                    class="mt-10 flex w-full max-w-2xl flex-col gap-3 rounded-2xl bg-white p-3 shadow-2xl sm:flex-row"
                    @submit.prevent="handleSearch"
                >
                    <div class="flex flex-1 items-center gap-3 px-3">
                        <svg
                            class="h-6 w-6 shrink-0 text-slate-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M21 21l-4.35-4.35m2.35-5.65a8 8 0 11-16 0 8 8 0 0116 0z"
                            />
                        </svg>

                        <input
                            v-model="search"
                            type="text"
                            placeholder="¿A dónde quieres viajar?"
                            class="w-full border-0 bg-transparent py-3 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:ring-0"
                        />
                    </div>

                    <button
                        type="submit"
                        class="rounded-xl bg-blue-600 px-7 py-3 font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
                    >
                        Buscar tours
                    </button>
                </form>

                <div class="mt-5 flex flex-wrap justify-center gap-2 text-sm text-blue-100">
                    <span>Populares:</span>

                    <button
                        type="button"
                        class="rounded-full bg-white/10 px-3 py-1 backdrop-blur transition hover:bg-white/20"
                        @click="search = 'Cartagena'"
                    >
                        Cartagena
                    </button>

                    <button
                        type="button"
                        class="rounded-full bg-white/10 px-3 py-1 backdrop-blur transition hover:bg-white/20"
                        @click="search = 'Santa Marta'"
                    >
                        Santa Marta
                    </button>

                    <button
                        type="button"
                        class="rounded-full bg-white/10 px-3 py-1 backdrop-blur transition hover:bg-white/20"
                        @click="search = 'San Andrés'"
                    >
                        San Andrés
                    </button>
                </div>
            </div>
        </section>
    </main>
</template>