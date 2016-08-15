var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant'),
    less = require('gulp-less'),
    minifyCss = require('gulp-minify-css'),
    path = require('path'),
    ttf2woff = require('gulp-ttf2woff');

gulp.task('ttf2woff', function(){
  gulp.src(['./resources/fonts/ttf/**/*.ttf'])
    .pipe(ttf2woff())
    .pipe(gulp.dest('./resources/fonts/woff/'));
});

gulp.task('less', function() {
  return gulp.src('./resources/less/style.less')
    .pipe(less({
      // paths: [ path.join(__dirname, 'less', 'includes') ]
      // paths: [ './bower_components/jquery/dist/jquery.min.js' ]
    }))
    .pipe(minifyCss())
    .pipe(gulp.dest('./resources/css'));
});

gulp.task('watch', function() {
  gulp.watch('./resources/less/**/*.less', ['less']);
});

gulp.task('default', ['less', 'watch'], function(){});
