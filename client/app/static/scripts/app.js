/**
 * Created by abdullah on 08/08/15.
 */

(function () {
    'use strict';
    angular.module('besteApp', ['ngRoute', 'ngStorage', 'ui.bootstrap', 'ngFileUpload', 'angucomplete-alt'])
        .config(function ($interpolateProvider, $httpProvider, $locationProvider,
                          $routeProvider, apiUrlProvider) {

            //$interpolateProvider.startSymbol('{$');
            //$interpolateProvider.endSymbol('$}');

            $locationProvider.html5Mode({
                enabled: true,
                requireBase: false
            });

            //$locationProvider.html5Mode(true);
            //$locationProvider.hashPrefix('!');

            //$httpProvider.defaults.xsrfCookieName = 'csrftoken';
            //$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

            apiUrlProvider.setHostname('localhost');
            apiUrlProvider.setPort(8000);

            var access = routingConfig.accessLevels;

            $routeProvider
                .when('/', {
                    templateUrl: '/static/views/index.html',
                    controller: 'IndexController',
                    access: access.public

                })
                .when('/giris', {
                    templateUrl: '/static/views/user/sign_in.html',
                    controller: 'SignInController',
                    access: access.public
                })
                .when('/kayit', {
                    templateUrl: '/static/views/user/sign_up.html',
                    controller: 'SignUpController',
                    access: access.public
                })
                .when('/profil', {
                    templateUrl: '/static/views/user/profile.html',
                    controller: 'ProfileController',
                    access: access.user
                })
                .when('/eserler', {
                    templateUrl: '/static/views/vote/compositions.html',
                    controller: 'CompositionsController',
                    access: access.user
                })
                .when('/eleme/tum_eserler', {
                    templateUrl: '/static/views/vote/compositions.html',
                    controller: 'CompositionsController',
                    access: access.public
                })
                .when('/:username/eserler', {
                    templateUrl: '/static/views/user/tracks.html',
                    controller: 'TracksController',
                    access: access.user
                })
                .when('/oylama', {
                    templateUrl: '/static/views/vote/finalist_compositions.html',
                    controller: 'FinalistCompositionsController',
                    access: access.public
                })
                .when('/yarismalar/:year', {
                    templateUrl: '/static/views/contest/contest.html',
                    controller: 'ContestController',
                    access: access.public
                })
                .when('/yarismalar/', {
                    templateUrl: '/static/views/contest/contests.html',
                    controller: 'ContestsController',
                    access: access.public
                })
                .when('/:contentLink', {
                    templateUrl: '/static/views/index.html'
                    , controller: 'IndexController'
                })
                .otherwise('/');
        })
        .run(function ($http, $localStorage, $log, $rootScope, $location, authorization) {
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';
            //$http.defaults.headers.common['HTTP_AUTHORIZATION'] = $localStorage.token;

            //var token=authorization.getToken();
            //if(authorization.getToken()){
            //    $log.info('token var');
            //    $http.defaults.headers.common.Authorization = 'Token '+ authorization.getToken();
            //}
            //else
            //    $log.info('token yok')


            $rootScope.$on("$routeChangeStart", function (event, next, current) {

                if (next.access && !authorization.isAuthorized(next.access)) {

                    $log.info('roautechange: ', authorization.isAuthorized(next.access));
                    event.preventDefault();
                    var from = next.$$route.originalPath;
                    $rootScope.$evalAsync(function () {
                        //$location.url('/login?from='+escape(from));
                        $location.url('/');
                    });
                }
            });

        });
})();