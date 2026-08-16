export default class GetTours {
    constructor(tourRepository) {
        this.tourRepository = tourRepository;
    }

    async execute(filters = {}) {
        return this.tourRepository.getAll(filters);
    }
}