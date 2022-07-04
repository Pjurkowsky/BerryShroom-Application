<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />

    <table class="center">
      <tr>
        <th>index</th>
        <th>logger</th>
        <th>message</th>
        <th>date</th>
      </tr>
      <tr v-for="log in logArray" v-bind:key="log">
        <Log :log="log"/>
      </tr>
    </table>



</template>

<script>
import Topbar from "../components/Topbar";
import Sidebar from "../components/Sidebar";
import Log from "../components/Log";
export default {
  name: "Logs",
  components: { Sidebar, Topbar, Log },
  methods: {
    updateData() {
      fetch("http://192.168.8.184:8000/api-log/")
        .then((response) => response.json())
        .then((data) => (this.logArray = data))
        .catch((err) => console.log(err));
    },
  },

  data() {
    return {
      navOpen: false,
      logArray: [],
    };
  },
  mounted() {
    this.updateData();
    setInterval(this.updateData, 10000);
  },
};
</script>

<style lang="scss" scoped>
table {
  border-collapse: collapse;
  font-size: 0.9em;
  min-width: 100px;
  tr {
    text-align: left;
    th {
      background-color: #527fb3;
      color: white;
      font-weight: bold;
    }
    th:first-of-type {
      width: 50px;
    }
    th:nth-of-type(2) {
      width: 200px;
    }
    th:nth-of-type(3) {
      width: 200px;
    }
    th:nth-of-type(4) {
      width: 200px;
    }
    th:nth-of-type(5) {
      width: 50px;
    }
    td {
      border-bottom: 1px solid #ddd;
    }
    th,
    td {
      padding: 2px 4px;
    }
  }
  tr:nth-of-type(even) {
    background: #f3f3f3;
  }
  tr:last-of-type {
    border-bottom: 2px solid #ddd;
  }
  input[type="text"] {
    border: none;
    appearance: none;
    background: #dbdbdb;
    width: 150px;
    border-radius: 3px;
    outline: none;
    transition: ease-in-out, width 0.35s ease-in-out;
  }
  input[type="text"]:focus {
    width: 190px;
  }
}
.center {
  margin: auto;
  margin-top: 1rem;
  width: 60%;
}

</style>
