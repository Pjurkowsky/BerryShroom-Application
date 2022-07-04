<template>
  <transition name="fade">
    <div class="sidebar" v-if="open">
      <i class="fas fa-arrow-left" @click="$emit('toggleSidebar')"></i>
      <h2><a href="/">Weather Station</a></h2>
      <ul class="sidebar-nav">
        <a href="/">
          <li class="sidebar-item"><i class="fas fa-home"></i>Dashboard</li>
        </a>
        <a href="/grzybiarnia">
          <li class="sidebar-item"><i class="fas fa-warehouse"></i>Relays</li>
        </a>
        <a href="/sensors/0">
          <li class="sidebar-item"><i class="fas fa-user"></i>Sensors</li>
        </a>
        <a href="/logs">
          <li class="sidebar-item"><i class="fas fa-file-alt"></i>Logs</li>
        </a>
        <a href="/settings">
          <li class="sidebar-item"><i class="fas fa-cog"></i>Settings</li>
        </a>
      </ul>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Sidebar",
  props: ["open"],
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  background: #333;
  position: fixed;
  z-index: 999;
  width: 15rem;
  height: 100%;
  box-shadow: 3px 3px 3px rgba(51, 51, 51, 0.5);
  h2 {
    text-align: center;
    border-bottom: 1px solid #444;
    padding-top: 0.7;
    padding-bottom: 2rem;
    a {
      color: #527fb3;
      text-decoration: none;
      &:hover {
        color: #29648a;
      }
    }
  }
  .fa-arrow-left {
    font-size: 17px;
    text-align: center;

    margin-top: 1rem;
    margin-left: 12.9rem;

    background: #444;
    color: white;
    padding: 0.4rem;
    cursor: pointer;
    border-radius: 5px;
    &:hover {
      background: #5e5e5e;
    }
  }
  .sidebar-nav {
    padding: 0;
    margin: 0;
    a {
      color: white;
      text-decoration: none;

      i {
        padding-right: 0.4rem;
        text-align: center;
        width: 30px;
      }
    }

    .sidebar-item {
      left: 0;
      padding-top: 0.5rem;
      padding-bottom: 0.5rem;
      padding-left: 1rem;
      text-align: left;
      list-style: none;

      transition: 0.5s;
      opacity: 0.7;
      &:hover {
        opacity: 1;
        background: #5e5e5e;
        border-radius: 5px;
      }

      &:last-child {
        padding-bottom: 1rem;
        border-bottom: 1px solid #444;
      }
    }
  }
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-60px);
}
.fade-enter-active,
.fade-leave-active {
  transition: all 500ms;
}
</style>
