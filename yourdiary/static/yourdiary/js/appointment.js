let closeBtn = document.querySelector('.sign-remove');

document.addEventListener("keydown", function(e){
  let ktype = e.key;
  if (ktype == "Escape") {
    $(".sign").removeClass("show");
    $("#overlay").remove();
  }
});

appointmentBtn.addEventListener("click", function() {
  var docHeight = $(document).height();
  $(".sign").addClass("show");
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
  $(".sign").removeClass("show");
  $("#overlay").remove();
});

$(document).ready(function() {

  $('._phone').inputmask("+7(999)999-9999");

  const form = document.getElementById('appointmentForm');
	$(".sign").submit(formSend);

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
        location.href = "thankyou.html";
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
    let formReq = document.querySelectorAll('._reqA')

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
