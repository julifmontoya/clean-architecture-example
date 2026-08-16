import TourListView from "../views/TourListView.vue";
import TourDetailsView from "../views/TourDetailsView.vue";

export default [
  {
    path: "/tours",
    name: "tours",
    component: TourListView,
  },
  {
    path: "/tours/:id",
    name: "tour-details",
    component: TourDetailsView,
  },
];
