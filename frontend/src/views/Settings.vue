<template>
  <Sidebar :open="navOpen" @toggleSidebar="navOpen = !navOpen" />
  <Topbar @toggleSidebar="navOpen = !navOpen" />
  <transition name="fade">
    <div class="notification good" v-if="good_noti_visible">Saved</div>
  </transition>
  <transition name="fade">
    <div class="notification bad" v-if="bad_noti_visible">Error</div>
  </transition>
  <h1>Settings</h1>
  <div class="container">
    <div class="charts-settings">
      <h2>Group Settings</h2>
      <div class="form-container">
        <div>
          Select Group:
          <select v-model="group_name" @change="groupChange(group_name)">
            <option v-for="tgroup in groups" :key="tgroup.index">{{
              tgroup.name
            }}</option>
          </select>
        </div>
        <div class="form">
          <!-- <label>Max acceptable value:</label>
          <input
            type="text"
            v-model="group.chart_settings.max_error_value"
            @value="group.chart_settings.max_error_value"
            @change="sendData()"
          />
          <label>Min acceptable value:</label>
          <input
            type="text"
            v-model="group.chart_settings.min_error_value"
            @value="group.chart_settings.min_error_value"
            @change="sendData()"
          /> -->
          <label>Color in hex:</label>
          <input
            type="text"
            v-model="group.chart_settings.chart_color"
            @value="group.chart_settings.chart_color"
            @change="sendData()"
          />
          <label>Show values from last: </label>
          <input
            type="text"
            v-model="group.dashboard_settings.time_last"
            @value="group.dashboard_settings.time_last"
            @change="sendData()"
          />
          <label>Delete or Add group: </label>
          <input type="text" v-model="new_group_name" />
          <div class="btn-container">
            <div class="delete-btn btn" @click="deleteGroup()">
              <i class="fas fa-minus"></i>
            </div>
            <div class="add-btn btn" @click="createGroup()">
              <i class="fas fa-plus"></i>
            </div>
          </div>
        </div>
        <table>
          <tr>
            <th>Station index</th>
            <th>Sensor index</th>
            <th>Sensor name</th>
            <th></th>
          </tr>
          <tr v-for="sensor in current_list_of_sensors">
            <td>{{ sensor.station_index }}</td>
            <td>{{ sensor.sensor_index }}</td>
            <td>{{ sensor.sensor_name }}</td>
            <div class="delete-btn btn"><i class="fas fa-minus"></i></div>
          </tr>
        </table>
      </div>
    </div>

    <div class="dashboard-settings">
      <h2>Sensor settings</h2>
      <div class="form-container">
        <div>
          Select Sensor:
          <select v-model="current_sensor">
       
            <option v-for="sensor in list_of_sensors" :value="sensor">{{
              sensor.sensor_name
            }}</option>
          </select>
        </div>
        <div class="form">
          <div>
            Add sensor to group:
            <select>
              <option v-for="tgroup in groups" :key="tgroup.index">{{
                tgroup.name
              }}</option>
            </select>
          </div>
          <div class="add-btn btn" @click="addSensorToGroup()">
            <i class="fas fa-plus"></i>
          </div>
        </div>
      </div>
    </div>
    <div class="station-settings">
    <h2>Station Settings</h2>
     <div class="form-container">
        <div>
          Select Station
          <select v-model="current_station">
            <option v-for="station in stations" :value="station" >{{
              station.name
            }}</option>
          </select>

        </div>
        <div class="form">
                   <label>Delay time:</label>
          <input
            type="text"
            v-model="current_station.delay_time"
            @value="current_station.delay_time"
            @change="sendData()"
          />
                      <div class="add-btn btn" @click="sendDelayTime()">
              <i class="fas fa-plus"></i>
            </div>
          </div>
     </div>
    </div>
  </div>
</template>

<script>
import Topbar from "../components/Topbar";
import Sidebar from "../components/Sidebar";

export default {
  name: "Settings",
  components: { Sidebar, Topbar },
  methods: {
    getStatinoData() {
      fetch("http://192.168.8.184:8000/api/dashboard/")
        .then((response) => response.json())
        .then((data) => {
       
          this.stations = data;
             console.log(this.stations);
          this.list_of_sensors = [];
          this.list_of_indexes = [];
          this.current_station = this.stations[0];
 
          for (let i in this.stations) {
            for (let j in this.stations[i].sensors) {
              this.list_of_sensors.push({
                station_index: this.stations[i].index,
                sensor_index: this.stations[i].sensors[j].index,
                sensor_name: this.stations[i].sensors[j].name,
              });
              
            }
          }
          this.current_sensor = this.list_of_sensors[0];
         
        })
        .catch((err) => console.log(err));
    },
    getData() {
      fetch("http://192.168.8.184:8000/api-settings/settings/")
        .then((response) => response.json())
        .then((data) => (this.groups = data))
        .then(() => {
          this.group = this.groups[this.current_group];
          this.group_name = this.group.name;
          this.current_list_of_sensors = JSON.parse(this.group.list_of_indexes);
        })
        .catch((err) => console.log(err));
    },
    groupChange(name) {
      for (let i in this.groups) {
        if (this.groups[i].name == name) {
          this.group = this.groups[i];
          this.current_group = i;
        }
      }
      console.log(this.group.list_of_indexes);
      this.current_list_of_sensors = JSON.parse(this.group.list_of_indexes);
    },
    createGroup() {
      let new_group = {
        name: this.new_group_name,
        list_of_indexes: "[]",
        chart_settings: {},
        dashboard_settings: {},
      };

      fetch("http://192.168.8.184:8000/api-settings/settings/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(new_group),
      }).then((res) => {
        res.json();
        if (res.status == 201) {
          this.good_noti_visible = true;

          this.new_group_name = "";
          setTimeout(() => (this.good_noti_visible = false), 1000);
        } else if (res.status == 400) {
          this.bad_noti_visible = true;
          setTimeout(() => (this.bad_noti_visible = false), 1000);
        }
        this.getData();
      });
    },
    deleteGroup() {
      fetch(
        "http://192.168.8.184:8000/api-settings/settings/" +
          this.new_group_name +
          "/",
        {
          method: "DELETE",
        }
      ).then((res) => {
        console.log(res);
        if (res.status == 204) {
          this.good_noti_visible = true;

          this.new_group_name = "";
          setTimeout(() => (this.good_noti_visible = false), 1000);
        } else if (res.status == 400) {
          this.bad_noti_visible = true;
          setTimeout(() => (this.bad_noti_visible = false), 1000);
        }
        this.getData();
      });
    },
    sendData() {
      fetch(
        "http://192.168.8.184:8000/api-settings/settings/" +
          this.group.id +
          "/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.group),
        }
      ).then((res) => {
        res.json();
        console.log(res.headers);
        if (res.status == 201) {
          this.good_noti_visible = true;
          setTimeout(() => (this.good_noti_visible = false), 1000);
        } else if (res.status == 400) {
          this.bad_noti_visible = true;
          setTimeout(() => (this.bad_noti_visible = false), 1000);
        }
        this.getData();
      });
    },
    addSensorToGroup() {
      this.group.list_of_indexes = JSON.parse(this.group.list_of_indexes);
      this.group.list_of_indexes.push(this.current_sensor);
      this.group.list_of_indexes = JSON.stringify(this.group.list_of_indexes);
      this.sendData();
    },
    sendDelayTime() {
      let station = {
        index: this.current_station.index,
        delay_time: this.current_station.delay_time,
        sensors: []
      }
  fetch("http://192.168.8.184:8000/api/station-update/" + station.index + '/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(station),
      }).then((res) => {
        res.json();
        if (res.status == 201) {
          this.good_noti_visible = true;

        
          setTimeout(() => (this.good_noti_visible = false), 1000);
        } else if (res.status == 400) {
          this.bad_noti_visible = true;
          setTimeout(() => (this.bad_noti_visible = false), 1000);
        }
        this.getData();
      });

    }
  },
  created() {
    this.getData();
    this.getStatinoData();
  },
  data() {
    return {
      navOpen: false,
      stations: Array,
      groups: Array,
      current_group: 0,
      group: {
        id: null,
        dashboard_settings: {
          id: null,
          time_last: null,
        },
        chart_settings: {
          id: null,
          chart_color: null,
          min_error_value: null,
          max_error_value: null,
        },
        name: null,
        list_of_indexes: [],
      },
      good_noti_visible: false,
      bad_noti_visible: false,
      group_name: "",
      new_group_name: null,
      list_of_sensors: Array,
      current_list_of_sensors: null,
      current_sensor: 0,
      current_station: 0,
    };
  },
};
</script>

<style lang="scss" scoped>
.notification {
  position: fixed;
  top: 1rem;
  left: 0;
  right: 0;
  margin: auto;
  max-width: 10rem;
  padding: 1rem;

  color: white;

  font-size: 16px;
  font-weight: bold;

  border-radius: 9px;

  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
.bad {
  background: #d9534f;
  border: 1px solid #d64945;
}
.good {
  border: 1px solid #24964c;
  background: #28a745;
}
.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: opacity 0.2s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  margin: auto;
  margin-top: 1rem;
  width: 74%;
  text-align: left;
  .charts-settings {
    display: grid;
    grid-template-columns: 1fr;
  }
  .form-container {
    margin-top: 2rem;
    width: 60%;
    font-size: 16px;
    font-weight: bold;
    text-align: left;
    table {
      border-collapse: collapse;
      font-size: 0.9em;
      min-width: 100px;
      margin-top: 1rem;
      tr {
        text-align: left;
        th {
          background-color: #527fb3;
          color: white;
          font-weight: bold;
        }
        th:first-of-type {
          width: 100px;
        }
        th:nth-of-type(2) {
          width: 100px;
        }
        th:nth-of-type(3) {
          width: 100px;
        }
        th:nth-of-type(4) {
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
    .btn-container {
      display: grid;
      grid-template-columns: 1fr 0.1fr;
      grid-template-rows: 1fr;
    }
    .btn {
      color: white;
      margin-top: 0.15rem;
      display: inline-block;
      i {
        padding: 0.1rem;
        border-radius: 5px;
        box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
      }
      :hover {
        cursor: pointer;
      }
    }
    .add-btn {
      margin-left: auto;
      i {
        background: #28a745;
        border: 1px solid #24964c;
      }
    }
    .delete-btn {
      margin-left: auto;
      i {
        background: #d9534f;
        border: 1px solid #d64945;
      }
    }
    .form {
      margin-top: 0.5rem;
      display: grid;
      grid-template-columns: 1fr;

      label {
        margin-top: 0.5rem;
      }
      input {
        outline: none;
        border-radius: 5px;
        border: 1px solid #ccc;
      }
    }
    select {
      border-radius: 5px;
    }
  }
}
</style>
