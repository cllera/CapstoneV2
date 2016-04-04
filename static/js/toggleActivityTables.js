$(function() {

	//array of activities for each event
	var actArr = $('.actEvtDiv').toArray();

	for (h in actArr) {
		$('#' + actArr[h].id + '.actEvtDiv').hide();
	};

	// When option is selected...
	$('#selEvent').click(function() {
		var selectedOption = $('#selEvent').val();

		for (a in actArr) {
			if (actArr[a].id == selectedOption) {
				$('#' + selectedOption + '.actEvtDiv').show();
			}
			else if (actArr[a].id !== selectedOption) {
				$('#' + actArr[a].id + '.actEvtDiv').hide();
			};
		};
	});
});