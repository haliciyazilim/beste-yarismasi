/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('SignUpController', SignUpController);

    function SignUpController($rootScope, $scope, $log, $location, authorization) {


        $scope.form = {
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            phone_number: '',
            gender: '',
            address: '',
            city: '',
            password: '',
            password_validation: ''
        };
        $scope.currentGender = 'Cinsiyet';


        $scope.setGender = function (gender) {
            $scope.currentGender = gender;
            $scope.form.gender = gender;
        };


        $scope.signUp = function () {

            authorization.signUp($scope.form).then(
                function (result) {
                    $log.info('result', result);
                    $location.url('profil')
                },
                function (error) {
                    $log.error('error', error);
                })
        }


    }
})();