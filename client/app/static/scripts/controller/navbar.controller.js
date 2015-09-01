/**
 * Created by abdullah on 11/08/15.
 */

(function () {
    'use strict';

    angular.module('besteApp').controller('NavbarController', NavbarController);

    function NavbarController($rootScope, $scope, $log, $location, authorization) {

        $scope.form = {
            username: '',
            password: ''
        };

        $scope.user = null;

        $scope.login = function () {

            $log.info('Username: ', $scope.form.username);
            $log.info('Password: ', $scope.form.password);

            if (!$scope.form.username) {
                $log.error('username yok');
                return;
            }
            if (!$scope.form.password) {
                $log.error('password yok');
                return;
            }

            authorization.login($scope.form).then(
                function (result) {
                    $scope.user = authorization.getUser();
                },
                function (error) {

                }
            );
        };

        $scope.logout = function (user) {
            authorization.logout().then(
                function (result) {
                    $log.info('logout result:', result);
                    $scope.user = null;
                    $location.url('/');
                },
                function (error) {
                    $log.error('logout error:', error);
                    $scope.user = null;
                    $location.url('/');
                }
            );


            $log.info('user: ', user);
        };

        $scope.goToProfile =

            $scope.$on('login-status-changed', function (event, args) {

                $scope.user = authorization.getUser();

                $log.info('login-status-changed', $scope.user);
            });
        $scope.user = authorization.getUser();
    }
})();