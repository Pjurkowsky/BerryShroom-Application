<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />
  <div class="container">
    <CardContainer
      v-for="station in station_array"
      v-bind:key="station"
      :station="station"
      which_parent="Grzybiarnia"
    />
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar";
import CardContainer from "../components/CardContainer";
import Topbar from "../components/Topbar";
export default {
  name: "Grzybiarnia",
  components: { CardContainer, Sidebar, Topbar },
  props: {},
  methods: {
    updateData() {
      fetch("http://192.168.8.184:8000/api-mushfarm/mushstation/")
        .then((response) => response.json())
        .then((data) => (this.station_array = data))
        .catch((err) => console.log(err));
    },
  },
  data() {
    return {
      navOpen: false,
      station_array: [],
    };
  },
  mounted() {
    this.updateData();
    setInterval(this.updateData, 10000);
  },
};
</script>

<style lang="scss" scoped>
.container {
  padding: 0;
  margin: 0px 20rem;
}
</style>
