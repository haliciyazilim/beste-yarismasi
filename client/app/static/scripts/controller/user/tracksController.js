/**
 * Created by abdullah on 20/08/15.
 */

(function () {
    'use strict';

    angular.module('besteApp').controller('TracksController', TracksController);

    function TracksController($scope, $log, authorization, Upload, trackWebService) {


        $scope.user = authorization.getUser();

        $scope.devices = [];
        $scope.softwares = [];
        $scope.stageMaterials = [];

        var Track = function (data) {

            this.id = null;
            this.name = '';
            this.file = null;
            this.url = '';
            this.devices = [];
            this.softwares = [];
            this.stageMaterials = [];

            this.isFileUploadStarted = false;
            this.isFileUploadCompleted = false;
            this.shouldTrackDetailCreate = false;

            if (data) {
                this.id = data['id'];
                this.name = data['name'];
                this.url = data['url'];
                this.devices = data['devices'];
                this.softwares = data['softwares'];
                this.stageMaterials = data['stageMaterials'];
            }

            var self = this;

            this.onDeviceSelect = function (object) {
                $log.info('on decvice select');
                if (object.originalObject.name)
                    self.devices.push(object.originalObject);
            };

            this.onSoftwareSelect = function (object) {
                self.softwares.push(object.originalObject)
            };

            this.onStageMaterialSelect = function (object) {
                self.stageMaterials.push(object.originalObject)
            };

            this.removeSelected = function (index, type) {

                $log.info('remove selected: ', index + ', ' + type);
                if (index < 0 || !type)
                    return;

                if (type == 'device')
                    self.devices.splice(index, 1);
                else if (type == 'software')
                    self.softwares.splice(index, 1);
                else if (type == 'stage')
                    self.stageMaterials.splice(index, 1)
            };

            this.onEnter = function (object, type) {
                $log.info('On Enter ', object);

                if (!object || !type)
                    return;

                var object = {name: object.searchStr};

                if (type == 'device')
                    self.devices.push(object);
                else if (type == 'software')
                    self.softwares.push(object);
                else if (type == 'stage')
                    self.stageMaterials.push(object)


            }
        };
        //$scope.tracks=[new Track(), new Track()]
        $scope.tracks = [];

        var getTrackRequiremenst = function () {
            trackWebService.getTrackRequiremenst().then(
                function (result) {
                    $scope.devices = result.devices;
                    $scope.softwares = result.softwares;
                    $scope.stageMaterials = result.stageMaterials;
                    $scope.currentContest = result.currentContest;
                },
                function (error) {

                }
            );
        };

        var getTracks = function () {
            trackWebService.getTracks(authorization.getUser().id).then(
                function (result) {
                    for (var i = 0; i < 2; i++) {
                        var track = result[i];
                        $log.info('get tracks: ', track);

                        $scope.tracks.push(new Track(track));

                    }
                },
                function (error) {

                }
            );
        };

        $scope.upload = function (file, track) {

            track.file = file;
            track.isFileUploadStarted = true;
            track.isFileUploadCompleted = false;

            trackWebService.uploadTrack(file, $scope.currentContest.year).then(
                function (result) {
                    track.isFileUploadCompleted = true;
                    track.url = result;
                    if (track.shouldTrackDetailCreate)
                        $scope.createOrUpdate(track)
                },
                function (error) {
                    track.isFileUploadCompleted = true;
                },
                function (progress) {


                }
            );


            //Upload.upload({
            //    url: '../api/upload',
            //    sendFieldsAs:'json',
            //    fields: {'username': $scope.user.username, track:angular.toJson(track)},
            //    file: file,
            //    data: angular.toJson(track)
            //    }).progress(function (evt) {
            //        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            //        console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            //    }).success(function (data, status, headers, config) {
            //        console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            //    }).error(function (data, status, headers, config) {
            //        console.log('error status: ' + status);
            //    })

            //$scope.upload = $upload.upload({
            //        url: '../api/upload',
            //        method: 'POST',
            //        data: angular.toJson(track),
            //        file: file
            //    }).progress(function (evt) {
            //        $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total, 10);
            //    }).success(function (data, status, headers, config) {
            //        console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            //    }).error(function (data, status, headers, config) {
            //        console.log('error status: ' + status);
            //    });
        };

        var handleArray = function (array) {
            var newArray = [];
            angular.forEach(array, function (item) {

                if (item.name && item.name.length > 0)
                    newArray.push(item)
            });

            return newArray;
        };

        $scope.createOrUpdate = function (track) {

            if (track.isFileUploadStarted && !track.isFileUploadCompleted) {
                $log.info('track is in upload progress');
                track.shouldTrackDetailCreate = true;
                return;
            }

            var param = {
                id: track.id,
                name: track.name,
                url: track.url,
                devices: handleArray(track.devices),
                softwares: handleArray(track.softwares),
                stageMaterials: handleArray(track.stageMaterials),
                contest: $scope.currentContest.id
            };


            trackWebService.createOrUpdate(param).then(
                function (result) {
                    $log.info('track success: ', result);
                },
                function (error) {
                    $log.info('track error: ', error);
                },
                function (progress) {
                    $log.info('track progress: ', progress);

                }
            );
        };

        getTrackRequiremenst();
        getTracks();
    }
})();