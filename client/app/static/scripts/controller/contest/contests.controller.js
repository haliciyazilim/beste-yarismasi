/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('ContestsController', ContestsController);

    function ContestsController($rootScope, $scope, $log, contestWebService) {


        contestWebService.getContests().then(
            function (result) {
                $scope.contests=result;
            },
            function (error) {
                
            }
        )
        
    }
})();