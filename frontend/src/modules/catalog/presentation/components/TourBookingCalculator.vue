<script setup>
import { computed, ref } from "vue";

const props = defineProps({
    tour: {
        type: Object,
        required: true,
    },
});

const MIN_ADULTS = 1;
const MIN_CHILDREN = 0;
const MIN_INFANTS = 0;

const adults = ref(MIN_ADULTS);
const children = ref(MIN_CHILDREN);
const infants = ref(MIN_INFANTS);

const incrementAdults = () => {
    adults.value += 1;
};
const decrementAdults = () => {
    if (adults.value > MIN_ADULTS) adults.value -= 1;
};
const incrementChildren = () => {
    children.value += 1;
};
const decrementChildren = () => {
    if (children.value > MIN_CHILDREN) children.value -= 1;
};
const incrementInfants = () => {
    infants.value += 1;
};
const decrementInfants = () => {
    if (infants.value > MIN_INFANTS) infants.value -= 1;
};

const hasPricing = computed(
    () => props.tour.min_price_adult !== null && props.tour.min_price_adult !== undefined
);

const priceAdult = computed(() => Number(props.tour.min_price_adult) || 0);
const priceChild = computed(() => Number(props.tour.price_child) || 0);
const priceInfant = computed(() => Number(props.tour.price_infant) || 0);

const adultTotal = computed(() => adults.value * priceAdult.value);
const childTotal = computed(() => children.value * priceChild.value);
const infantTotal = computed(() => infants.value * priceInfant.value);
const total = computed(() => adultTotal.value + childTotal.value + infantTotal.value);

const formatCurrency = (value) =>
    Number(value).toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });

const whatsappNumber = import.meta.env.VITE_WHATSAPP_NUMBER || "";

const whatsappMessage = computed(() =>
    [
        "Hola, quiero reservar este tour:",
        "",
        `Tour: ${props.tour.title}`,
        "",
        `Adultos: ${adults.value}`,
        `Niños: ${children.value}`,
        `Infantes: ${infants.value}`,
        "",
        `Total estimado: ${
            hasPricing.value ? `US$${formatCurrency(total.value)}` : "A consultar"
        }`,
    ].join("\n")
);

const whatsappUrl = computed(() =>
    whatsappNumber
        ? `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage.value)}`
        : "#"
);
</script>

<template>
    <div class="w-full rounded-xl bg-gray-900 p-6 text-white md:w-96">
        <p class="text-sm text-gray-400">Desde</p>

        <p class="mt-1 text-3xl font-bold">
            <template v-if="hasPricing">${{ formatCurrency(priceAdult) }}</template>
            <template v-else>Consultar</template>
        </p>

        <p class="mt-1 text-sm text-gray-400">por adulto</p>

        <!-- Passenger selectors -->
        <div class="mt-6 space-y-4 border-t border-gray-700 pt-6">
            <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-200">Adultos</span>

                <div class="flex items-center gap-3">
                    <button
                        type="button"
                        :disabled="adults <= MIN_ADULTS"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Disminuir adultos"
                        @click="decrementAdults"
                    >
                        −
                    </button>

                    <span class="w-4 text-center font-semibold">{{ adults }}</span>

                    <button
                        type="button"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700"
                        aria-label="Aumentar adultos"
                        @click="incrementAdults"
                    >
                        +
                    </button>
                </div>
            </div>

            <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-200">Niños</span>

                <div class="flex items-center gap-3">
                    <button
                        type="button"
                        :disabled="children <= MIN_CHILDREN"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Disminuir niños"
                        @click="decrementChildren"
                    >
                        −
                    </button>

                    <span class="w-4 text-center font-semibold">{{ children }}</span>

                    <button
                        type="button"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700"
                        aria-label="Aumentar niños"
                        @click="incrementChildren"
                    >
                        +
                    </button>
                </div>
            </div>

            <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-200">Infantes</span>

                <div class="flex items-center gap-3">
                    <button
                        type="button"
                        :disabled="infants <= MIN_INFANTS"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Disminuir infantes"
                        @click="decrementInfants"
                    >
                        −
                    </button>

                    <span class="w-4 text-center font-semibold">{{ infants }}</span>

                    <button
                        type="button"
                        class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-800 text-lg font-bold text-white transition hover:bg-gray-700"
                        aria-label="Aumentar infantes"
                        @click="incrementInfants"
                    >
                        +
                    </button>
                </div>
            </div>
        </div>

        <!-- Price summary -->
        <div v-if="hasPricing" class="mt-6 space-y-2 border-t border-gray-700 pt-6 text-sm text-gray-300">
            <div class="flex items-center justify-between">
                <span>Adultos</span>
                <span>{{ adults }} × ${{ formatCurrency(priceAdult) }}</span>
            </div>

            <div class="flex items-center justify-between">
                <span>Niños</span>
                <span>{{ children }} × ${{ formatCurrency(priceChild) }}</span>
            </div>

            <div class="flex items-center justify-between">
                <span>Infantes</span>
                <span>{{ infants }} × ${{ formatCurrency(priceInfant) }}</span>
            </div>
        </div>

        <p v-else class="mt-6 border-t border-gray-700 pt-6 text-sm text-gray-400">
            Precios sujetos a disponibilidad. Escríbenos por WhatsApp para cotizar tu grupo.
        </p>

        <div class="mt-4 flex items-center justify-between border-t border-gray-700 pt-4">
            <span class="text-base font-semibold text-white">Total</span>

            <span class="text-2xl font-bold text-white">
                {{ hasPricing ? `$${formatCurrency(total)}` : "Consultar" }}
            </span>
        </div>

        <a
            :href="whatsappUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700"
        >
            Reservar por WhatsApp
        </a>
    </div>
</template>
