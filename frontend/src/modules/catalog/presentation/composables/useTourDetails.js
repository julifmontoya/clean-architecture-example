import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

export function useTourDetails() {
    const route = useRoute();

    const tour = ref(null);
    const loading = ref(true);
    const error = ref(null);

    const getTour = async () => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/v1/tours/${route.params.id}/`
            );

            if (!response.ok) {
                throw new Error("Unable to load tour");
            }

            tour.value = await response.json();
        } catch (err) {
            error.value = err.message;
        } finally {
            loading.value = false;
        }
    };

    onMounted(getTour);

    return {
        tour,
        loading,
        error,
    };
}
