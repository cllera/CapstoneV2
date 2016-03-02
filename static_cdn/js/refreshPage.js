$(function() {
	//jQuery methods will go here
	$("button").click(function() {
		//hide everything and then show what they want to show
		$("p").hide();
	});
});





// ******************** Helpful notes *************************:
// $(this).hide() - hides the current element.

// $("p").hide() - hides all <p> elements.

// $(".test").hide() - hides all elements with class="test".

// $("#test").hide() - hides the element with id="test".