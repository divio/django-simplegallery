/**
 * @framework	CFF - Classy Frontend Framework
 * @author		Angelo Dini
 * @copyright	http://www.divio.ch under the BSD Licence
 * @requires	jquery, cycle, classy
 *
 * check if classy.js and cycle exists */
 if($.fn.cycle === undefined) log('jquery.gallery.js: cycle.js is required!');
 if(window['Class'] === undefined) log('jquery.gallery.js: classy.js is required!');

/*##################################################|*/
/* #GALLERY# */
(function ($, Class) {
	/**
	 * Cl.Gallery
	 * @version: 3.0.0
	 * @params
		- fx: transition style - see http://jquery.malsup.com/cycle/browser.html
		- timeout: default timeout
		- speed: transition speed
		- startingSlide: index where to initiate the gallery
		- activePagerClass: active class for selected page
		- before: add trigger event for gallery
		- after: add trigger event for gallery
		- ui: enable/disable or add ui elements
		- plugins: enable/disable or add plugins
		- keys: define keycodes for next/prev event
		- cls: modify finder classes
		- autoplay: should gallery autoplay?
	 */
	Cl.Gallery = Class.$extend({
		
		options: {
			/* cycle settings | see http://jquery.malsup.com/cycle/options.html */
			fx: 'fade', /*  */
			timeout: 5000,
			speed: 900,
			startingSlide: 0,
			activePagerClass: 'active',
			before: function () {$(this).trigger('cycle.before');},
			after: function () {$(this).trigger('cycle.after');},
			/* ui loaders */
			ui: {
				caption: true,
				controls: true,
				thumbnails: true
			},
			/* plugin loaders */
			plugins: {
				external: true,
				keycontrol: true,
				lightbox: true,
				lightboxOptions: {}
			},
			/* use jquery keycodes */
			keys: {
				next: 39,
				prev: 37
			},
			/* control css classes */
			cls: {
				canvas: '.gallery-list',
				canvas_elements: '.gallery-list-slide',
				active: 'active',
				controls: '.gallery-controls',
				controls_play: '.gallery-ctrl-play',
				controls_pause: '.gallery-ctrl-pause',
				controls_next: '.gallery-ctrl-next',
				controls_prev: '.gallery-ctrl-prev',
				caption: '.gallery-caption',
				thumb: '.gallery-thumbs',
				thumb_els: '.gallery-thumbs-slide',
				thumb_next: '.gallery-thumbs-next',
				thumb_prev: '.gallery-thumbs-prev'
			},
			/* custom settings */
			autoplay: true
		},
		
		initialize: function (el, options) {
			var classy = this;
			// check if only one element is given
			if($(el).length > 2) { log('Gallery Error: one element expected, multiple elements given.'); return false; }
			
			/* merge defaults */
			this.options = $.extend(this.options, options);
			this.hooks = {};
			
			this.gallery = $(el);
			this.canvas = this.gallery.find(this.options.cls.canvas);
			this.elements = this.gallery.find(this.options.cls.canvas_elements);
			
			// load ui/plugin elements
			this.loadUI();
			this.loadPlugins();
			
			// init gallery
			this.initGallery();
		},
		
		loadUI: function () {
			var ui = this.options.ui;
			
			if(ui.caption) this.uiCaption();
			if(ui.controls) this.uiControls();
			if(ui.thumbnails) this.uiThumbnails();
		},
		
		loadPlugins: function () {
			var plugins = this.options.plugins;
			
			if(plugins.external) this.pluginExternal();
			if(plugins.keycontrol) this.pluginKeyControl();
			if(plugins.lightbox) this.pluginLightbox();
		},
		
		uiCaption: function () {
			this.gallery.find(this.options.cls.caption).show();
		},
		
		uiControls: function () {
			var classy = this;
			var cls = this.options.cls;
			var play = this.gallery.find(cls.controls+' '+cls.controls_play);
				(this.options.autoplay) ? play.data('active', true) : play.data('active', false);
			var pause = this.gallery.find(cls.controls+' '+cls.controls_pause);
				(this.options.autoplay) ? pause.data('active', false) : play.data('active', true);
			var next = this.gallery.find(cls.controls+' '+cls.controls_next);
			var prev = this.gallery.find(cls.controls+' '+cls.controls_prev);
			
			// show element
			this.gallery.find(cls.controls).show();
			
			// initial setup
			if(play.data('active')) play.addClass(cls.active);
			if(pause.data('active')) play.addClass(cls.active);
			
			// play button
			play.bind('click', function (e) {
				e.preventDefault();
				classy.canvas.cycle('resume');
				
				play.data('active', true).addClass(cls.active);
				pause.data('active', false).removeClass(cls.active);
			});
			
			// pause button
			pause.bind('click', function (e) {
				e.preventDefault();
				classy.canvas.cycle('pause');
				
				pause.data('active', true).addClass(cls.active);
				play.data('active', false).removeClass(cls.active);
			});
			
			// next button
			next.bind('click', function (e) {
				e.preventDefault();
				classy.canvas.cycle('next');
			});
			
			// prev button
			prev.bind('click', function (e) {
				e.preventDefault();
				classy.canvas.cycle('prev');
			});
		},
		
		uiThumbnails: function () {
			var classy = this;
			var cls = this.options.cls;
			var thumbs = this.gallery.find(cls.thumb);
				thumbs.find('> ul').show();
			var elements = thumbs.find(cls.thumb_els);
			var next = thumbs.find(cls.thumb_next);
			var prev = thumbs.find(cls.thumb_prev);
			var bound = elements.length;
			var index = null;
			
			// catch before event
			this.elements.bind('cycle.before', function (e) {
				index = classy.elements.index($(e.currentTarget));
				
				// add / remove active class
				elements.removeClass(cls.active);
				$(elements[index]).addClass(cls.active);
				
				// check if first in loop and add active state
				(index == 0) ? prev.addClass(cls.active) : prev.removeClass(cls.active);
				// check if last in loop and add active state
				(index == (bound-1)) ? next.addClass(cls.active) : next.removeClass(cls.active);
			});
			
			// add click event to thumbnails
			elements.bind('click', function (e) {
				e.preventDefault();
				classy.canvas.cycle(elements.index($(e.currentTarget)));
			});
			
			// next button
			next.bind('click', function () {
				classy.canvas.cycle('next');
				return false;
			});
			
			// back button
			prev.bind('click', function () {
				classy.canvas.cycle('prev');
				return false;
			});
		},
		
		// navigate to specific gallery item via hashcode
		// http://localhost:8000/de/plugins/#3 (jump to slide 3)
		pluginExternal: function () {
			var classy = this;
			var hash = window.location.hash.split('#')[1]-1;
				// if(hash == 'NaN') hash = 0;
				hash = (!isNaN(hash)) ? hash : 0;
			// transfere value
			this.options.startingSlide = hash;
			
			// catch before event
			this.elements.bind('cycle.before', function (e) {
				index = classy.elements.index($(e.currentTarget));
				window.location.hash = index+1;
			});
		},
		
		pluginKeyControl: function () {
			var classy = this;
			$(document).keypress(function (key) {
				if(key.keyCode == classy.options.keys.next) classy.canvas.cycle('next');
				if(key.keyCode == classy.options.keys.prev) classy.canvas.cycle('prev');
			});
		},
		
		pluginLightbox: function () {
			// attach lightbox to elements
			if($.fn.colorbox !== undefined) this.elements.find('a[rel^=lightbox]').colorbox(this.options.lightboxOptions);
			if($.fn.shadowbox !== undefined) this.elements.find('a[rel^=lightbox]').shadowbox(this.options.lightboxOptions);
			if($.fn.fancybox !== undefined) this.elements.find('a[rel^=lightbox]').fancybox(this.options.lightboxOptions);
		},
		
		initGallery: function () {
			// start gallery
			this.canvas.parent().css('max-height', ''); /* fix showing all images */
			this.canvas.cycle(this.options);
		}
		
	});
})(jQuery, Class);