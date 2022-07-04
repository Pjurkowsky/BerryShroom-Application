<template>
  <div class="chart">
    <highcharts
      :constructorType="'stockChart'"
      class="hc"
      :options="chartOptions"
      ref="chart"
    ></highcharts>
  </div>
</template>

<script>
export default {
  props: {
    sensor: Object,
    s_id: Number,
  },
  methods: {
    getData() {
      fetch("http://192.168.8.184:8000/api-settings/settings/")
        .then((response) => response.json())
        .then((data) => (this.settings = data))
        .then(() => {
          for (let i in this.settings) {
            let sensor_group = JSON.parse(this.settings[i]["list_of_indexes"]);
            for (let n in sensor_group)
              if (
                this.s_id == sensor_group[n].station_index &&
                this.sensor.index == sensor_group[n].sensor_index
              ) {
                console.log(this.settings[i].chart_settings);
                // this.chartOptions.yAxis.max = this.settings[i].chart_settings.max_error_value;
                //    this.chartOptions.yAxis.min = this.settings[i].chart_settings.min_error_value;
                
                this.chartOptions.plotOptions.series.color = this.settings[i].chart_settings.chart_color;
                
              
                break;
              }
          }
            let list = this.formatData();
                this.chartOptions.series[0].data = list;
        })
        .catch((err) => console.log(err));
    },
    formatData() {
     var list = new Array();
      for (let i in this.sensor.values) {
        let date = new Date(this.sensor.values[i]["date_created"]).getTime();
        list[i] = [date, this.sensor.values[i]["value"]];
      }
     return list;
     
    },
  },
  mounted() {
    this.getData();

  },
  data() {
    return {
      settings: Object,

      chartOptions: {
        chart: {
          type: "spline",
          events: {},
        },
        rangeSelector: {
          buttons: [
            {
              type: "hour",
              count: 1,
              text: "1H",
            },
            {
              type: "hour",
              count: 6,
              text: "6H",
            },
            {
              type: "day",
              count: 1,
              text: "1D",
            },
            {
              type: "all",
              count: 1,
              text: "All",
            },
          ],
          selected: 4,
          inputEnabled: false,
        },
        navigator: {
          enabled: false,
        },
        scrollbar: {
          enabled: false,
        },
        title: {
          text: "",
        },
        xAxis: {
          type: "datetime",
        },
        tooltip: {
          xDateFormat: "%Y-%m-%d %H:%M:%S",
        },
        yAxis: {
          title: {
            text: this.sensor.type,
          },
          opposite: false,
        },
        plotOptions: {
          series: {
            
          },
          spline: {
            dataLabels: {
              enabled: false,
            },
            enableMouseTracking: true,
          },
        },
        credits: {
          enabled: false,
        },
        series: [
          {
            name: this.sensor.type,
            dataGrouping: {
              enabled: false,
            },
          },
        ],
        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                "printChart",
                "downloadPNG",
                "downloadJPEG",
                "downloadPDF",
                "downloadSVG",
              ],
            },
          },
        },
      },
    };
  },
};
</script>

<style lang="scss" scoped>
.chart {
  margin: auto;
  width: 60%;
}
</style>