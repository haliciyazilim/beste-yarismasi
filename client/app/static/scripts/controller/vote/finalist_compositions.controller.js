/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('FinalistCompositionsController', FinalistCompositionsController);

    function FinalistCompositionsController($rootScope, $scope, $log, authorization, trackWebService) {


        $scope.user = authorization.getUser();

        $scope.tracks = [];
        $scope.ratingMax = 10;

        var setTracksVoteStatus = function (track) {

            for (var i = 0; i < $scope.tracks.length; i++) {
                var currentTrack = $scope.tracks[i];

                if (currentTrack.id == track.id) {
                    $scope.tracks[i].isQualified = track.rate;
                    $scope.tracks[i].isVoteOnAction = false;
                    break;
                }

            }
        };

        $scope.vote = function (track) {
            $log.info('track is rated: ', track.rate);

            trackWebService.voteForFinal(track.id, track.rate).then(
                function (result) {
                    $log.info('Track vote Success: ', result);
                },
                function (error) {
                    $log.error('Track vote Success: ', error);
                }
            );
        };

        var setVotesToTracks = function (tracks, votes) {

            for (var i = 0; i < tracks.length; i++) {

                var track = tracks[i];

                for (var f = 0; f < votes.length; f++) {
                    var vote = votes[f];

                    if (track.id == vote.composition) {

                        track.rate = vote.value;
                        break;
                    }
                }
            }

            return tracks;
        };

        trackWebService.getAllTrackForVote().then(
            function (result) {

                $scope.tracks = setVotesToTracks(result.compositions, result.votes);
                $scope.votes = result.votes;


                $log.info('Finalist Compositions: ', result)
            },
            function (error) {

            }
        );


    }
})();