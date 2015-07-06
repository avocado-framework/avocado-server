/*
 * Avocado dashboard Javascript library.
 * Copyright (c) 2015 Red Hat.
 * Author: Ruda Moura <rmoura@redhat.com>
 */

var avocadoDashboard = {
    server: avocadoServer,
    init: function() {
        $( document ).ajaxError(function( event, jqxhr, settings, thrownError ) {
            $( "#errors" ).show();
            if ( settings.url.match( "version/$" )) {
                $( "#errors" ).append( "<p>Could not get server version from " + avocadoServerSettings.url + "</p>" );
            } else if ( settings.url.match( "jobs/summary/$" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve jobs summary from " + settings.url +  "</p>" );
            } else if ( settings.url.match( "jobs/" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve job results from " + settings.url + "</p>" );
            } else if ( settings.url.match( "tests/summary/$" ) ) {
                $( "#errors" ).append( "<p>Failed to retrieve tests summary from " + settings.url + "</p>" );
            } else {
                $( "#errors" ).append( "<p>Generic error on request " + settings.url + "</p>" );
            }
            if (jqxhr.responseText) {
                detail = jQuery.parseJSON( jqxhr.responseText ).detail;
                $( "#errors" ).append( "<p>Reason: " + detail + "</p>" );
            }
        });
        this.server.init(avocadoServerSettings);
    },
    version: function() {
        this.server.getVersion(function( json ) {
           $( "#info" ).text( "Server version: " + json.version );
        });
    },
    syncJobs: function() {
        if ( $.fn.dataTable.isDataTable( "#results") ) {
            var jobs_table = $("#results").DataTable();
        } else {
            var jobs_table = $( "#results" ).dataTable({
                order: [[0, "desc"]],
                columns: [
                    { title: "Date", data: "time"},
                    { title: "Id", data: "id"},
                    { title: "Description", data: "description"},
                    { title: "Status", data: "status" },
                    { title: "Tests", data: "tests_total" },
                    { title: "Elapsed Time", data: "elapsed_time"},
                ],
                serverSide: true,
                ajax: function(data, callback, settings) {
                    console.log(data);
                    avocadoServer.getJobs({
                            page_size: data.length,
                            page: (data.start / data.length)+1,
                            ordering: (data.order[0].dir == "desc" ? "-" : "") + data.columns[data.order[0].column].data
                        }, function( json ) {
                            $.each(json.results, function(index, value) {
                                value.tests_total = value.tests.length;
                            });
                            callback({
                                recordsTotal: json.count,
                                recordsFiltered: json.count,
                                data: json.results,
                            });
                    });
                }
            });
        }

    },
    syncOverview: function() {
        this.plotLastTestResult();
        this.plotLastJobResult();
        this.plotTrend();
    },
    plotLastTestResult: function() {
        this.server.getLastJob(function( json ) {
            avocadoDashboard.server.getTestsSummaryForJob(json.id, function( summary_json ) {
                json.tests_summary = summary_json;
                var pieData = [
                    {
                        value: json.tests_summary.failed,
                        color: "#F7464A",
                        highlight: "#FF5A5E",
                        label: "Failed"
                    }, {
                        value: json.tests_summary.other,
                        color: "#949FB1",
                        highlight: "#A8B3C5",
                        label: "Other"
                    }, {
                        value: json.tests_summary.passed,
                        color: "#46BFBD",
                        highlight: "#5AD3D1",
                        label: "Passed"
                    } ];
                var ctx = $("#chart-area-last").get(0).getContext("2d");
                var pieJobs = new Chart(ctx).Pie(pieData);
            });
        });
    },
    plotLastJobResult: function() {
        this.server.getJobsSummary(function( json ) {
            var pieData = [
                {
                    value: json.failed,
                    color: "#F7464A",
                    highlight: "#FF5A5E",
                    label: "Failed"
                }, {
                    value: json.other,
                    color: "#949FB1",
                    highlight: "#A8B3C5",
                    label: "Other"
                }, {
                    value: json.passed,
                    color: "#46BFBD",
                    highlight: "#5AD3D1",
                    label: "Passed"
                } ];

            var ctx = $("#chart-area-jobs").get(0).getContext("2d");
            var pieLastJob = new Chart(ctx).Pie(pieData);
        });
    },
    plotTrend: function() {
        this.server.getJobTrend(function ( json ) {
            var trend = {
                labels: [],
                datasets: [
                    {
                        label: "Passed",
                        fillColor: "rgba(70,191,189,0.5)",
                        strokeColor: "rgba(70,191,189,0.8)",
                        highlightFill: "rgba(70,191,189,0.75)",
                        highlightStroke: "rgba(70,191,189,1)",
                        data: []
                    },
                    {
                        label: "Failed",
                        fillColor: "rgba(248,70,74,0.5)",
                        strokeColor: "rgba(247,70,74,0.8)",
                        highlightFill: "rgba(247,70,74,0.75)",
                        highlightStroke: "rgba(247,70,74,1)",
                        data: []
                    },
                    {
                        label: "Other",
                        fillColor: "rgba(148,159,177,0.5)",
                        strokeColor: "rgba(148,159,177,0.8)",
                        highlightFill: "rgba(148,159,177,0.75)",
                        highlightStroke: "rgba(148,159,177,1)",
                        data: []
                    }
                ]
            };
            $.each(json.results, function( index, value ) {
                var shortid = json.results[index].id.substring(0,7);
                trend.labels.push(shortid);
                avocadoServer.getTestsSummaryForJob( value.id, function( json ) {
                    trend.datasets[0].data.push(json.passed);
                    trend.datasets[1].data.push(json.failed);
                    trend.datasets[2].data.push(json.other);
                });
            });
            var ctx = $("#chart-area-trend").get(0).getContext("2d");
            var barTrend = new Chart(ctx).Bar(trend);
        });
    }
};
