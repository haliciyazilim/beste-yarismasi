/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('ProfileController', ProfileController);

    function ProfileController($rootScope, $scope, $log, authorization) {


        $scope.user = authorization.getUser()
    }
})();