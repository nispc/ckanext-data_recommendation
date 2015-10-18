// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('data_recommendation', function ($, _) {
  return {
    initialize: function () {
        $('#tag-nav>li:first').addClass('active');
        $('#tag-content>div:first').addClass('active');
    }
  };
});