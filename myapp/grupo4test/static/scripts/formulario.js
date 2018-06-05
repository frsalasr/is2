$(document).ready( function() {
	$('#id_1').on('change', function() {
  		if($("#id_1").val() == '1'){
  			alert('hola');
      }
      else{
      		alert('chao');
          //$('#id_pregunta1_2').prop('checked', true);
      }
	});
});