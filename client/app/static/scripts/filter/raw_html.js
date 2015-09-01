/**
 * Created by abdullah on 09/08/15.
 */
(function () {

    'use strict';

    angular.module('besteApp').filter('rawHtml', ['$sce',
        function ($sce) {
            return function (val) {
                return $sce.trustAsHtml(val);
            };
        }]);
})();