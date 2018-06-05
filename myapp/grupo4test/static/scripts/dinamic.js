$(document).ready( function() {
	$('#id_pregunta1').on('change', function() {
      var x = document.getElementById("div_1");
  		if($("#id_pregunta1").val() == 'si'){
  			//alert('hola');
          x.style.display = "block";
      }
      else{
          x.style.display = "none";
          $('#id_pregunta1_1').val('');
          //$('#id_pregunta1_2').prop('checked', true);
      }
	});
  $('#id_pregunta1_2').on('change', function(){
    var x = document.getElementById("div_1_2");
    if(this.checked){
      x.style.display = 'block';
    }
    else{
      x.style.display = 'none';
      $('#id_pregunta1_2_1').val('');
    }
  });
  $('#id_pregunta3').on('change', function(){
    var x = document.getElementById("div_3_1");
      if($("#id_pregunta3").val() == 'mucho'){
        //alert('hola');
          x.style.display = "block";
      }
      else{
          x.style.display = "none";
          $('#id_pregunta3_1').val('');
      }
  });

});


