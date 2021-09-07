console.log('updating profile')
    $('#id-profile').submit(function(e){
        e.preventDefault();
        $("#id-profile-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
        $form = $(this)
        var formData = new FormData(this);
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            beforeSend: function() {
                $("#error-last_name").html('');
                $("#error-email").html('');
                $("#error-first_name").html('');
                $("#error-phone_number").html('');
                $("#error-gender").html('');
                $("#error-image").html('');
            },
            success: function (response) {
                console.log(response);
                $("#id-profile-btn").html('Update Profile');
                if(response['info']) {
                 iziToast.info({
                    title: 'Profile Not Updated:',
                    message: response['info'],
                    position: 'topRight'
                  });
                }
                if(response['message']) {
                 iziToast.success({
                    title: 'Profile Updated:',
                    message: response['message'],
                    position: 'topRight'
                  });
                setTimeout(function () {
                    location.reload()
                }, 2000);
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
                if(response['p_form']['phone_number']) {
                   $("#error-phone_number").html(response['p_form']['phone_number']);
                }
                if(response['p_form']['gender']) {
                   $("#error-gender").html(response['p_form']['gender']);
                }
                if(response['p_form']['image']) {
                   $("#error-image").html(response['p_form']['image']);
                }
            },
            error: function (request, status, error) {
            $("#id-profile-btn").html('Update Profile');
                 console.log(request.responseText);
                 iziToast.error({
                    title: status,
                    message: error,
                    position: 'topRight'
                  });
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });