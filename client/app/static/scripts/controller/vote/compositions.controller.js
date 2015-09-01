/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('CompositionsController', CompositionsController);

    function CompositionsController($rootScope, $scope, $log, authorization, trackWebService) {


        $scope.user = authorization.getUser();
        $scope.tracks = [];

        trackWebService.getTracks().then(
            function (result) {

                if (!$scope.user || !$scope.user.isSuperuser) {

                    result.sort(function (a, b) {

                        if (a.isQualified && !b.isQualified)
                            return -1;
                        else if (!a.isQualified && b.isQualified)
                            return 1;

                        return 0;
                    });
                }

                $scope.tracks = result;
            },
            function (error) {

            }
        );

        var setTracksVoteStatus = function (track) {

            for (var i = 0; i < $scope.tracks.length; i++) {
                var currentTrack = $scope.tracks[i];

                if (currentTrack.id == track.id) {
                    $scope.tracks[i].isQualified = track.isQualified;
                    $scope.tracks[i].isFinalist = track.isFinalist;
                    $scope.tracks[i].isVoteForQualificationOnAction = false;
                    $scope.tracks[i].isVoteForFinalOnAction = false;
                    break;
                }

            }
        };


        $scope.vote = function (track, isForFinal) {

            if (!$scope.user || !$scope.user.isSuperuser)
                return;

            var isQualified = false;
            var isFinalist = false;

            if (isForFinal != null) {
                isQualified = true;
                isFinalist = !track.isFinalist;
                track.isVoteForFinalOnAction = true;

            }
            else {
                isQualified = !track.isQualified;
                isFinalist = false;
                track.isVoteForQualificationOnAction = true;
            }


            trackWebService.voteForQualification(track.id, isQualified, isFinalist).then(
                function (result) {
                    $log.info('vote result: ', result);
                    setTracksVoteStatus(result);
                },
                function (error) {
                    $log.info('vote error: ', result);
                    if (isForFinal != null)
                        track.isFinalist = !track.isFinalist;
                    else
                        track.isQualified = !track.isQualified;

                    setTracksVoteStatus(track);
                }
            );
        }

    }
})();