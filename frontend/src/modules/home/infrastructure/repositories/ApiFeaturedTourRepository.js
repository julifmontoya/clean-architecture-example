// src/modules/home/infrastructure/repositories/ApiFeaturedTourRepository.js

import api from "@/core/http/api";

export default class ApiFeaturedTourRepository {
    async getAll() {
        const response = await api.get("featured-tours/");

        return response.data;
    }
}
