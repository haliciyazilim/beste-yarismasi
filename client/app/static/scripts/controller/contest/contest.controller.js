/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('ContestController', ProfileController);

    function ProfileController($rootScope, $scope, $routeParams, $log, contestWebService) {
        var contestYear=$routeParams.year

        contestWebService.getContest(contestYear).then(
            function (result) {
                $scope.contest=result.contest;
                $scope.tracks=result.tracks;
            },
            function (error) {

            }
        )
    }
})();