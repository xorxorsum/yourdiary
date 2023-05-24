$(".toggle-mnu").click(function() {
  $(this).toggleClass("on");
  $(".hidden-mnu").slideToggle();
  return false;
});

new WOW(
  {
    mobile: false
  }
).init();

$('#multiCarousel').carousel({
  interval: 10000
});


$(function() {
  $('.carousel-eq').slick({});

  $('.open-popuplink').magnificPopup({
    type:'inline',
    midClick: true,
    cursor: 'mfp-zoom-out-cur'
  });

	//SVG Fallback
	if(!Modernizr.svg) {
		$("img[src*='svg']").attr("src", function() {
			return $(this).attr("src").replace(".svg", ".png");
		});
	};


  let callbackBtn = document.getElementById('callbackButton');
  let closeBtn = document.querySelector('.tag-remove');

  callbackBtn.addEventListener("click", function() {
    var docHeight = $(document).height();
    $(".send").addClass("show");
    $("body").append("<div id='overlay'></div>");
    $("#overlay")
      .height(docHeight)
      .css({
       'opacity' : 0.4,
       'position': 'absolute',
       'top': 0,
       'left': 0,
       'background-color': 'black',
        'width': '100vw',
        'z-index': 900
      });
  });

  closeBtn.addEventListener('click', function() {
    $(".send").removeClass("show");
    $("#overlay").remove();
  });

  document.addEventListener("keydown", function(e){
    let ktype = e.key;
    if (ktype == "Escape") {
      $(".send").removeClass("show");
      $("#overlay").remove();
    }
  });

  $(document).ready(function() {
    const form = document.getElementById('callbackForm');
  	$(".send").submit(formSend);

    async function formSend(e) {
      e.preventDefault();

      let error = formValidate(form);

      if (error === 0) {
        form.classList.add('_sending');
        var th = $(this);
        $.ajax({
          type: "POST",
          url: "../../appointment.php", //Change
          data: th.serialize()
        }).done(function() {
          setTimeout(function() {
            th.trigger("reset");
          }, 1000);
        });
        return false;
      } else {
        alert('Заполните обязательные поля.')
      }
    }

    function formValidate(form) {
      let error = 0;
      let formReq = document.querySelectorAll('._req')

      for (var i = 0; i < formReq.length; i++) {
        const input = formReq[i];
        formRemoveError(input);

        if (input.classList.contains('_phone')) {
          if (phoneTest(input)) {
            formAddError(input);
            error++;
          }
        } else {
          if (input.value === '') {
            formAddError(input);
            error++;
          }
        }
      }
      return error;
    }
    function formAddError(input) {
      input.parentElement.classList.add('_error');
      input.classList.add('_error');
    }
    function formRemoveError(input) {
      input.parentElement.classList.remove('_error');
      input.classList.remove('_error');
    }
    function phoneTest(input) {
      return !/\+\d{1}\(\d{3}\)\d{3}-\d{4}/g.test(input.value);
    }

  });



});
