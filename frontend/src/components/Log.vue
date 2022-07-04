<template>
  <td>{{ log.id }}</td>
  <td>{{ log.logger }}</td>
  <td>{{ log.message }}</td>
  <td>{{ logDate }}</td>
</template>

<script>
var options = {
  hour: "numeric",
  minute: "numeric",
  second: "numeric",
  year: "numeric",
  month: "2-digit",
  day: "numeric",
};
export default {
  name: "Log",
  props: {
    log: {
      required: true,
    },
  },
  computed: {
    logDate() {
      return this.log.datetime != null
        ? new Date(this.log.datetime).toLocaleDateString("pl-PL", options)
        : null;
    },
  },
};
</script>

<style>
</style>