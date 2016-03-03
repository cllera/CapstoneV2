$(function() {
	//jQuery methods will go here
	//initially hide everything but first scene

	//puts all scene divs into an array for sorting by id
	var divArr = $('.sceneDiv').toArray();

	//hides all scenes
	$('.sceneDiv').hide(); 

	//shows first scene and hides remaining scenes
	for (d in divArr) {
		if (divArr[0].id) {
			var divID = divArr[0].id;
			$('#' + divID).show();
		};
	};

	//when button is clicked, button's id (next scene) will be used to bring up new info
	$('button').click(function() {
		$('.sceneDiv').hide(1000); //fade out! Woot.
		// console.log('first one' + nxtScnID);
		for (d in divArr) {
			var nxtScnID = this.id;
			if (divArr[d].id == nxtScnID) {
				$('#' + nxtScnID + '.sceneDiv').show(1000);
			};
		};
	});
});





// ******************** Helpful notes *************************:
// $(this).hide() - hides the current element.

// $("p").hide() - hides all <p> elements.

// $(".test").hide() - hides all elements with class="test".

// $("#test").hide() - hides the element with id="test".

// .toggle will let us switch back and forth

	// 	// console.log('div' + index + ':' + this.attr('id'));

// http://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_hide_slow


