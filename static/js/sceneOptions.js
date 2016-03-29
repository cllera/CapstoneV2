$(function() {

	//array of rows to hide
	var rowArr = $('.hideRow').toArray();

	//array of main rows
	var mainArr = $('.mainSORow').toArray();

	$('.mainSORow').each(function(i) {
		$('td:first', this).html(i+1);
	});

	$('tr').click(function() {
		//if the .mainRow id is the same as the .hideRow id, show that row
		for (r in rowArr) {
			var rowID = this.id;
			if (mainArr[r].id == rowID) {
				$('#' + rowID + '.hideRow').toggle();
			};
		};
	});
});