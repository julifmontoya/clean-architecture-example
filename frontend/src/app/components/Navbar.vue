<script setup>
import { computed, ref } from "vue";
import { RouterLink } from "vue-router";

const isMenuOpen = ref(false);

const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || "";
const whatsappUrl = computed(() =>
    whatsappNumber ? `https://wa.me/${whatsappNumber}` : "#"
);

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
    isMenuOpen.value = false;
};
</script>

<template>
    <header class="border-b border-slate-200 bg-white">
        <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
            <RouterLink
                :to="{ name: 'home' }"
                class="text-lg font-bold tracking-tight text-slate-900"
                @click="closeMenu"
            >
                Tour<span class="text-blue-600">Explorer</span>
            </RouterLink>

            <nav class="hidden items-center gap-8 md:flex" aria-label="Principal">
                <RouterLink
                    :to="{ name: 'tours' }"
                    class="text-sm font-medium text-slate-600 transition hover:text-blue-600"
                >
                    Tours
                </RouterLink>

                <a
                    href="#contacto"
                    class="text-sm font-medium text-slate-600 transition hover:text-blue-600"
                >
                    Contáctenos
                </a>

                <a
                    :href="whatsappUrl"
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label="Contáctanos por WhatsApp"
                    class="flex items-center gap-2 rounded-full bg-green-50 px-4 py-2 text-sm font-medium text-green-700 transition hover:bg-green-100"
                >
                    <svg
                        class="h-4 w-4 shrink-0"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        aria-hidden="true"
                    >
                        <path
                            d="M12.04 2c-5.52 0-10 4.48-10 10 0 1.77.46 3.45 1.32 4.95L2 22l5.2-1.36a9.96 9.96 0 0 0 4.84 1.23h.01c5.52 0 10-4.48 10-10s-4.48-10-10.01-10zm5.85 14.3c-.25.7-1.24 1.28-2.02 1.44-.54.11-1.24.2-3.6-.77-3.02-1.25-4.97-4.32-5.12-4.52-.15-.2-1.22-1.63-1.22-3.1 0-1.48.76-2.2 1.03-2.5.27-.3.6-.37.8-.37.2 0 .4 0 .58.01.18.01.44-.07.68.53.25.6.86 2.08.93 2.23.07.15.12.33.02.53-.1.2-.15.33-.3.5-.15.18-.32.4-.45.53-.15.15-.3.32-.13.62.17.3.76 1.25 1.63 2.02 1.12 1 2.06 1.31 2.36 1.46.3.15.48.13.65-.08.18-.2.75-.87.95-1.17.2-.3.4-.25.68-.15.28.1 1.75.83 2.05.98.3.15.5.22.57.35.08.13.08.73-.17 1.43z"
                        />
                    </svg>
                    WhatsApp
                </a>
            </nav>

            <button
                type="button"
                class="inline-flex items-center justify-center rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 md:hidden"
                :aria-expanded="isMenuOpen"
                aria-controls="mobile-menu"
                :aria-label="isMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
                @click="toggleMenu"
            >
                <svg
                    v-if="!isMenuOpen"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M4 6h16M4 12h16M4 18h16"
                    />
                </svg>

                <svg
                    v-else
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                    />
                </svg>
            </button>
        </div>

        <nav
            v-if="isMenuOpen"
            id="mobile-menu"
            class="border-t border-slate-100 px-6 py-4 md:hidden"
            aria-label="Principal móvil"
        >
            <div class="flex flex-col gap-1">
                <RouterLink
                    :to="{ name: 'tours' }"
                    class="rounded-lg px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-blue-600"
                    @click="closeMenu"
                >
                    Tours
                </RouterLink>

                <a
                    href="#contacto"
                    class="rounded-lg px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-blue-600"
                    @click="closeMenu"
                >
                    Contáctenos
                </a>

                <a
                    :href="whatsappUrl"
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label="Contáctanos por WhatsApp"
                    class="mt-1 flex items-center gap-2 rounded-lg bg-green-50 px-3 py-3 text-sm font-medium text-green-700 transition hover:bg-green-100"
                    @click="closeMenu"
                >
                    <svg
                        class="h-4 w-4 shrink-0"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        aria-hidden="true"
                    >
                        <path
                            d="M12.04 2c-5.52 0-10 4.48-10 10 0 1.77.46 3.45 1.32 4.95L2 22l5.2-1.36a9.96 9.96 0 0 0 4.84 1.23h.01c5.52 0 10-4.48 10-10s-4.48-10-10.01-10zm5.85 14.3c-.25.7-1.24 1.28-2.02 1.44-.54.11-1.24.2-3.6-.77-3.02-1.25-4.97-4.32-5.12-4.52-.15-.2-1.22-1.63-1.22-3.1 0-1.48.76-2.2 1.03-2.5.27-.3.6-.37.8-.37.2 0 .4 0 .58.01.18.01.44-.07.68.53.25.6.86 2.08.93 2.23.07.15.12.33.02.53-.1.2-.15.33-.3.5-.15.18-.32.4-.45.53-.15.15-.3.32-.13.62.17.3.76 1.25 1.63 2.02 1.12 1 2.06 1.31 2.36 1.46.3.15.48.13.65-.08.18-.2.75-.87.95-1.17.2-.3.4-.25.68-.15.28.1 1.75.83 2.05.98.3.15.5.22.57.35.08.13.08.73-.17 1.43z"
                        />
                    </svg>
                    WhatsApp
                </a>
            </div>
        </nav>
    </header>
</template>
