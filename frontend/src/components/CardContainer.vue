<template>
  <div v-if="which_parent == 'Home'">
    <div class="station" v-if="visibilityOfStation">
      <h2>{{ station.display_name }}</h2>
      <p class="text-muted">Ostatni odczyt: <timeago :datetime="time" /></p>
      <div class="card-container">
        <Card v-for="sensor in station.sensors" :key="sensor.index" :sensor="sensor" :station_id="station.index" />
      </div>
    </div>
  </div>
  <div v-else-if="which_parent == 'Grzybiarnia'">
    <div class="station">
      <h2>{{ station.name }}</h2>
      <p class="text-muted">Ostatni odczyt: wczoraj</p>
      <div class="card-container">
        <CardRelay
          v-for="relay in station.relays"
          v-bind:key="relay"
          :relay="relay"
          :station_id="station.index"
          @cardState="changeState"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "./Card";
import CardRelay from "./CardRelay";

export default {
  name: "CardContainer",
  components: { Card, CardRelay },
  emits: [],
  props: {
    station: {
      required: true,
    },

    which_parent: String,
  },
  methods: {
    changeState(state, id) {
      let updated_station = {
        index: id,
        state: state,
      };
      this.station.relays[id].state = state;
      fetch("http://192.168.8.184:8000/api-mushfarm/relay-update/" + this.station.index + "/" + id + "/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updated_station),
      }).then((res) => {
        res.json();
      });
    },
  },
  computed: {
    time() {
      return Date.parse(this.station["date_created"]);
    },
    visibilityOfStation() {
      let show = false;
      for (let i in this.station.sensors) {
        if (this.station.sensors[i].show) {
          if (this.station.sensors[i].value != null) {
            // this.station.sensors[i].values.length > 0)  tak bylo gdy uzywalem fetcha do station a nie do dashboard
            show = true;
          }
        }
      }
      return show;
    },
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.station {
  margin-top: 1rem;
  text-align: center;
  p {
    margin-top: 0.2rem;
    font-size: 15px;
    min-width: 160px;
  }
  h2 {
    text-align: center;
    min-width: 160px;
  }
  .card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    grid-template-rows: 0.75fr;
    column-gap: 30px;
    row-gap: 30px;
    min-width: 250px;
    min-height: 130px;
    margin: auto;
  }
}
</style>
