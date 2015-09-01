/**
 * Created by abdullah on 08/08/15.
 */
(function () {
    'use strict';

    angular.module('besteApp').controller('IndexController', IndexController);

    function IndexController($rootScope, $scope, $routeParams, $sce, $localStorage, $log, $location, contentWebService) {

        var contentLink = $routeParams.contentLink;
        $log.info('content Lİnk: ', contentLink);


        var getContentsForIndex = function () {

            //$scope.contents=$localStorage.contents;

            contentWebService.getContentsForIndex().then(
                function (data) {
                    var contents = data;
                    setContent(data[data.length - 1]);

                    $log.info('result: ', contents)

                },
                function (error) {

                });
        };

        var getContent = function (contentLink) {
            $scope.getContent(contentLink);
        };

        var getLinks = function () {
            contentWebService.getLinks().then(
                function (result) {
                    $scope.links = result;

                    $log.info('links: ', result);
                },
                function (error) {

                }
            );
        };

        $scope.getContent = function (contentLink, isForStatic) {

            if (!isForStatic) {
                $location.url(contentLink)
            }
            else {
                //$location.url(contentLink, false);
                //$location.path(contentLink)
                contentWebService.getContent(contentLink).then(
                    function (data) {
                        $log.info('current content: ', data);
                        setContent(data);

                    },
                    function (error) {

                    });
            }
        };

        var setContent = function (content) {
            $scope.currentContent = content;
            $scope.currentContent.content = $sce.trustAsHtml(content.content);
        };

        if (!contentLink) {
            getContentsForIndex();
        }
        else {
            getContent(contentLink);
        }

        getLinks();

    }


})();