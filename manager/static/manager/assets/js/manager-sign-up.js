console.log("Creating manager")
$(document).ready(function() {
        $("#manager-sign-up").submit(function(event) {
           event.preventDefault();
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-last-name").html('');
                        $("#error-email").html('');
                        $("#error-first-name").html('');
                        $("#error-password1").html('');
                        $("#error-password2").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        if(response['redirect']) {
                         location.href = response['redirect']
                        }
                        if(response['info']) {
                         iziToast.info({
                            title: 'Account Not Created:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['form']['last_name']) {
                           $("#error-last-name").html(response['form']['last_name']);
                        }
                        if(response['form']['first_name']) {
                           $("#error-first-name").html(response['form']['first_name']);
                        }
                        if(response['form']['email']) {
                           $("#error-email").html(response['form']['email']);
                        }
                        if(response['form']['password1']) {
                           $("#error-password1").html(response['form']['password1']);
                        }
                        if(response['form']['password2']) {
                           $("#error-password2").html(response['form']['password2']);
                        }

                    },
                    error: function (request, status, error) {
                         console.log(request.responseText);
                         $("#error").html(error);
                    }
           });
       });
    })