<template>
  <label class="switch">
    <input
      type="checkbox"
      id="tog_btn"
      v-model="checkedValue"
      @click="sendState()"
      :disabled="!isManual"
    />
    <div class="slider">
      <span v-if="isActive" class="on">ON</span>
      <span v-if="!isActive" class="off">OFF</span>
    </div>
  </label>
</template>

<script>
export default {
  props: {
    defaultState: {
      type: Boolean,
      default: false,
    },
    isManual: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    sendState() {
      this.$emit("relayState", !this.currentState);
    },
  },
  data() {
    return {
      currentState: this.defaultState,
    };
  },
  computed: {
    isActive() {
      return this.defaultState;
    },
    checkedValue: {
      get() {
        return this.currentState;
      },
      set(state) {
        this.currentState = state;
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.relay-toggle-button {
  margin: auto;
  margin-top: 0.2rem;
  .switch {
    position: relative;
    display: inline-block;
    width: 80px;
    height: 60px;
  }
  .switch input {
    display: none;
  }
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ca2222;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    border-radius: 5px;
    box-shadow: 0px 5px 5px rgba(51, 51, 51, 0.2);
  }
  .slider:before {
    position: absolute;
    content: "";
    height: 60px;
    width: 15px;
    border-radius: 5px;
    background-color: white;
    -webkit-transition: 0.4s;
    transition: 0.4s;
  }

  input:checked + .slider {
    background-color: #2ab934;
  }

  input:focus + .slider {
    box-shadow: 0 0 1px #2196f3;
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(65px);
    -ms-transform: translateX(65px);
    transform: translateX(65px);
  }

  .on,
  .off {
    color: white;
    position: absolute;
    transform: translate(-50%, -50%);
    top: 50%;
    left: 50%;
    font-size: 10px;
    font-family: Verdana, sans-serif;
  }

  input:checked + .slider .on {
    display: block;
  }

  input:checked + .slider .off {
    display: none;
  }
}
</style>