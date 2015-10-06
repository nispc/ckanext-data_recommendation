// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('graph', function ($, _) {
  return {
    initialize: function () {
    //console.log(categories);
      $(function() {
      // console.log(categories);
        $.getScript("http://code.highcharts.com/highcharts.js").done(function() {
            $(function () {
                $('#stack_chart').highcharts({
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: '相同的標籤'
                    },
                    xAxis: {
                        categories: categories
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: '包含這個標籤的資料集'
                        },
                        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                            }
                        }
                    },
                    legend: {
                        align: 'right',
                        x: -30,
                        verticalAlign: 'top',
                        y: 25,
                        floating: true,
                        backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                        borderColor: '#CCC',
                        borderWidth: 1,
                        shadow: false
                    },
                    tooltip: {
                        headerFormat: '<b>{point.x}</b><br/>',
                        pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
                    },
                    plotOptions: {
                        column: {
                            stacking: 'normal',
                            dataLabels: {
                                enabled: true,
                                color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                                style: {
                                    textShadow: '0 0 3px black'
                                }
                            }
                        }
                    },
                    series: series
                });
            });
          })
      });


        var word_array = [];

        for(var tag in tags){
             // console.log(tag, tags[tag]);
             if( tags[tag]  )
                 word_array.push({
                    text: tags[tag][0],
                    weight: tags[tag][1]['sum'],
                    link: "/dataset?tags=" + tags[tag][0]
                 });
        }


       //console.log(word_array);
      $(function() {
        $.getScript("/jqcloud-1.0.4.js").done(function() {
            // $('#tag_cloud').html('aaa');
            $('#tag_cloud').jQCloud(word_array);
        })
      });

      $('#graph-nav>li>a').click(function(){
        $(this).parent().addClass('active');
        $(this).parent().siblings().removeClass('active');
        $('#' + $(this).attr('href').slice(1)).show();
        $('#' + $(this).attr('href').slice(1)).siblings().hide();
        event.preventDefault();
      })
    }
  };
});