let STYLE_SPARK_BASE = {
  chart: {
    backgroundColor: null,
    borderWidth: 0,
    margin: [2, 0, 2, 0],
    width: 120,
    height: 30,
    style: {overflow: 'visible'},
    skipClone: true
  },
  title: {text: ''},
  credits: {enabled: false},
  xAxis: {
    crosshair: true,
    labels: {enabled: false},
    title: {text: null},
    startOnTick: false,
    endOnTick: false,
    tickPositions: [],
    lineWidth: 0
  },
  yAxis: {
    endOnTick: false,
    startOnTick: false,
    labels: {enabled: false},
    title: {text: null},
    lineWidth: 0,
    tickPositioner: function () {
      return range(this.dataMin, this.dataMax + 1, (this.dataMax - this.dataMin) / 2);
    }
  },
  legend: {enabled: false},
  navigator: {enabled: false},
  scrollbar: {enabled: false},
  rangeSelector: {enabled: false},
  tooltip: {
    backgroundColor: "white",
    outside: true,
    hideDelay: 0,
    style: {
      padding: 0
    },
    formatter: function () {
      return this.points.map(function (point) {
        return '<span style="color:' + point.series.color + '">●</span><b>' + padT(point.y) + '</b>';
      });
    }
  },
  plotOptions: {
    dataGrouping: {enabled: false},
    series: {
      dataGrouping: {enabled: false},
      animation: false,
      lineWidth: 1,
      shadow: false,
      states: {
        hover: {
          halo: {size: 0},
          lineWidth: 1
        }
      },
      marker: {
        enabled: false,
        symbol: 'circle',
        radius: 2,
        states: {
          hover: {
            fillColor: null,
            lineColor: 'rgb(100, 100, 100)',
            lineWidth: 1
          }
        }
      }
    }
  }
};

let STYLE_SPARK_SPLINE = merge(STYLE_SPARK_BASE, {
  chart: {
    type: "spline"
  }
});

let STYLE_SPARK_SCATTER = merge(STYLE_SPARK_BASE, {
  chart: {
    type: "scatter"
  }
});

/**
 * Holds general configuration about HighChart charts.
 */
let STYLE_BASE = {
  chart: {
    spacing: 100,
    margin: 100,
    padding: 100
  },
  title: {text: ""},
  credits: {text: ""},
  xAxis: [{
    minorTickInterval: 'auto',
    startOnTick: true,
    endOnTick: true,
    showEmpty: false,
    lineWidth: 1,
    lineColor: "#333",
    labels: {
      rotation: -45,
      x: 15,
      formatter: function () {
        return time(this.value, "%d.%m.%Y<br>%H:%M:%S.%f");
      }
    }
  }, {
    visible: false,
    labels: {
      formatter: function () {
        return false;
      }
    }
  }],
  yAxis: {
    minorTickInterval: 'auto',
    startOnTick: true,
    endOnTick: true,
    lineWidth: 1,
    lineColor: "#333",
    opposite: false
  },
  plotOptions: {series: {marker: {enabled: false, radius: 4}}},
  legend: {
    enabled: true,
    y: 60,
    align: 'right',
    layout: 'vertical',
    verticalAlign: 'top'
  },
  navigator: {
    enabled: true,
    margin: 5,
    height: 35,
    outlineWidth: 0,
    outlineColor: 'transparent',
    xAxis: {labels: {enabled: false}},
    yAxis: {lineWidth: 0},
    handles: {
      height: 20,
      width: 8,
      backgroundColor: 'white',
      borderColor: 'black'
    }
  },
  tooltip: {
    shared: true,
    split: true,
    outside: true,
    backgroundColor: 'white',
    positioner: function (width, height, point) {
      let point_pos = point.plotX + this.chart.plotLeft - width / 2;
      let max_right = this.chart.chartWidth - width / 2 - this.chart.marginRight;

      if (point.isHeader) {
        return {
          x: Math.max(0, Math.min(point_pos, max_right)),
          y: this.chart.chartHeight
        };
      } else {
        return {
          x: Math.max(0, Math.min(point_pos, max_right)),
          y: 0
        };
      }
    },
    formatter: function () {
      return [time(this.x, "<b>%d.%m.%Y</b><br><b>%H:%M:%S.%f</b>")].concat(
        this.points.map(function (point) {
          let val = padT(dec(point.y));

          if (point.series.xAxis.visible) {
            return '<span style="color:' + point.series.color + '">●</span> <b>' + val + '</b>';
          } else {
            let percentile = v_index(Math.floor((point.key + 1) / point.series.points.length * 100)) + ' percentile'
            return '<span style="color:' + point.series.color + '">●</span> ' + percentile + '<b>' + val + '</b>';
          }
        })
      );
    }
  },
  rangeSelector: {
    enabled: true,
    verticalAlign: 'top',
    inputDateFormat: '%d.%m %H:%M',
    inputEditDateFormat: '%d.%m %H:%M',
    inputPosition: {align: 'left', y: -32, x: 0},
    buttonPosition: {align: 'left', y: 32, x: 0},
    buttons: [{
      type: 'second',
      count: 60,
      text: '60s'
    }, {
      type: 'minute',
      count: 5,
      text: '5min'
    }, {
      type: 'minute',
      count: 30,
      text: '30min'
    }, {
      type: 'hour',
      count: 1,
      text: '1h'
    }, {
      type: 'hour',
      count: 12,
      text: '12h'
    }, {
      type: 'day',
      count: 1,
      text: '1d'
    }, {
      type: 'all',
      text: 'All'
    }]
  },
  scrollbar: {
    height: 5,
    margin: 0,
    minWidth: 0,
    showFull: false,
    zIndex: 0,
    barBackgroundColor: 'transparent',
    barBorderColor: 'transparent',
    barBorderRadius: 0,
    barBorderWidth: 0,
    buttonBackgroundColor: 'transparent',
    buttonArrowColor: 'transparent',
    buttonBorderColor: 'transparent',
    buttonBorderWidth: 0,
    buttonBorderRadius: 0,
    trackBackgroundColor: 'transparent',
    trackBorderColor: 'transparent',
    trackBorderWidth: 0,
    trackBorderRadius: 0,
    rifleColor: 'transparent'
  }
};

let STYLE_SPLINE = merge(STYLE_BASE, {
  chart: {type: "spline"}
});

let STYLE_SCATTER = merge(STYLE_BASE, {
  chart: {type: "scatter"}
});

let STYLE_COLUMN = merge(STYLE_BASE, {
  chart: {type: "column"}
});

let STYLE_BAR = merge(STYLE_BASE, {
  chart: {type: "bar"}
});

let STYLE_PIE = merge(STYLE_BASE, {
  chart: {type: "pie"},
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
      }
    }
  }
});


let STYLE_CHART = {
  "spline": STYLE_SPLINE,
  "pie": STYLE_PIE,
  "bar": STYLE_BAR,
  "column": STYLE_COLUMN,
};