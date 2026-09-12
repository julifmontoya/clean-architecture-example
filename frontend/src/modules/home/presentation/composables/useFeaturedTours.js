import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import GetFeaturedTours from "@/modules/home/application/use-cases/GetFeaturedTours";
import ApiFeaturedTourRepository from "@/modules/home/infrastructure/repositories/ApiFeaturedTourRepository";

const featuredTourImages = [
    "https://images.unsplash.com/photo-1587595431973-160d0d94add1?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1530789253388-582c481c54b0?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1533130061792-64b345e4a833?auto=format&fit=crop&w=900&q=80",
];

export function useFeaturedTours() {
    const router = useRouter();

    const tours = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const getFeaturedTours = new GetFeaturedTours(new ApiFeaturedTourRepository());

    const getImage = (index) => featuredTourImages[index % featuredTourImages.length];

    const goToDetails = (tourId) => {
        router.push({
            name: "tour-details",
            params: {
                id: tourId,
            },
        });
    };

    const load = async () => {
        loading.value = true;
        error.value = null;

        try {
            tours.value = await getFeaturedTours.execute();
        } catch (err) {
            error.value = "No pudimos cargar los tours destacados. Intenta de nuevo.";
        } finally {
            loading.value = false;
        }
    };

    onMounted(load);

    return {
        tours,
        loading,
        error,
        getImage,
        goToDetails,
        reload: load,
    };
}
