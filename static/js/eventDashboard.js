//Belongs to eventDashboard.html and deals with custom.css elements

$(function() {

	//get array of event blocks below
	var evtArr = $('.br-bm-gd-lt').toArray();
	console.log(evtArr);

	$('#private').click(function() {
		var enfArr = $('.sub-event').toArray();
		for (e in enfArr) {
			console.log("EnfArr: " + enfArr[e].id);
		}

		for (e in evtArr) {
			if ($("input[type='checkbox']").is(":checked")) {
				for (n in enfArr) {
					if (enfArr[n].id == False) {
						$(this).hide();
					}
				}
			}
			else {
				for (n in enfArr) {
					$('#' + enfArr[n].id + '.sub-event').show();
				};
			};
		};
	});
});


