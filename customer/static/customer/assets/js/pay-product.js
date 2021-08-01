console.log("checking out")
$(document).ready(function() {
        $("#checkout").submit(function(event) {
           event.preventDefault();
           $("#checkout-btn").html(`<i class="fas fa-redo-alt fa-pulse"></i>`);
           $.ajax({ data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    beforeSend: function() {
                        $("#error-phone").html('');
                        $("#error-mpesa").html('');
                        $("#error-amount").html('');
                    },
                    success: function(response) {
                        console.log(response);
                        $("#checkout-btn").html('Confirm and Pay');
                        if(response['info']) {
                         iziToast.info({
                            title: 'Payment Not sent:',
                            message: response['info'],
                            position: 'topRight'
                          });
                        }
                        if(response['message']) {
                         iziToast.success({
                            title: 'Payment Sent:',
                            message: response['message'],
                            position: 'topRight'
                          });
                         setTimeout(function () {
                         location.reload()
                        }, 5200);
                        }
                         if(response['mpesa']) {
                           $("#error-mpesa").html(response['mpesa']);
                        }
                        if (response['form']){
                            if(response['form']['phone']) {
                               $("#error-phone").html(response['form']['phone']);
                            }
                            if(response['form']['amount']) {
                               $("#error-amount").html(response['form']['amount']);
                            }
                        }

                    },
                    error: function (request, status, error) {
                    $("#checkout-btn").html('Confirm and Pay');
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