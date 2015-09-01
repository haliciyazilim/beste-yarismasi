/**
 * Created by abdullah on 08/08/15.
 */
(function () {

    'use strict';

    angular.module('besteApp')
        .factory('contestWebService', function ($http, $q, requestService, apiUrl, $log) {

            var ContentWebService = {};

            ContentWebService.getContests = function () {
                return requestService.get(null, 'contests');
            };

            ContentWebService.getContest = function (id) {
                return requestService.get(null, 'contests', id);
            };

            return ContentWebService;
        });
})();