/**
 * Created by abdullah on 08/08/15.
 */

(function () {

    'use strict';

    angular.module('besteApp').provider('apiUrl', function () {

        var hostname = "sss";
        var port = "";
        var urls = {
            links: "links",
            contents: "contents",
            signUp: "user/signup",
            login: "user/login",
            logout: "user/logout",
            profile: "user/profile",
            trackRequirements: "tracks/requirements",
            tracks: "tracks",
            tracksForVote: "tracks/finalist",
            vote: "vote",
            contests: "contests"
        };

        this.setHostname = function (name) {
            hostname = name
        };

        this.setPort = function (portNumber) {
            port = portNumber;
        };

        // Private constructor
        function APIUrl() {
            this.hostname = hostname;
            this.port = port;
            this.urls = urls;

            this.getUrl = function (key, arg) {

                console.log('hostName: ', this.hostname);
                console.log('hostName: ', hostname);

                var url = this.urls[key],
                    argsArray;
                // allow the user to use a function which generates the url depending on some params
                if (angular.isFunction(url)) {
                    argsArray = Array.prototype.slice.call(arguments);
                    argsArray.splice(0, 1);
                    url = url.apply(null, argsArray);
                }

                //var result= location.protocol + "//" + this.hostname+':'+this.port + '/api/' + url;
                var result = '/api/' + url;
                if (arg)
                    result += '/' + arg;
                result += '.json';
                console.log('api url: ', result);
                return result;
            }
        }


        // Method for instantiating
        this.$get = function () {
            return new APIUrl();
        };
    });
})();