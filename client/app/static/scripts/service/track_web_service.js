/**
 * Created by abdullah on 08/08/15.
 */
(function () {

    'use strict';

    angular.module('besteApp')
        .factory('trackWebService', function ($http, $q, requestService, apiUrl, $log) {

            var TrackWebService = {};


            TrackWebService.getTrackRequiremenst = function () {
                return requestService.get(null, 'trackRequirements');
            };

            TrackWebService.getTracks = function (userId) {
                return requestService.get(null, 'tracks', userId);
            };

            var uniqueString = function () {
                var text = new Date().getTime();
                var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

                for (var i = 0; i < 8; i++) {
                    text += possible.charAt(Math.floor(Math.random() * possible.length));
                }
                return text;
            };
            TrackWebService.uploadTrack = function (file, directory) {
                var deferred = $q.defer();

                var bucketPath = 'gong-ir/temp_attachments/beste';
                //var bucket='beste-yarisma/beste_deneme';

                if (directory){
                    bucket += '/' + directory;
                }

                var creds = {
                    accessKey: 'AKIAJ6FILHU6L567EJLA',
                    secretKey: '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',
                    bucket: bucketPath,
                    //accessKey:'AKIAJZPVU26EITJXQIOQ',
                    //secretKey:'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'
                };
                AWS.config.update({
                    accessKeyId: creds.accessKey, secretAccessKey: creds.secretKey,
                    //s3BucketEndpoint:true
                });
                AWS.config.region = 'eu-west-1';
                var bucket = new AWS.S3({params: {Bucket: creds.bucket, ACL: 'public-read'}});
                var uniqueFileName = uniqueString();
                var params = {Key: uniqueFileName, ContentType: file.type, Body: file, ServerSideEncryption: 'AES256'};
                bucket.putObject(params, function (err, data) {

                    if (err) {
                        console.log('Error: ', err);
                        deferred.reject(data);
                    }
                    else {
                        // Upload Successfully Finished
                        //toastr.success('File Uploaded Successfully', 'Done');
                        var imagePath = bucket.endpoint.href + creds.bucket + '/' + uniqueFileName;
                        console.log('Success: ', imagePath);

                        deferred.resolve(imagePath);
                    }
                })
                    .on('httpUploadProgress', function (progress) {
                        var uploadProgress = Math.round(progress.loaded / progress.total * 100);
                        deferred.notify(uploadProgress);
                        console.log('Upload Progress: ', uploadProgress);
                        //scope.$digest();
                    });

                return deferred.promise;
            };

            TrackWebService.createOrUpdate = function (track) {
                return requestService.post('tracks', track);
            };


            TrackWebService.getAllTrackForVote = function () {
                return requestService.get(null, 'tracksForVote');
            };

            var vote = function (params) {
                return requestService.post('vote', params);
            };
            TrackWebService.voteForQualification = function (trackId, isQualified, isFinalist) {
                var params = {
                    composition: trackId,
                    isQualified: isQualified,
                    isFinalist: isFinalist
                };

                return vote(params)
            };

            TrackWebService.voteForFinal = function (trackId, rating) {
                var params = {
                    composition: trackId,
                    value: rating
                };

                return vote(params)
            };


            return TrackWebService;
        });
})();