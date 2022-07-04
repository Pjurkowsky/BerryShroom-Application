<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />
  <h2>Settings of Relay {{ id }}</h2>
  <div class="container" v-if="station">
    <div class="names">
      <h3>Mode:</h3>
      <h3>T_ON:</h3>
      <h3>T_OFF:</h3>
      <h3>Interval:</h3>
      <h3>Hysteresis:</h3>
      <h3>Set_value:</h3>
      <h3>Sensor_name:</h3>
    </div>
    <div class="inputs">
      <div>
        <select v-model="station.relays[id].mode">
          <option>AUTO</option>
          <option>MANUAL</option>
          <option>SENSOR</option>
          <option>TIME_1</option>
          <option>TIME_2</option>
        </select>
      </div>
      <div>
        <input type="text" v-model="station.relays[id].t_on" />
      </div>
      <div>
        <input type="text" v-model="station.relays[id].t_off" />
      </div>
      <div>
        <input type="text" v-model="station.relays[id].interval" />
      </div>
      <div>
        <input type="text" v-model="station.relays[id].hysteresis" />
      </div>
      <div>
        <input type="text" v-model="station.relays[id].set_value" />
      </div>
      <div>
        <input type="text" v-model="station.relays[id].sensor_id" />
      </div>
    </div>
  </div>
  <a href="/grzybiarnia">
    <button @click="sendData()">Send</button>
  </a>
</template>

<script>
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
export default {
  name: "GrzybiarniaEdit",
  components: { Sidebar, Topbar },
  methods: {
    getData() {
      fetch("http://192.168.8.184:8000/api-mushfarm/mushstation/" + this.station_id)
        .then((response) => response.json())
        .then((data) => (this.station = data))
        .catch((err) => console.log(err));
    },
    sendData() {
      for (let i in this.station.relays) {
        delete this.station.relays[i]["id"];
      }

      fetch("http://192.168.8.184:8000/api-mushfarm/relay-update/" + this.station_id + "/" + this.id + "/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.station.relays[this.id]),
      }).then((res) => {
        res.json();
      });
    },
  },
  data() {
    return {
      station: Object,
      navOpen: false,
      station_id: this.$route.params.station_id,
      id: this.$route.params.id,
    };
  },
  created() {
    this.getData();
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
h2 {
  margin-top: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}
.container {
  display: grid;
  margin: auto;
  width: 20%;
  grid-template-columns: repeat(2, minmax(100px, 1fr));
}
h3 {
  padding: 12px 20px;
  margin-top: 0.73rem;
  text-align: right;
}
select {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
}
button {
  width: 60px;
  height: 40px;
}
</style>
