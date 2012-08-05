
$(document).ready(function(){
   
   $(".display").click(function() {
       fileName = $(this).attr("src").split("/").pop();
      $("#preview img").attr("src",$(this).attr("src")); 
      $("#hidden_var").attr("value","/static/img/base_memes/" + fileName);
   });
    
});
