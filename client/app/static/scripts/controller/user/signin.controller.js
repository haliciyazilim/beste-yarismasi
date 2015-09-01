/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('SignInController', SignInController);

    function SignInController($scope, $location, $log, authorization) {

        $scope.form = {
            username: '',
            password: ''
        };


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
                    $location.url('profil');
                },
                function (error) {

                }
            );
        }


    }
})();