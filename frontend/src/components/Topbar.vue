<template>
  <div class="topbar">
    <a class="btn" @click="$emit('toggleSidebar')">
      <i class="fas fa-bars"></i>
    </a>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.topbar {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 12vh;
  box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
  background: #527fb3;

  .btn {
    top: 1rem;
    left: 1rem;
    position: fixed;
    width: 1.5rem;
    height: 1.5rem;
    padding: 0.5rem;
    z-index: 997;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgba(51, 51, 51, 0.2);
    background: #29648a;
    color: white;
    cursor: pointer;
    display: block;
    text-align: center;
    i {
      margin-top: 0.2rem;
    }
    &:hover {
      background: #235676;
    }
  }
}
</style>