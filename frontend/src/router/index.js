import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Grzybiarnia from "../views/Grzybiarnia.vue";
import GrzybiarniaEdit from "../views/GrzybiarniaEdit.vue";
import SensorChart from "../views/SensorChart.vue";
import Sensors from "../views/Sensors.vue";
import Settings from "../views/Settings.vue";
import Logs from "../views/Logs.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/grzybiarnia",
    name: "Grzybiarnia",
    component: Grzybiarnia,
  },
  {
    path: "/grzybiarnia/edit/:station_id/:id",
    name: "GrzybiarniaEdit",
    component: GrzybiarniaEdit,
  },
  {
    path: "/sensor-chart/:station_id/:id",
    name: "SensorChart",
    component: SensorChart,
  },
  {
    path: "/sensors/:id",
    name: "Sensors",
    component: Sensors,
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
  },
  {
    path: "/logs",
    name: "Logs",
    component: Logs,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
