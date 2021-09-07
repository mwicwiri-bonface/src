console.log("Creating customer")
$(document).ready(function() {
        $("#sign-up").submit(function(event) {
           event.preventDefault();
           $("#sign-up-tn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-last_name").html('');
                        $("#error-email").html('');
                        $("#error-first_name").html('');
                        $("#error-password1").html('');
                        $("#error-password2").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#sign-up-tn").html('Signup');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Account Not Created:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Account Created:',
                            message: response['message'],
                            position: 'topRight'
                          });
                         setTimeout(function () {
                         location.href = response['redirect']
                        }, 5200);
                        }
                        if(response['form']['last_name']) {
                           $("#error-last_name").html(response['form']['last_name']);
                        }
                        if(response['form']['first_name']) {
                           $("#error-first_name").html(response['form']['first_name']);
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
                    $("#sign-up-tn").html('Signup');
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