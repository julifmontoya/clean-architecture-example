// src/modules/catalog/infrastructure/repositories/ApiTourRepository.js

import api from "@/core/http/api";

export default class ApiTourRepository {
    async getAll(filters = {}) {
        const response = await api.get("tours/", {
            params: filters,
        });

        return response.data;
    }
}