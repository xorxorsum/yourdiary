$(function(){


  $(".toggle-mnu").click(function() {
    $(this).toggleClass("on");
    $(".hidden-mnu-wrap").toggleClass('d-none');
    return false;
  });

  // var fadeElem = document.querySelector('.fade-anim');
  // var fadeBtn = document.querySelector('.fadeBtn');
  //
  // fadeBtn.addEventListener('click', function() {
  //   fadeElem.classList.add('elementFadeout');
  // })

});
