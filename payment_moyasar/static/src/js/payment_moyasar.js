// Capture the form submit button
$("#submit_button_id").click(function(event){
  event.preventDefault();
  // Get form data
  var form_data = $("#contactForm1").serialize();
  var errmsg = $('#error_msg');
  // Sending a POST request to Moyasar API using AJAX
  $.ajax({
  url: "https://api.moyasar.com/v1/payments",
  type: "POST",
  data: form_data,
  dataType: "json",
})
// uses `.done` callback to handle a successful AJAX request
.done(function(data) {
// Here we will handle JSON response and do step3 & step4
var payment_id = data.id;
// Redirect the user to transaction_url
var url = data.source.transaction_url;
window.location.href=url;
})
.fail(function (data) {
                    console.log('An error occurred.');
                console.log(data);
                errmsg.text(' حدث خطأ فى ادخال البيانات او الرصيد غير كافي');
                });
});



//    console.log('hi ....');
//    var frm = $('#contactForm1');
//    var errmsg = $('#error_msg');
//    frm.submit(function (e) {
//
//        e.preventDefault();
//
//        $.ajax({
//            type: frm.attr('method'),
//            url: frm.attr('action'),
//            data: frm.serialize(),
//            success: function (data) {
//                console.log('Submission was successful.');
//                console.log(data);
//            },
//            error: function (data) {
//                console.log('An error occurred.');
//                console.log(data);
//                errmsg.text(' حدث خطأ فى ادخال البيانات او الرصيد غير كافي');
//
//            },
//        });
//    });
