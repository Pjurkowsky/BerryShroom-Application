<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />

  <div class="side">
    <p>
      Select station <br />
      by index:
    </p>
    <select v-model="id" @change="getStation(id)">
      <option v-for="station in stations" :key="station.index">{{ station.index }}</option>
    </select>
  </div>

  <table class="center">
    <tr>
      <th>index</th>
      <th>name</th>
      <th>display_name</th>
      <th>delay_time</th>
      <th>show</th>
    </tr>
    <tr>
      <td>{{ statio.index }}</td>
      <td>{{ statio.name }}</td>
      <td v-if="!statio.edit">{{ statio.display_name }}</td>
      <td v-if="!statio.edit">{{ statio.delay_time }}</td>
      <td v-if="statio.edit"><input type="text" v-model="statio.display_name" /></td>
      <td v-if="statio.edit"><input type="text" v-model="statio.delay_time" /></td>
      <td><input type="checkbox" :disabled="!statio.edit" v-model="statio.show" /></td>
    </tr>
  </table>

  <table class="center">
    <tr>
      <th>index</th>
      <th>name</th>
      <th>display_name</th>
      <th>type</th>
      <th>show</th>
    </tr>
    <tr v-for="sensor in statio.sensors" :key="sensor.index" @click="deleteSensor(sensor.index)">
      <td>{{ sensor.index }}</td>

      <td v-if="!sensor.edit">{{ sensor.name }}</td>
      <td v-if="sensor.edit"><input type="text" v-model="sensor.name" /></td>
      <td v-if="!sensor.edit">{{ sensor.display_name }}</td>
      <td v-if="sensor.edit"><input type="text" v-model="sensor.display_name" /></td>
      <td v-if="!sensor.edit">{{ sensor.type }}</td>
      <td v-if="sensor.edit"><input type="text" v-model="sensor.type" /></td>
      <td><input type="checkbox" :disabled="!sensor.edit" v-model="sensor.show" /></td>
    </tr>
  </table>

  <div class="down">
    <a :href="'/sensors/' + id" v-if="edit || add" @click="edit ? sendData() : sendSensor()"><button>Send</button></a>
    <a :href="'/sensors/' + id" v-if="deleteS" @click="deleteData()"><button>Delete</button></a>
    <button class="add" v-if="!edit && !add && !deleteS" @click="addSensor()" :disabled="add">Add</button>
    <button class="delete" v-if="!add && !edit && !deleteS" @click="changeDelete()">Delete</button>
    <button class="edit" v-if="!add && !deleteS" @click="changeEdit()">Edit</button>
    <a :href="'/sensors/' + id" v-if="add || deleteS || edit">
      <button class="back"><i class="fas fa-arrow-left"></i></button>
    </a>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export default {
  name: "Sensors",
  components: { Sidebar, Topbar },
  methods: {
    getData() {
      fetch("http://192.168.8.184:8000/api/dashboard/")
        .then((response) => response.json())
        .then((data) => (this.stations = data))
        .then(() => (this.statio = this.stations[this.id]))
        .catch((err) => console.log(err));
    },
    getStation(index) {
      if (this.stations[this.id] != null) this.statio = this.stations[this.id];
    },
    changeEdit() {
      for (let i in this.statio.sensors) {
        this.statio.sensors[i].edit = !this.statio.sensors[i].edit;
      }
      this.statio.edit = !this.statio.edit;
      this.edit = !this.edit;
    },
    changeAdd() {
      this.add = false;
    },
    changeDelete() {
      this.deleteS = !this.deleteS;
      for (let i in this.statio.sensors) {
        this.statio.sensors[i].deleteS = true;
      }
    },
    sendData() {
      let updated_station = {
        index: this.statio.index,
        display_name: this.statio.display_name,
        delay_time: this.statio.delay_time,
        show: this.statio.show,
        sensors: [],
      };

      fetch("http://192.168.8.184:8000/api/station-update/" + this.statio.index + "/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updated_station),
      }).then((res) => {
        res.json();
      });

      for (let i in this.statio.sensors) {
        let updated_sensor = {
          index: this.statio.sensors[i].index,
          display_name: this.statio.sensors[i].display_name,
          type: this.statio.sensors[i].type,
          show: this.statio.sensors[i].show,
          values: [],
        };
        console.log(JSON.stringify(updated_sensor));
        fetch(
          "http://192.168.8.184:8000/api/sensor-update/" + this.statio.index + "/" + this.statio.sensors[i].index + "/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updated_sensor),
          }
        ).then((res) => {
          res.json();
        });
      }
    },
    sendSensor() {
      let last_sensor;
      for (let i in this.statio.sensors) last_sensor = this.statio.sensors[i];
      console.log(last_sensor);
      fetch("http://192.168.8.184:8000/api/sensor-create/" + this.statio.index + "/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(last_sensor),
      }).then((res) => {
        res.json();
      });
    },
    addSensor() {
      this.add = true;

      let biggestIndex;
      for (let i in this.statio.sensors) biggestIndex = this.statio.sensors[i].index + 1;
      let created_sensor = {
        index: biggestIndex,
        display_name: "placeholder",
        show: false,
        values: [],
      };
      this.statio.sensors[biggestIndex] = created_sensor;
      this.statio.sensors[biggestIndex].edit = true;
    },

    deleteSensor(sensorId) {
      if (event.target && this.statio.sensors[sensorId].deleteS && this.deleteS) {
        event.target.parentElement.style.borderStyle = "solid";
        event.target.parentElement.style.borderColor = "red";
        event.target.parentElement.style.borderWidth = "2px";
        this.toDelete.push(sensorId);
        this.statio.sensors[sensorId].deleteS = false;
      } else if (event.target && this.deleteS) {
        event.target.parentElement.style.borderStyle = null;
        event.target.parentElement.style.borderColor = null;
        event.target.parentElement.style.borderWidth = null;
        let index = this.toDelete.indexOf(sensorId);
        if (index > -1) this.toDelete.splice(index, 1);
        this.statio.sensors[sensorId].deleteS = true;
      }
    },
    deleteData() {
      for (let i in this.toDelete) {
        fetch("http://192.168.8.184:8000/api/sensor-delete/" + this.statio.index + "/" + this.toDelete[i] + "/", {
          method: "DELETE",
        });
      }
    },
  },
  mounted() {
    this.getData();
    this.getStation();
  },

  computed: {},
  data() {
    return {
      stations: Array,
      statio: Object,
      navOpen: false,
      id: this.$route.params.id,
      edit: false,
      add: false,
      deleteS: false,
      toDelete: [],
    };
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
.side {
  position: absolute;
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 0.5rem;
  margin-top: 1rem;
  left: 2.5%;
  font-size: 0.9em;
  background: #527fb3;
  border-radius: 5px;
  padding: 0.2rem;
  color: white;
  select {
    height: 40px;
    margin-top: 0.7rem;
    color: white;
    background: #29648a;
    border-radius: 5px;
    border-color: #29648a;
    option {
      border-color: #29648a;
    }
    option:focus,
    option:hover {
      outline: 0 !important;
    }
  }
  select:focus {
    border-color: #66afe9;
    outline: 0;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(102, 175, 233, 0.6);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(102, 175, 233, 0.6);
  }
}
.down {
  .edit {
    position: absolute;
    left: 77%;
    margin-top: 4rem;
  }
  .add {
    position: absolute;
    left: 77%;
  }
  .delete {
    position: absolute;
    left: 73%;
  }
  .back {
    position: absolute;
    left: 20%;
  }
}
button {
  margin-top: 1rem;

  width: 60px;
  height: 40px;
  background: #527fb3;
  border: none;
  color: white;
  text-align: center;
  cursor: pointer;
  border-radius: 5px;
  box-shadow: 2px 2px 2px rgba(51, 51, 51, 0.5);
  font-size: 0.9em;
  font-weight: bold;
}
</style>
