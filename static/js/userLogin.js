// $(function () {
//     $('#newmember').on('.submit', function (e) {
//     	e.preventDefault();
//     	$.ajax({
//     		url: "/activityDashboard/"
//     		type: 'POST'
//     		data: $('').serialize
//     	})
//         $(this.form).submit();
//         // $('#myModalLabel').modal('hide');
//         $('#myModalLabel').hide();
//     });
// });


// $(document).ready(function() {
// 	$("a#myModalLabel").on("click", function() {
// 		$.post("ajax.html", function(data) {
// 			$("#becomeamember").html(data).fadeIn();
// 		});
// 	});
// });

$('#userLogin').on('submit', function(event){
	event.preventDefault();
	console.log("form submitted!")
	create_post();
});