newvideo_link = $('.newvideo_link')
newvideo_link.hover(
    function(){
        $(this).children('picture').css("opacity","1");
        $(this).children('.link_to_newvideo').css("color","#ff0000");
    },
    function(){
        $(this).children('picture').css("opacity","0.5");
        $(this).children('.link_to_newvideo').css("color","#ffffff");
    },
    )

// Появление кнопки перемотки вверх
    window.onscroll = function() {
        if(window.pageYOffset>300){
          document.getElementById('upbutton').style.display="block";
      
        }
        else{
           document.getElementById('upbutton').style.display="none";
        }
      }