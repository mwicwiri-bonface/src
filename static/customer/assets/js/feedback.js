console.log("Sending feedback ... ")
$(document).ready(function() {
        $("#feedback").submit(function(event) {
           event.preventDefault();
           $("#feedback-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-subject").html('');
                        $("#error-message").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#feedback-btn").html('Send');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Feedback Not Sent:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Feedback Sent:',
                            message: response['message'],
                            position: 'topRight'
                          });
                        }
                        if(response['form']['subject']) {
                           $("#error-subject").html(response['form']['subject']);
                        }
                        if(response['form']['message']) {
                           $("#error-message").html(response['form']['message']);
                        }

                    },
                    error: function (request, status, error) {
                    $("#feedback-btn").html('Send');
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