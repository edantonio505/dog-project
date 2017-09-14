

Dropzone.options.myAwesomeDropzone = {
  paramName: "file", // The name that will be used to transfer the file
  createImageThumbnails: true,
  dictDefaultMessage: '',
  clickable:'.dog_display',
  init: function() {
	this.on("thumbnail", function(file) {
		$(".dog_display_background").hide();
		$("#classified").html("<h1>Loading...</h1><p style='font-size:30px;'>This may take a couple of minutes.</p>");
		$("#directions").hide();
		$('.dog_display').css('backgroundImage','url('+file.dataURL+')').css('background-size', 'cover');
		$(".dz-image , .dz-image-preview, .dz-preview").hide();
	});


	this.on("success", function(response){
		$(".loader-container").show();
		$(".loader").fadeIn();
		getBreed(response);
	});
  }
};





function getBreed(image){
	$.post('/get_breed', {image_name: image.name}, function(response){
		data = JSON.parse('{'+response+'}');

		var message = ''
		if (data.speciment == 'dog')
		{
			message = "This "+data.speciment+" is a "+data.dog_breed;
		}
		else if(data.speciment == 'human'){
			message = "This is a person who looks like a "+data.dog_breed;
		}
		else if(data.message != ''){
			message = data.message;
		}

		console.log(data);
		$("#classified").html("<h1>"+message+"</h1>");
		$(".loader").fadeOut();
		$(".loader-container").fadeOut();
	});
}	