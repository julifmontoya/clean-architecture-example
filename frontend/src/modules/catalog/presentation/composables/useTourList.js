import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import GetTours from "@/modules/catalog/application/use-cases/GetTours";
import ApiTourRepository from "@/modules/catalog/infrastructure/repositories/ApiTourRepository";

const tourImages = [
    "https://images.unsplash.com/photo-1587595431973-160d0d94add1?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1530789253388-582c481c54b0?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1533130061792-64b345e4a833?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=900&q=80",
];

export function useTourList() {
    const route = useRoute();
    const router = useRouter();

    const tours = ref([]);
    const loading = ref(false);
    const favorites = ref([]);

    const getTours = new GetTours(new ApiTourRepository());

    const toggleFavorite = (tourId) => {
        if (favorites.value.includes(tourId)) {
            favorites.value = favorites.value.filter((id) => id !== tourId);
            return;
        }

        favorites.value.push(tourId);
    };

    const getImage = (index) => {
        return tourImages[index % tourImages.length];
    };

    const goToDetails = (tourId) => {
        router.push({
            name: "tour-details",
            params: {
                id: tourId,
            },
        });
    };

    onMounted(async () => {
        loading.value = true;

        try {
            tours.value = await getTours.execute({
                title: route.query.title || "",
                category: route.query.category || "",
                duration: route.query.duration || "",
            });
        } finally {
            loading.value = false;
        }
    });

    return {
        route,
        tours,
        loading,
        favorites,
        toggleFavorite,
        getImage,
        goToDetails,
    };
}
