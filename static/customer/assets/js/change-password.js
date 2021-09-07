console.log("Changing Password")
$(document).ready(function() {
        $("#change-password").submit(function(event) {
           event.preventDefault();
           $("#change-password-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-old_password").html('');
                        $("#error-new_password1").html('');
                        $("#error-new_password2").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#change-password-btn").html('Change Password');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Password Not Changed:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Password Changed:',
                            message: response['message'],
                            position: 'topRight'
                          });
                        }
                        if(response['form']['old_password']) {
                           $("#error-old_password").html(response['form']['old_password']);
                        }
                        if(response['form']['new_password1']) {
                           $("#error-new_password1").html(response['form']['new_password1']);
                        }
                        if(response['form']['new_password2']) {
                           $("#error-new_password2").html(response['form']['new_password2']);
                        }

                    },
                    error: function (request, status, error) {
                    $("#change-password-btn").html('Change Password');
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