<template>
  <div class="card" v-show="sensor.show" v-if="isThereValue()">
    <div class="card-header">
      <h2>{{ sensor.display_name }}</h2>
      <a :href="'/sensor-chart/' + station_id + '/' + sensor.index"><i class="fas fa-chart-line"/></a>
    </div>
    <div class="card-container">
      <h2>
        <i class="fas fa-thermometer-three-quarters" v-if="sensor.type === 'temperature'" />
        <i class="fas fa-tint" v-else-if="sensor.type === 'humidity'" />
        {{ lastValue }}
        <span v-if="sensor.type === 'temperature'">°C</span>
        <span v-else-if="sensor.type === 'humidity'">%</span>
      </h2>
      <h4>
        <span>
          <i class="fas fa-info-circle"></i>
          <div class="tooltip">
            <p>id: {{ sensor.index }}</p>
            <p>display_name: {{ sensor.display_name }}</p>
            <p>name: {{ sensor.name }}</p>
            <p>value: {{ lastValue }}</p>
            <p>type: {{ sensor.type }}</p>
            <p>min_value: {{ minValue }}</p>
            <p>max_value: {{ maxValue }}</p>
            <p>value_date: {{ lastValueDate }}</p>
            <p>min_value_date: {{ minValueDate }}</p>
            <p>max_value_date: {{ maxValueDate }}</p>
          </div>
        </span>
      </h4>
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    sensor: {
      required: true,
    },
    station_id: {
      type: Number,
      required: true,
    },
  },
  methods: {
    isThereValue() {
      return this.sensor.values.length;
    },
  },
  computed: {
    lastValue() {
      return this.sensor.values[0]["value"].toFixed(2);
    },
    lastValueDate() {
      var options = {
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        year: "numeric",
        month: "2-digit",
        day: "numeric",
      };
      return new Date(this.sensor.values[0]["date_created"]).toLocaleDateString("pl-PL", options);
    },
    minValue() {
      let smallestValue = this.sensor.values[0]["value"];
      for (let i in this.sensor.values) {
        if (smallestValue > this.sensor.values[i]["value"]) smallestValue = this.sensor.values[i]["value"];
      }
      return smallestValue.toFixed(2);
    },
    minValueDate() {
      var options = {
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        year: "numeric",
        month: "2-digit",
        day: "numeric",
      };
      let smallestValue = this.sensor.values[0]["value"];
      let idOfSmallestValue;
      for (let i in this.sensor.values) {
        if (smallestValue > this.sensor.values[i]["value"]) {
          smallestValue = this.sensor.values[i]["value"];
          idOfSmallestValue = i;
        } else if (this.sensor.values[0]["value"] == smallestValue) idOfSmallestValue = 0;
      }
      return new Date(this.sensor.values[idOfSmallestValue]["date_created"]).toLocaleDateString("pl-PL", options);
    },
    maxValue() {
      let biggestValue = this.sensor.values[0]["value"];
      for (let i in this.sensor.values) {
        if (biggestValue < this.sensor.values[i]["value"]) biggestValue = this.sensor.values[i]["value"];
      }
      return biggestValue.toFixed(2);
    },
    maxValueDate() {
      let biggestValue = this.sensor.values[0]["value"];
      let idOfBiggestValue;
      var options = {
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        year: "numeric",
        month: "2-digit",
        day: "numeric",
      };
      for (let i in this.sensor.values) {
        if (biggestValue < this.sensor.values[i]["value"]) {
          biggestValue = this.sensor.values[i]["value"];
          idOfBiggestValue = i;
        } else if (this.sensor.values[0]["value"] == biggestValue) idOfBiggestValue = 0;
      }
      return new Date(this.sensor.values[idOfBiggestValue]["date_created"]).toLocaleDateString("pl-PL", options);
    },
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.card {
  display: grid;
  grid-template-rows: 0.2fr;
  margin-top: 0.5rem;
  border: 1px solid #c0c0c0;
  border-radius: 5px;
  text-align: left;
  max-width: 20rem;

  .card-header {
    display: grid;
    grid-template-columns: 1fr 0.15fr;
    margin: 0.2rem;
    a {
      background: #6c757d;
      box-shadow: 3px 3px 3px rgba(51, 51, 51, 0.2);
      border: 1px solid #c0c0c0;
      border-radius: 4px;
      color: white;
      margin: auto;
      padding: 0.4rem;
      margin-right: 0;
    }
  }
  .card-container {
    margin-left: 0.2rem;
    h2 {
      margin-top: 0.1rem;
    }
    h4 {
      text-align: right;
      margin-right: 0.3rem;
      i {
        z-index: 1;
      }
      i::before {
        cursor: pointer;
        z-index: 1;
      }
      .tooltip {
        position: absolute;
        background: black;
        color: white;
        border: 1px solid;
        border-radius: 4px;
        top: 25px;
        left: -85px;
        width: max-content;
        padding: 7px;
        font-size: 10px;
        visibility: hidden;
        text-align: left;
        z-index: 2;
      }
      @include phone {
        .tooltip {
          left: -80px;
        }
      }
      .tooltip::before {
        position: absolute;
        content: "";
        height: 15px;
        width: 15px;
        background: black;
        top: -7px;
        left: 50%;
        transform: translateX(-50%) rotate(45deg);
      }
      span {
        position: relative;
      }
      span:hover {
        .tooltip {
          visibility: visible;
        }
      }
    }
  }
}
</style>
