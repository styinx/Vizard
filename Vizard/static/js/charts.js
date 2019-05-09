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
    borderWidth: 1,
    shadow: false,
    useHTML: true,
    style: {
      padding: 0,
    },
    formatter: function () {
      return this.points.map(function (point) {
        return '<span style="color:' + point.series.color + '">●</span> ' + time(point.x) + ': ' + point.y;
      });
    },
    positioner: function (w, h, point) {
      return {x: point.plotX + 20, y: 0};
      //return {x: point.plotX - w / 2, y: point.plotY - h - 15};
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

let STYLE_SPARK_SCATTER = Object.assign({
  chart: {
    type: "scatter"
  }
}, STYLE_SPARK_BASE);

/**
 * Holds general configuration about HighChart charts.
 */
let STYLE_BASE = {
  chart: {
    spacing: 0,
    height: 300
  },
  title: {text: "asd"},
  credits: {text: ""},
  xAxis: {
    minorTickInterval: 'auto',
    startOnTick: true,
    endOnTick: true,
    lineWidth: 1,
    lineColor: "#333",
    labels: { formatter: function () { return time(this.value); } }
  },
  yAxis: {
    minorTickInterval: 'auto',
    startOnTick: true,
    endOnTick: true,
    lineWidth: 1,
    lineColor: "#333",
    opposite: false
  },
  legend: {enabled: true},
  navigator: {
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
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
      }
    }
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
  },
  rangeSelector: {enabled: false}
};

let STYLE_SPLINE = merge(STYLE_BASE, {
  chart: {
    type: "spline"
  }
});

let STYLE_SCATTER = merge(STYLE_BASE, {
  chart: {
    type: "scatter"
  }
});