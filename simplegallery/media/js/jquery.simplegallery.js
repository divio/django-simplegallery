(function ($) {
/**
 * SimpleGallery
 * @version: 2.0
 * @params (items marked with # are not yet finished)
   - external: enable external interface (starting slide controllable via: http://localhost:8000/de/plugins/#8)
   - thumbnails: enable thumbnail view on bottom of gallery
   - slideNav: enable next/back button on slideshow
   - thumbNav: enable next/back button on thumbnail
   - navSelectors: classes for binding single/multiple next/back buttons
   - infinite: should gallery spin infinite?
   - cycleThumbnav: should thumbnav cycle too? Redommended when you have lots of thumbs
   - controls: show play/pause buttons
   - nummeric: display nummeric thumbnail navigation instead of image-based
   - nummericSeperator: seperator for seperating each item
   - caption: show captions from title and alt attributes
   - captionFx: define caption transitions, either fade, slide or toggle
   - lightbox: enable lightbox functionality
   - ligthboxType: define lightbox type. Either colorbox or fancybox
   - lightboxOptions: transmit options for lightbox
   # proper event delegation
 */
$.fn.simpleGallery = function (options) {
	// save element
	$this = $(this), init = false;
	// do some proper height calculation
	var gallery = $this.find('.simplegallery_fullview ul');
	var fullview = $this.find('.simplegallery_fullview');
		fullview.css('height', fullview.find('img').height());
	var fullviewImages = fullview.find('ul li a');

	// default settings
	var options = $.extend({
		fx: 'fade',
		timeout: 5000,
		speed: 900,
		startingSlide: 0,
		activePagerClass: 'active',
		/* callbacks */
		before: bindBeforeCycleCallback,
		after: bindAfterCycleCallback,
		/* custom options */
		external: false,
		thumbnails: true,
		cycleThumbNav: false,
		slideNav: true,
		thumbNav: false,
		navSelectors: { next: '.fv-nav a[href*=#next]', prev: '.fv-nav a[href*=#prev]' },
		infinite: true,
		controls: true,
		nummeric: false,
		nummericSeperator: ' | ',
		caption: true,
		captionFx: 'fade', /* fade, slide, toggle */
		lightbox: false,
		lightboxType: 'colorbox',
		lightboxOptions: {}
	}, options);

	// navigate to specific gallery item via hashcode
	// works like http://localhost:8000/de/plugins/#3 (jump to slide 3)
	if(options.external) {
		var hash = window.location.hash.split('#')[1]-1;
		// if(hash == 'NaN') hash = 0;
		hash = (!isNaN(hash)) ? hash : 0;
		// transfere value
		options.startingSlide = hash;
	}

	// attach thumbnail events
	if(options.thumbnails) {
		var thumb = $this.find('.simplegallery_thumbnails ul');
		// show thumbnails
		thumb.show();

		options = $.fn.extend({
			/* attach events */
			pager: thumb,
			pagerAnchorBuilder: function(index, DOMelement) {
				return thumb.find('li:eq(' + (index) + ') a');
			}
		}, options);
	}

	// attach next/prev trigger events to navigations
	if(options.slideNav || options.thumbNav) {
		if(options.slideNav) $this.find('.fv-nav').show();
		if(options.thumbNav) $this.find('.thmb-nav').show();

		options = $.fn.extend({
			next: options.navSelectors.next,
			prev: options.navSelectors.prev
		}, options);
	}

	// cycle thumbnav
	if(options.cycleThumbNav) {
		if(options.thumbNav) {
			var thumbControls = {
				next: $this.find('.thmb-nav .thmb-next'),
				prev: $this.find('.thmb-nav .thmb-prev')
			}
			thumbControls.next.bind('click', function (e) {
				e.preventDefault();
				$(this).trigger('thumbBtnNext');
				//console.log('next');
			});
			thumbControls.prev.bind('click', function (e) {
				e.preventDefault();
				$(this).trigger('thumbBtnPrev');
				//console.log('back');
			});
		}

		var bound = thumb.find('li a').length;
		var thumbWidth = thumb.find('li').outerWidth(true);
		//var thumbHeight = thumb.find('li').outerHeight(true);
		var fullviewWidth = fullview.width();

		// set width and height
		thumb.parent().addClass('thmb_cycle').css({
			width: fullviewWidth,
			height: thumb.find('li').outerHeight(true)
		});
		thumb.css({
			position: 'absolute',
			left: 0,
			top: 0
		});
	}

	// play/pause controls
	if(options.controls) {
		var controls = $this.find('.fv-controls');
			controls.show();
		var ctrls = {
			play: controls.find('a[href*=#play]'),
			pause: controls.find('a[href*=#pause]')
		}
		ctrls.play.hide();
		// pauser event
		ctrls.pause.bind('click', function () {
			gallery.cycle('pause');
			ctrls.pause.fadeOut();
			setTimeout(function () { ctrls.play.fadeIn(); }, 400);
		});
		// play event
		ctrls.play.bind('click', function () {
			gallery.cycle('resume');
			ctrls.play.fadeOut();
			setTimeout(function () { ctrls.pause.fadeIn(); }, 400);
		});
	}

	// nummeric navigation
	if(options.nummeric) {
		thumb.find('li a').each(function (index) {
			var seperator = (index == 0) ? '' : options.nummericSeperator;
			$(this).html(seperator+(index+1));
		});
		thumb.addClass('thmb-nummeric');
	}

	// implement caption
	if(options.caption) { var caption = $this.find('.fv-caption'); caption.show(); }

	// load lightbox
	if(options.lightbox) {
		// show magnifier
		var magnifier = $this.find('.fv-magnifier');
			magnifier.show();
		// attach ligtbox event
		if(options.lightboxType == 'fancybox') fullviewImages.fancybox(options.lightboxOptions);
		if(options.lightboxType == 'colorbox') fullviewImages.colorbox(options.lightboxOptions);
	} else {
		// disattach events from pictures
		fullviewImages.bind('click', function (e) { e.preventDefault(); gallery.cycle('next'); });
		fullviewImages.css('cursor', 'default');
	}

	// function that will be triggered before (initiated at first load)
	function bindBeforeCycleCallback(currSlideElement, nextSlideElement, options, forwardFlag) {
		// calc index for before
		var index = gallery.find('li').index($(nextSlideElement));

		// caption effect
		if(options.caption) {
			// show caption immediately
			var speed = (init) ? options.speed : 0;

			if(init && options.captionFx == 'fade') caption.fadeOut();
			if(init && options.captionFx == 'slide') caption.slideUp();
			if(init && options.captionFx == 'toggle') caption.hide();
			// do some delay
			setTimeout(function () {
				var title = $(nextSlideElement).find('a').attr('title');
				var desc = $(nextSlideElement).find('a img').attr('alt');
				caption.find('p').html('<span>' + title + '</span>' + desc);
			}, speed);
		}
		// check thumbNav
		if(options.cycleThumbNav) {
			// rewrite active class setting for better performance
			thumb.find('li').removeClass('active');
			$(thumb.find('li')[(index)]).addClass('active');
			// save variables
			var visibleBound = Math.floor(fullviewWidth/thumbWidth)-1;
			var currentTurn = Math.ceil((index+1)/visibleBound);
			var addWidth = 0;
			if(index >= visibleBound) addWidth = thumbWidth;
			// initiate animation
			thumb.animate({left: -(thumbWidth*visibleBound*(currentTurn-1))+addWidth});
		}
		// animation started
		if(init) $this.trigger('animation.start');
	}

	// function that will be triggered after (initiated at first load)
	function bindAfterCycleCallback(currSlideElement, nextSlideElement, options, forwardFlag) {
		// get the index
		var index = 0;

		// caption effect
		if(options.caption) {
			if(options.captionFx == 'fade') caption.fadeIn();
			if(options.captionFx == 'slide') caption.slideDown();
			if(options.captionFx == 'toggle') caption.show();
		}
		// infinite deactivation at last slide
		if(!options.infinite && (options.currSlide == (options.slideCount-1))) {
			gallery.cycle('pause');
			if(options.controls) ctrls.pause.trigger('click');
		}
		// add disabled classes to navigation items
		if((options.slideNav || options.thumbNav) && !options.infinite) {
			// first remove any classes
			$this.find(options.navSelectors.next).removeClass('fv-nav-disabled');
			$this.find(options.navSelectors.prev).removeClass('fv-nav-disabled');
			// than add specific classes
			if(options.currSlide == 0) {	
				$this.find(options.navSelectors.prev).addClass('fv-nav-disabled');
			} else if(options.currSlide == (options.slideCount-1)) {
				$this.find(options.navSelectors.next).addClass('fv-nav-disabled');
			}
		}
		// add mignifier event
		if(options.lightbox) magnifier.unbind().bind('click', function () { 
			$(nextSlideElement).find('a').trigger('click');
		});
		// external interface
		if(options.external) window.location.hash = options.currSlide+1;
		// animation ended
		if(init) $this.trigger('animation.end');
		// gallery has been initiated
		init = true;
	}

	var handler = function (e) { e.preventDefault(); };

	// proper event delegation (store events / retrieve events)
	$this.bind('animation.start', function () {
		//console.log('### animation started');
		//$this.bind('click', function (e) {
			//console.log('fire');
			//e.preventDefault();
			//e.stopPropagation();
			//e.stopImmediatePropagation();
		//});
	});
	$this.bind('animation.end', function () {
		//$this.log('### animation ended');
		//$this.unbind('click');
	});

	// init main gallery
	gallery.cycle(options);
};
})(jQuery);