var gulp = require('gulp');
var changed = require('gulp-changed');
var filelog = require('gulp-filelog');
var imageResize = require('gulp-image-resize');
var imageMin = require('gulp-imagemin');
var plumber = require('gulp-plumber');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var browserify = require('browserify');
var uglify = require('gulp-uglify');
var compass = require('gulp-compass');
var shell = require('gulp-shell');
var del = require('del');
var runSequence = require('run-sequence');
var notify = require('gulp-notify');
var pyjade = require('gulp-pyjade');
var livereload = require('gulp-livereload');

var paths = {
  staticDir:  './app/development/static',
  distStaticDir: './app/development/dist/static',
  productionDir: './app/production',
  distDir: './app/development/dist',
  templateDir: './app/development/template',
  distTemplateDir: './app/development/dist/template'
};


// gulp-starter
// https://github.com/greypants/gulp-starter
// Copyright 2014 Daniel Tello
// Released under the MIT license
// https://github.com/greypants/gulp-starter/blob/master/LICENSE.md
///////////////////////////////////////////////////////////////////
var handleErrors = function() {
  var args = Array.prototype.slice.call(arguments);

  // Send  error to notification center with gulp-notify
  notify.onError({
    title:  "Compile Error",
    message: "<%= error %>"
  }).apply(this, args);

  // Keep gulp from hanging on this task
  this.emit('end');
};
///////////////////////////////////////////////////////////////////

gulp.task('build:image', function() {
  var srcGlob = paths.staticDir + '/img/**/*';
  var distGlob = paths.distStaticDir + '/img';
  var resize_opt = {
    width: 260,
    height: 370,
    gravity: 'Center',
    crop: false,
    upscale: true,
    imageMagick: true
  };
  var imageminOpt = {
    optimizationLevel: 7
  };

  return gulp.src(srcGlob)
    .pipe(plumber({errorHandler: notify.onError('<%= error.message %>')}))
    .pipe(changed(distGlob))
    .pipe(imageResize(resize_opt))
    .pipe(imageMin(imageminOpt))
    .pipe(gulp.dest(distGlob))
    .pipe(filelog());
});

gulp.task('build:js', function() {
  var entrieFile = paths.staticDir + '/js/main.js';
  var distGlob = paths.distStaticDir + '/js';

  return browserify(entrieFile)
    .bundle()
    .on('error', handleErrors)
    .pipe(source('app.js'))
    .pipe(buffer())
    .pipe(uglify({preserveComments: 'some'}))
    .pipe(gulp.dest(distGlob))
    .pipe(filelog());
});

gulp.task('build:compass', function() {
  var srcGlob = paths.staticDir + '/sass/**/*.sass';
  var distGlob = paths.distStaticDir + '/css';
  var configPath = './config.rb';

  return gulp.src(srcGlob)
    .pipe(plumber({errorHandler: notify.onError('<%= error.message %>')}))
    .pipe(compass({
      config_file: configPath,
      css: distGlob,
      sass: paths.staticDir + '/sass'
    }))
    .pipe(filelog());
});

gulp.task('build:pyjade', function() {
  return gulp.src(paths.templateDir + '/**/*.jade')
    .pipe(pyjade({engine: "tornado"}))
    .on('error', handleErrors)
    .pipe(gulp.dest(paths.distTemplateDir))
    .pipe(filelog());
});

gulp.task('clean:dist', function(cb) {
  return del([paths.distDir + '/**/*'], cb);
});

gulp.task('clean:production', function(cb) {
  return del([paths.productionDir + '/**/*'], cb);
});

gulp.task('copy:production', ['clean:production'], function() {
  return gulp.src(paths.distDir + '/**/*')
    .pipe(gulp.dest(paths.productionDir))
    .pipe(filelog());
});

gulp.task('copy:dist', function() {
  var favicon = paths.staticDir + '/favicon.ico';
  var fontPath = paths.staticDir + '/font/**/*';
  return gulp.src([favicon, fontPath], {base: paths.staticDir})
    .pipe(changed(paths.distStaticDir))
    .pipe(gulp.dest(paths.distStaticDir))
    .pipe(filelog());
});

gulp.task('watch', function() {
  livereload.listen();
  gulp.watch(paths.templateDir + '/**/*.jade', ['build:pyjade']);
  gulp.watch(paths.staticDir + '/sass/**/*.sass', ['build:compass']);
  gulp.watch(paths.staticDir + '/js/**/*.js', ['build:js']);
  gulp.watch(paths.staticDir + '/img/**/*', ['build:image']);
  gulp.watch(paths.distDir + '/**/*', function(e) {
    return livereload.changed(e.path);
  });
});

gulp.task('clean', ['clean:dist', 'clean:production']);

gulp.task('build', function() {
  runSequence(
    'clean', ['build:pyjade', 'build:compass', 'build:js', 'copy:dist', 'build:image'],
    'copy:production'
  );
});
gulp.task('default', ['build']);
