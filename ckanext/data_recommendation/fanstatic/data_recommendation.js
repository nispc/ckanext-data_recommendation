// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('data_recommendation', function ($, _) {
  return {
    initialize: function () {
      $('.related_pkg').each(function() {
        var title = $(this).find('h4 strong').text();
        //console.log(title);
        var that = this;
        $.getJSON( "/api/3/action/package_search?q=" + title, function( data ) {
            //console.log(data.result.results[0].title);
            if(data.success){
              if(data.result.count){
                //console.log('test');
                var results = data.result.results;
                for(var i = 0; i < results.length; i++){
                    var result = results[i];
                    $(that).find('ul').append('<li style="line-height: 25px;"><span class="label">'+result.organization.title+'</span><a href="/dataset/'+result.name+'" style="padding: 5px;">' + result.title + '</a></li>');
                    $(that).show("1000");
                }
              }
            }
        });

      });
      //console.log("I've been initialized for element: ", this.el);
    }
  };
});

