<template>
  <div class="card">
    <div class="card-header">
      <h2>{{ relay.name }}</h2>
      <h3>{{ relay.display_name }}</h3>
    </div>
    <div class="card-container">
      <div class="buttons">
        <div class="relay-toggle-button">
          <ToggleButton :defaultState="relay.state" :isManual="isManual()" @relayState="relayCardState" />
        </div>
        <div class="relay-edit-button">
          <a :href="'grzybiarnia/edit/' + station_id + '/' + relay.index"> <i class="fas fa-edit"></i> Edit</a>
        </div>
      </div>
      <h4>
        <span>
          <i class="fas fa-info-circle"></i>
          <div class="tooltip">
            <p>id: {{ relay.index }}</p>
            <p>display_name: {{ relay.display_name }}</p>
            <p>state: {{ relay.state }}</p>
            <p>mode: {{ relay.mode }}</p>
            <p>t_on: {{ relay.t_on }}</p>
            <p>t_off: {{ relay.t_off }}</p>
            <p>interval: {{ relay.interval }}</p>
            <p>hysteresis: {{ relay.hysteresis }}</p>
            <p>set_value: {{ relay.set_value }}</p>
            <p>sensor_name: {{ relay.sensor_name }}</p>
          </div>
        </span>
      </h4>
    </div>
  </div>
</template>

<script>
import ToggleButton from "./ToggleButton";
export default {
  name: "CardRelay",
  components: {
    ToggleButton,
  },
  props: {
    relay: {
      required: true,
    },
    station_id: {
      type: Number,
      required: true,
    },
  },
  emits: ["cardState"],
  methods: {
    relayCardState(state) {
      this.toggleState = state;
      this.$emit("cardState", this.toggleState, this.relay.index);
    },
    isManual() {
      if (this.relay.mode == "MANUAL") {
        return true;
      } else return false;
    },
  },

  data() {
    return {
      toggleState: {
        type: Boolean,
        default: false,
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.card {
  display: grid;
  grid-template-columns: 1fr 1fr;

  margin-top: 0.5rem;
  border: 1px solid #c0c0c0;
  border-radius: 5px;
  text-align: left;

  .card-header {
    margin: 0.2rem;
    a {
      background: #6c757d;
      box-shadow: 3px 3px 3px rgba(51, 51, 51, 0.2);
      border: 1px solid #c0c0c0;
      border-radius: 4px;
      color: white;
      margin: auto;
      padding: 0.4rem;
    }
  }
  .card-container {
    display: grid;
    grid-template-columns: 1fr 0.4fr;
    .buttons {
      display: grid;
      grid-template-rows: 1fr 0.5fr;
      .relay-toggle-button {
        margin: auto;
        margin-top: 0.2rem;
      }
      .relay-edit-button {
        background: #adb5bd;
        width: 70px;
        height: 20px;
        border-radius: 5px;
        margin: auto;
        a {
          margin-left: 0.4rem;
          color: white;
          i {
            color: black;
          }
        }
      }
    }

    h2 {
      margin-top: 0.1rem;
    }
    h4 {
      text-align: right;
      margin-top: 5rem;
      margin-right: 0.2rem;
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
        left: 75%;
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
