<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />
  <a href="/"
    ><button><i class="fas fa-arrow-left"></i></button
  ></a>
  <div class="container">
    <h2>{{ station.sensors[id].name }}</h2>

    <Chart
      :sensor="station.sensors[id]"
      :s_id="parseInt(station_id)"
      :settings="c_settings"
    />
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import Chart from "../components/Chart";
export default {
  components: { Sidebar, Topbar, Chart },

  methods: {
    getData() {
      fetch("http://192.168.8.184:8000/api/station/" + this.station_id)
        .then((response) => response.json())
        .then((data) => (this.station = data))
        .catch((err) => console.log(err));
    },
    getSettingsData() {
      fetch("http://192.168.8.184:8000/api-settings/settings/")
        .then((response) => response.json())
        .then((data) => (this.settings = data))
        .catch((err) => console.log(err));
    },
  },
  computed: {
    c_settings() {
      for (let i in this.settings) {
        let sensor_group = JSON.parse(this.settings[i]["list_of_indexes"]);
        for (let n in sensor_group)
          if (
            this.s_id == sensor_group[n].station_index &&
            this.station.sensors[id].index == sensor_group[n].sensor_index
          ) {
            return settings[i].chart_settings;

          }
      }
    },
  },
  data() {
    return {
      station: Object,
      navOpen: false,
      id: this.$route.params.id,
      station_id: this.$route.params.station_id,
      settings: Object,
    };
  },
  created() {
    this.getData();
    this.getSettingsData();
  },
};
</script>

<style lang="scss" scoped>
.container {
  margin-top: 2rem;
}
a {
  text-decoration: none;
  button {
    margin-top: 1rem;
    position: absolute;
    left: 10rem;
    width: 60px;
    height: 40px;
    background: #527fb3;
    border: none;
    color: white;
    text-align: center;
    cursor: pointer;
    border-radius: 5px;
    box-shadow: 2px 2px 2px rgba(51, 51, 51, 0.5);
    font-size: 18px;
  }
}
</style>
