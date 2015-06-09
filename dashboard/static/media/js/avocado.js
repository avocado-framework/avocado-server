/*
 * Avocado Server Javascript library.
 * Copyright (c) 2015 Red Hat.
 * Author: Ruda Moura <rmoura@redhat.com>
 */

var avocadoServerSettings = {
    url: "/",
};

var avocadoServer = {
    init: function(settings) {
        avocadoServer.settings = settings;
    },
    getVersion: function(success) {
        $.getJSON(this.settings.url + "version/", success);
    },
    getJobs: function(params, success) {
        console.log(params);
        $.getJSON(this.settings.url + "jobs/", params, success);
    },
    getLastJob: function(success) {
        $.getJSON(this.settings.url + "jobs/", {ordering:"-time"}, function ( json ) {
            success(json.results[0]);
        });
    },
    getJobTrend: function(success) {
        $.getJSON(this.settings.url + "jobs/", {ordering:"-time", page_size:10}, success);
    },
    getJobsSummary: function(success) {
        $.getJSON(this.settings.url + "jobs/summary/", success);
    },
    getTestsSummaryForJob: function(job_id, success) {
        $.ajax({
            url: this.settings.url + "jobs/" + job_id + "/tests/summary/",
            type: "GET",
            async: false,
            dataType: 'json',
            success: success,
        });
    }
};
