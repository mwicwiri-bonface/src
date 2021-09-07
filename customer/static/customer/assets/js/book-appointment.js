console.log("Book Payment")
$(document).ready(function() {
        $("#book_appointment").submit(function(event) {
           event.preventDefault();
           $("#id-book-appointment-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-date").html('');
                        $("#error-stop_date").html('');
                        $("#error-booking").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#id-book-appointment-btn").html('Book');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Appointment Not Made:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Appointment:',
                            message: response['message'],
                            position: 'topRight'
                          });
                        }
                        if(response['form']['date']) {
                           $("#error-date").html(response['form']['date']);
                        }
                        if(response['form']['stop_date']) {
                           $("#error-stop_date").html(response['form']['stop_date']);
                        }
                        if(response['form']['booking']) {
                           $("#error-booking").html(response['form']['booking']);
                        }

                    },
                    error: function (request, status, error) {
                    $("#id-book-appointment-btn").html('Book');
                         console.log(request.responseText);
                         iziToast.error({
                            title: status,
                            message: error,
                            position: 'topRight'
                          });

                    }
           });
       });
    })