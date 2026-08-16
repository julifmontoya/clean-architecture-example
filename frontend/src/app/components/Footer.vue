<script setup>
const currentYear = new Date().getFullYear();
</script>

<template>
    <footer class="border-t border-slate-200 bg-white">
        <div class="mx-auto max-w-7xl px-6 py-8">
            <div class="flex flex-col items-center justify-between gap-4 sm:flex-row">
                <p class="text-lg font-bold tracking-tight text-slate-900">
                    Tour<span class="text-blue-600">Explorer</span>
                </p>

                <p class="text-sm text-slate-500">
                    Explora experiencias y destinos únicos para tu próxima aventura.
                </p>
            </div>

            <div class="mt-6 border-t border-slate-100 pt-6 text-center text-sm text-slate-400">
                © {{ currentYear }} TourExplorer. Todos los derechos reservados.
            </div>
        </div>
    </footer>
</template>
