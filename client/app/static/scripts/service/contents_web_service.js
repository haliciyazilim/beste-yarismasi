/**
 * Created by abdullah on 08/08/15.
 */
(function () {

    'use strict';

    angular.module('besteApp')
        .factory('contentWebService', function ($http, $q, requestService, apiUrl, $log) {

            var ContentWebService = {};


            ContentWebService.getContentsForIndex = function () {
                return requestService.get(null, 'contents');
            };

            ContentWebService.getContent = function (contentLink) {
                return requestService.get(null, 'contents', contentLink);
            };

            ContentWebService.getLinks = function (contentLink) {
                return requestService.get(null, 'links', contentLink);
            };

            return ContentWebService;
        });
})();