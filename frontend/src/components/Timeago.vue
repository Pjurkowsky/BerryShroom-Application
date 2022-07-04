<template></template>

<script>
import VueTimeago from "vue-timeago";
export default {
  name: "Timeago",
  locale: "en-US",
  locales: {
    "en-US": [
      "just now",
      ["%s second ago", "%s seconds ago"],
      ["%s minute ago", "%s minutes ago"],
      ["%s hour ago", "%s hours ago"],
      ["%s day ago", "%s dni ago"],
      ["%s week ago", "%s mis ago"],
      ["%s month ago", "%s months ago"],
      ["%s year ago", "%s years ago"],
    ],
  },
};
</script>

<style></style>
