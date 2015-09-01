/**
 * Created by abdullah on 07/08/15.
 */

module.exports = function (grunt) {

    'use strict';
    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                files: {
                    'dist/static/scripts/lib.js': ['app/static/bower/jquery/jquery.js',
                        'app/static/bower/angular/angular.js',
                        'app/static/bower/**/*.js'],
                    'dist/static/styles/lib.css': 'app/static/bower/**/*.css',
                    'dist/static/scripts/app.js': 'app/static/scripts/**/*.js',
                    'dist/static/styles/app.css': 'app/static/styles/**/*.css',
                }
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                files: {
                    'dist/static/scripts/lib.js': [
                        'static/bower/jquery/jquery.js',
                        'static/bower/angular/angular.js',
                        'static/bower/angular-route/angular-route.js',
                        'static/bower/ngstorage/ngstorage.js',
                        'static/bower/bootstrap/bootstrap.js',
                        'static/bower/agular-bootstrap/ui-bootstrap-tpls.js',
                    ],
                    'dist/static/styles/lib.css': 'static/bower/**/*.css',
                    'dist/static/scripts/app.js': 'static/scripts/**/*.js',
                    'dist/static/styles/app.css': 'static/styles/**/*.css',
                }
            }
        },
        watch: {
            scripts: {
                files: ['app/static/scripts/**/*.js', 'app/static/**/*.jade'],
                tasks: ['jade', 'concat'],
                options: {
                    spawn: true,
                    reload: true
                },
            },
        },
        wiredep: {
            task: {
                //directory:'src/bower',
                src: ['index.html']
            }
        },
        'string-replace': {
            dist: {
                files: {
                    'index.html': 'index.html',

                },
                options: {
                    replacements: [{
                        pattern: /bower_components/ig,
                        replacement: 'static/bower'
                    }]
                }
            }
        },
        jade: {
            compile: {
                options: {
                    data: {
                        debug: false
                    }
                },
                files: [{
                    expand: true,
                    src: '**/*.jade',
                    dest: 'dist/',
                    cwd: 'app/',
                    ext: '.html'
                }]
            }
        },
        jshint: {
            options: {
                jshintrc: '.jshintrc',
                reporter: require('jshint-stylish')
            },
            all: {
                src: [
                    'Gruntfile.js',
                    'app/static/scripts/**/*.js'
                ]
            },
            test: {
                options: {
                    jshintrc: 'test/.jshintrc'
                },
                src: ['test/spec/{,*/}*.js']
            }
        },
        copy: {
            main: {
                files: [
                    {expand: true, cwd: 'app/static/images/', src: ['**'], dest: 'dist/static/images/'},
                    {expand: true, cwd: 'app/static/fonts/', src: ['**'], dest: 'dist/static/fonts/'}]
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-wiredep');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-string-replace');
    grunt.loadNpmTasks('grunt-contrib-jade');
    grunt.loadNpmTasks('grunt-contrib-copy');


    grunt.registerTask('log', 'Log some stuff.', function () {
        grunt.log.write('Logging some stuff...').ok();
    });
    // Default task(s).
    grunt.registerTask('default', ['concat', 'jade', 'copy', 'log']);
    //grunt.registerTask('concat', ['concat', 'log']);
    //grunt.registerTask('watch', ['watch']);
};