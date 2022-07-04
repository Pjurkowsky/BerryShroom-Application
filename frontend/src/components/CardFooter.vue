<template>
  <div class="card-footer">
    <i
      class="fas fa-arrow-right"
      @click="$emit('toggleFooter', sensor.id, stationId)"
      v-if="!sensor.footer"
    />

    <div class="card-footer-outer-container" v-if="sensor.footer">
      <div class="card-footer-container">
        <p>min:</p>
        <div class="card-footer-inner-container">
          <i
            class="fas fa-thermometer-empty"
            v-if="sensor.type === 'temperature'"
          />
          <i class="fas fa-tint" v-else-if="sensor.type === 'humidity'" />
          <p>{{ sensor.min_value }}</p>
          <p v-if="sensor.type === 'temperature'">°C</p>
          <p v-else-if="sensor.type === 'humidity'">%</p>
        </div>
      </div>

      <div
        class="card-footer-container last-child"
        :data-tooltip="sensor.max_value_date"
      >
        <p>max:</p>
        <div class="card-footer-inner-container">
          <i
            class="fas fa-thermometer-empty"
            v-if="sensor.type === 'temperature'"
          />
          <i class="fas fa-tint" v-else-if="sensor.type === 'humidity'" />
          <p>{{ sensor.max_value }}</p>
          <p v-if="sensor.type === 'temperature'">°C</p>
          <p v-else-if="sensor.type === 'humidity'">%</p>
        </div>
      </div>
    </div>

    <i
      class="fas fa-arrow-left"
      @click="$emit('toggleFooter', sensor.id, stationId)"
      v-if="sensor.footer"
    />
  </div>
</template>

<script>
export default {
  emits: ["toggleFooter"],
};
</script>

<style lang="scss" scoped>
.card-footer {
  display: flex;
  width: 100%;
  height: 100%;
  padding-top: 0.3rem;
  font-size: 1rem;

  .fa-arrow-left {
    margin-left: auto;
    font-size: 1.5rem;
    padding-top: 0.5rem;
    cursor: pointer;
  }
  .fa-arrow-right {
    padding-top: 0.5rem;
    font-size: 1.5rem;

    cursor: pointer;
  }

  .card-footer-outer-container {
    display: flex;
    .last-child {
      padding-left: 0.5rem;
    }
    .card-footer-container {
      display: flex;
      position: relative;
      flex-direction: column;
      p {
        font-weight: bold;
        cursor: pointer;
      }
      i {
        cursor: pointer;
      }
      .card-footer-inner-container {
        display: flex;
        p {
          padding-left: 0.1rem;
        }
      }
    }
  }
}
</style>