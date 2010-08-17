(function ($) {
/**
 * SimpleGallery
 * @version: 2.2.5
 * @params
   - external: enable external interface (starting slide controllable via: http://localhost:8000/de/plugins/#8)
   - thumbnails: enable thumbnail view on bottom of gallery
   - slideNav: enable next/back button on slideshow
   - autoSlideNav: shows slidenav only when hovering the picture
   - thumbNav: enable next/back button on thumbnail
   - navSelectors: classes for binding single/multiple next/back buttons
   - infinite: should gallery spin infinite?
   - cycleThumbnav: should thumbnav cycle too? Recommended when you have lots of thumbs
   - cycleThumbNavCount: items to slide at once
   - controls: show play/pause buttons
   - nummeric: display nummeric thumbnail navigation instead of image-based
   - nummericSeperator: seperator for seperating each item
   - status: show count status on fullview layer
   - statusSeperator: define seperator for currentCount and bound
   - caption: show captions from title and alt attributes
   - captionFx: define caption transitions, either fade, slide or toggle
   - htmlCaption: grabs html caption instead of alt/title caption
   - disableAnchor: disables default link behavior on fullview image
   - magnifier: show/hide magnifier
   - lightbox: enable lightbox functionality
   - ligthboxType: define lightbox type. Either colorbox or fancybox
   - lightboxOptions: transmit options for lightbox
   ##### todo
   - infiniteCycle
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
		before: bindBeforeCycleCallback, /* wouldn't recomend ;) */
		after: bindAfterCycleCallback, /* wouldn't recomend ;) */
		/* custom options */
		external: false,
		thumbnails: true,
		thumbNav: false,
		slideNav: true,
		autoSlideNav: false,
		navSelectors: { next: '#simplegallery_{{ instance.id }} .fv-nav a[href*=#next]', prev: '#simplegallery_{{ instance.id }} .fv-nav a[href*=#prev]' },
		cycleThumbNav: false,
		cycleThumbNavCount: 'auto', /* only auto works atm */
		infinite: true, /* hm check that thing */
		nummeric: false,
		nummericSeperator: ' | ',
		controls: true,
		status: true,
		statusSeperator: ' / ',
		caption: true,
		captionFx: 'fade', /* fade, slide, toggle */
		htmlCaption: false,
		disableAnchor: false,
		magnifier: true,
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

		// save some basic vars
		var bound = thumb.find('li a').length;
		var thumbWidth = thumb.find('li').outerWidth(true);
		var fullviewWidth = fullview.width();
		var visibleBound = Math.ceil(fullviewWidth/thumbWidth);
		if(options.cycleThumbNavCount == 'auto') options.cycleThumbNavCount = visibleBound;

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
		if(options.thumbnails && options.thumbNav && options.cycleThumbNav) $this.find('.thmb-nav').show();

		options = $.fn.extend({
			next: options.navSelectors.next,
			prev: options.navSelectors.prev
		}, options);
	}

	// autoshow/hide slideNav
	if(options.autoSlideNav) {
		// requires slideNav
		if(!options.slideNav) return false;
		// autohide nav
		$this.find('.fv-nav').hide();
		// attach events
		$this.find('.simplegallery_fullview').bind('mouseenter', function () {
			$this.find('.fv-nav').css('opacity', 1).stop().fadeIn();
		});
		$this.find('.simplegallery_fullview').bind('mouseleave', function () {
			$this.find('.fv-nav').stop().fadeOut();
		});
	}

	// cycle thumbnav
	if(options.thumbnails) {
		var thumbControls = {
			next: $this.find('.thmb-nav .thmb-next'),
			prev: $this.find('.thmb-nav .thmb-prev')
		}
		thumbControls.next.bind('click', function (e) {
			e.preventDefault();
			moveThumbNav('right');
			$(this).trigger('thumbBtnNext');
		});
		thumbControls.prev.bind('click', function (e) {
			e.preventDefault();
			moveThumbNav('left');
			$(this).trigger('thumbBtnPrev');
		});

		if(options.cycleThumbNav) {
			// set width and height
			thumb.css({
				width: (bound*thumbWidth),
				position: 'absolute',
				left: 0,
				top: 0
			});
			thumb.parent().addClass('thmb_cycle').css({
				width: fullviewWidth,
				height: thumb.find('li a').outerHeight(true)
			});
		}
	}

	// nummeric navigation
	if(options.nummeric) {
		thumb.find('li a').each(function (index) {
			var seperator = (index == 0) ? '' : options.nummericSeperator;
			$(this).html(seperator+(index+1));
		});
		thumb.addClass('thmb-nummeric');
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

	// show current status
	if(options.status) {
		var status = $this.find('.fv-status');
			status.show();
	}

	// implement caption
	if(options.caption) { var caption = $this.find('.fv-caption'); caption.show(); }
		$this.find('.fv-caption-inline').hide();
		$this.find('.fv-caption-block').hide();

	// load lightbox
	if(options.lightbox) {
		// show magnifier
		var magnifier = $this.find('.fv-magnifier');
			if(options.magnifier) magnifier.show();
		// attach ligtbox event
		if(options.lightboxType == 'fancybox') $this.find('a[rel^=lightbox]').fancybox(options.lightboxOptions);
		if(options.lightboxType == 'colorbox') $this.find('a[rel^=lightbox]').colorbox(options.lightboxOptions);
	} else {
		// disattach events from pictures
		if(options.disableAnchor) {
			fullviewImages.bind('click', function (e) { e.preventDefault(); gallery.cycle('next'); });
			fullviewImages.css('cursor', 'default');
		}
	}

	// function that will be triggered before (initiated at first load)
	function bindBeforeCycleCallback(currSlideElement, nextSlideElement, options, forwardFlag) {
		// calc index for before
		var index = gallery.find('li').index($(nextSlideElement));

		// caption effect
		if(options.caption) {
			// show caption immediately
			var speed = (init) ? options.speed : 0;
			var title = $(nextSlideElement).find('a').attr('title');
			var desc = $(nextSlideElement).find('a img').attr('alt');

			if(init && options.captionFx == 'fade') caption.stop().fadeOut();
			if(init && options.captionFx == 'slide') caption.stop().slideUp();
			if(init && options.captionFx == 'toggle') caption.stop().hide();
			// do some delay
			setTimeout(function () {
				if(options.htmlCaption) {
					caption.find('.fv-caption-block').hide();
					$(caption.find('.fv-caption-block')[index]).show();
				} else {
					caption.find('.fv-caption-inline').show();
					caption.find('p').html('<span>' + title + '</span>' + desc);
				}
			}, speed);
		}
		// check thumbNav
		if(options.thumbnails && options.cycleThumbNav) {
			// rewrite active class setting for better performance
			thumb.find('li').removeClass('active');
			$(thumb.find('li')[(index)]).addClass('active');

			// switching
			if((index) == (visibleBound*(thmbPos+1))) moveThumbNav('right');

			// if reached 0 than move to left
			if(index == 0) { thumb.stop().animate({'left': 0}); thmbPos = 0; }
		}
		// change status
		if(options.status) status.html((index+1) + options.statusSeperator + options.slideCount);
		// animation started
		if(init) $this.trigger('animation.start');
	}

	// function that will be triggered after (initiated at first load)
	function bindAfterCycleCallback(currSlideElement, nextSlideElement, options, forwardFlag) {
		// get the index
		var index = 0;

		// caption effect
		if(options.caption && !($(nextSlideElement).find('a').attr('title') == '' 
						   && $(nextSlideElement).find('a img').attr('alt') == '')) {
			if(options.captionFx == 'fade') caption.css('opacity', 1).stop().fadeIn();
			if(options.captionFx == 'slide') caption.css('height', 'auto').stop().slideDown();
			if(options.captionFx == 'toggle') caption.css('display', 'block').stop().show();
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
		if(options.lightbox) magnifier.unbind().bind('click', function (e) { 
			e.preventDefault();
			$.colorbox({'open':true, 'href': $(nextSlideElement).find('a').attr('rel').replace('lightbox group ', '')});
		});
		// external interface
		if(options.external) window.location.hash = options.currSlide+1;
		// animation ended
		if(init) $this.trigger('animation.end');
		// gallery has been initiated
		init = true;
	}

	// save the current slide
	var thmbPos = options.startingSlide;
	// move thumb navigation
	function moveThumbNav(pos) {
		if(pos == 'left') {
			if(!(thmbPos <= 0)) {
				thmbPos--;
				thumb.stop().animate({'left': -(thmbPos*(thumbWidth*options.cycleThumbNavCount))});
			}
		} else {
			if(!((thmbPos*options.cycleThumbNavCount) >= (bound-visibleBound))) {
				thmbPos++;
				thumb.stop().animate({'left': -(thmbPos*(thumbWidth*options.cycleThumbNavCount))});
			}
		}
	}

	// init main gallery
	gallery.cycle(options);
};
})(jQuery);