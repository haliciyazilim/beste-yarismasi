/**
 * Created by abdullah on 08/08/15.
 */
(function () {

    'use strict';

    angular.module('besteApp')
        .factory('authorization', function ($rootScope, $q, $localStorage, $location, requestService, apiUrl, $log) {

            var accessLevels = routingConfig.accessLevels,
                userRoles = routingConfig.userRoles,
                publicUser = {first_name: '', user_type: userRoles.public},
                currentUser = $localStorage.user || publicUser;

            if (!currentUser.user_type) {
                currentUser = publicUser;
            }


            var setUserDataToLocalStorage = function (user, token) {

                if (!user || !token) {
                    delete $localStorage.token;
                    delete $localStorage.user;

                    $log.info('setUserDataToLocalStorage delete');
                }
                else {
                    $localStorage.token = token;
                    user.user_type = accessLevels.user;
                    $localStorage.user = user;
                    $log.info('setUserDataToLocalStorage set');
                }


            };

            var Authorization = {};

            Authorization.isAuthorized = function (accessLevel, role) {
                if (role === undefined)
                    role = currentUser.user_type;

                //if(accessLevel==accessLevels.admin || accessLevel==accessLevels.user ){
                //    if($localStorage.token)
                //       return  true;
                //    else
                //        return false;
                //}

                $log.info('isAuthorized accessLevel: ', accessLevel);
                $log.info('isAuthorized role: ', currentUser.user_type);

                return accessLevel & role;
            };

            Authorization.getToken = function () {
                return $localStorage.token;
            };

            Authorization.getUser = function () {
                return $localStorage.user;
            };

            Authorization.signUp = function (params) {

                var deferred = $q.defer();

                requestService.post('signUp', params).then(
                    function (result) {
                        setUserDataToLocalStorage(result.user, result.token);
                        deferred.resolve(result);
                    },
                    function (error) {
                        deferred.reject(error);
                    }
                );

                return deferred.promise

            };

            Authorization.login = function (params) {
                var deferred = $q.defer();

                requestService.post('login', params).then(
                    function (result) {

                        $log.info('LOgin result: ' + result);
                        $log.info('LOgin token: ' + result.token);

                        setUserDataToLocalStorage(result.user, result.token);
                        $rootScope.$broadcast('login-status-changed');
                        deferred.resolve(result);
                    },
                    function (error) {
                        deferred.reject(error);
                    }
                );

                return deferred.promise
            };

            Authorization.logout = function (params) {

                var deferred = $q.defer();

                requestService.post('logout', params).then(
                    function (result) {
                        setUserDataToLocalStorage();
                        $rootScope.$broadcast('login-status-changed');
                        deferred.resolve(result);
                    },
                    function (error) {
                        setUserDataToLocalStorage();
                        $rootScope.$broadcast('login-status-changed');
                        deferred.reject(error);
                    }
                );

                return deferred.promise
            };

            Authorization.profile = function () {
                return requestService.post('profile');
            };


            return Authorization;
        });
})();