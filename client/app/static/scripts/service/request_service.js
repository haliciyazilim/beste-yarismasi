/**
 * Created by abdullah on 14/08/15.
 */

(function () {
    'use strict';

    angular.module('besteApp').factory('requestService', function ($http, $q, $log, apiUrl, $localStorage) {

        var RequestService = {};

        var requestMethods = {
            get: 'GET',
            post: 'POST',
        };

        var getConfig = function (requestMethod, url, param) {
            var config = {
                method: requestMethod,
                url: url,
                headers: {
                    Authorization: function () {
                        var token = $localStorage.token;
                        $log.info('getConfig Token: ', token);
                        if (token)
                            return 'Token ' + $localStorage.token;
                        else
                            return null;
                    }
                },
                data: param
            };

            return config;
        };

        var callRequest = function (requestMethod, params, method, urlExtra) {
            var deferred = $q.defer();
            //var param={params:params}

            var url = apiUrl.getUrl(method, urlExtra);
            $log.info('url: ', url);


            if (requestMethod == requestMethods.post) {
                //params=Object.removeNullsAndEmpties(params)
                params = Object.toUnderscoreKeys(params);

                $log.info('underscore: ', params);
            }


            var config = getConfig(requestMethod, url, params);
            $http(config).then(
                function (result) {

                    var data = Object.toCamelKeys(result.data);
                    $log.info(method, data);
                    deferred.resolve(data);
                },
                function (data) {
                    $log.error(method + ' Error: ', data);
                    data = Object.toCamelKeys(data);
                    deferred.reject(data);
                }
            );

            return deferred.promise;

        };
        RequestService.get = function (params, method, urlExtra) {
            return callRequest(requestMethods.get, params, method, urlExtra);
        };

        RequestService.post = function (method, params) {
            return callRequest(requestMethods.post, params, method)
        };

        return RequestService;
    });

})();
