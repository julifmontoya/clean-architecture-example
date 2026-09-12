export default class GetFeaturedTours {
    constructor(featuredTourRepository) {
        this.featuredTourRepository = featuredTourRepository;
    }

    async execute() {
        return this.featuredTourRepository.getAll();
    }
}
