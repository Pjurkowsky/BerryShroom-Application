import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Highcharts from "highcharts";
import Stock from "highcharts/modules/stock";
import HighchartsVue from "highcharts-vue";
import timeago from 'vue-timeago3'

const timeagoOptions = {

  }  

Stock(Highcharts);  


createApp(App).use(router).use(HighchartsVue).use(timeago, timeagoOptions).mount('#app')
