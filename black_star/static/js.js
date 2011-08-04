	$(function(){
	  var obj = $('#content');
	  if (!obj.length) obj = $('#content-home');
	  if (!obj.length) obj = $('#content-404');
	  $(window).resize(function(){
	    var win_height = $(window).height();
	    var at_height = $('#header').outerHeight() + obj.outerHeight() + $('#footer').outerHeight()+40;
	    if (win_height >= at_height) {
	      $('#footer').addClass('footer-fixed');
	      obj.addClass('content-absolute');
	      var content_left = ($(this).width()-obj.outerWidth())/2;
	      if ($(this).width()<700) {
	        content_left = (700-obj.outerWidth())/2;
	      }
	      obj.css({
	           top: (win_height-obj.outerHeight()-20)/2,
	           left: content_left
	      });
	    } else {
	      $('#footer').removeClass('footer-fixed');
	      obj.removeClass('content-absolute');
	    }
	  });
	  $(window).resize();
	  
	  var resize_pic = function(which){
	    var max_width = $('#fp-max-width').val();
	    var max_height = $('#fp-max-height').val();
	    var ratio = 0;
	    var width = $(which).width();
	    var height = $(which).height();
	    if (width == 0 && height == 0) {
	      // read pic from cache
	      $(window).load(function(){resize_pic('.file-img');})
	      return false;
	    }
	    if (max_width > 0 && width > max_width) {
	      ratio = max_width/width;
	      $(which).css('width', max_width);
	      height = height * ratio;
	      $(which).css('height', height);
	    }
	    if (max_height > 0 && height > max_height) {
	      ratio = max_height/height;
	      $(which).css('height', max_height);
	      width = width * ratio;
	      $(which).css('width', width);
	    }
	    $(which).fadeIn();
	  }
	  $('.file-img').load(function(){
	    resize_pic(this)
	  });
	  
	  
	  $('#rand_url').click(function(){
	    $.ajax({
	      type: 'POST',
	      cache: false,
	      dateType: 'text',
	      url: $(this).attr('rel'),
	      success: function(data) {
	         $('#ufile_url').val(data);
	      }
	      
	    });
	  });
	  
	  $('.del-file-link').click(function(){
	    return confirm('Are you sure to delete this file?');
	  });
	});
	$(window).load(function(){
	  $(window).resize();
	});
