
console.log("Confirm order payment.")
var orderPaymentBtns = $(".confirm")
function stop_reloading(slug) {
  $('#'+slug).html(`<i class="fe fe-check"></i> Confirm`);
}
for (i = 0; i < orderPaymentBtns.length; i++) {
	orderPaymentBtns[i].addEventListener('click', function(){
		var slug = this.dataset.slug
		var url = this.dataset.url
		console.log('Slug:', slug)
        confirmPayment(slug, url)
        console.log(this)
        this.innerHTML = `<i class="fas fa-redo-alt fa-pulse"></i>`
	})
}
 function confirmPayment(slug, url){
        console.log('confirming payment....')
       fetch(url, {
          method:'POST',
          headers:{
             'Content-Type':'application/json',
             'X-CSRFToken':csrftoken,
          },
          body:JSON.stringify({'id':slug})
       })
       .then((response) => {
       stop_reloading(slug)
           console.log(response)
           if (response['statusText'] != 'OK'){
           iziToast.error({
               title: response['status'],
               message: response['statusText'],
               position: 'topRight'
             });
             }
          return response.json();
       })
       .then((data) => {
       stop_reloading(slug)
           console.log(data)
           if (data['message']){
                 iziToast.success({
                   title: 'Payment Confirmed:',
                   message: data['message'],
                   position: 'topRight'
                 });
             setTimeout(function () {
             location.reload()
            }, 5200);
           }
       });
 }