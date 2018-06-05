$(document).ready( function() {
	$('#post-form').on('submit', function(event){
    	event.preventDefault();
    	if($('#name').val() == 'si'){
     		if(!$('#divx').is(':visible')){
     			$('#divx').show();
     		}
   		}
    	console.log('form submitted!')  // sanity check
	});
	$('#id_boludo').on('change', function() {
  		if(this.value === 'si'){
  			//alert($('#hid_div').attr('style'));
  			if(!$('#hid_div').is(':visible')){
  				$('#hid_div').show();
  			}
  		}
  		else{
  			if($('#hid_div').is(':visible')){
  				$('#hid_div').hide();
  			}
  		}
	});
	$('#checkbox_webpage').change(function(){
		if(this.checked){
			$('#url_th').show();
		}
		else{
			$('#id_url').val('');
			$('#url_th').hide();
		}
	});
});

