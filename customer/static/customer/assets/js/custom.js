
console.log("Add to cart.")
var cartBtns = document.getElementsByClassName('add-to-cart-btn')
function stop_reloading(slug) {
  $('#'+slug).html("Add to cart");
}
for (i = 0; i < cartBtns.length; i++) {
	cartBtns[i].addEventListener('click', function(){
		var slug = this.dataset.slug
		var url = this.dataset.url
		console.log('Slug:', slug)
        addToCart(slug, url)
        console.log(this)
        this.innerHTML = `<i class="fas fa-redo-alt fa-pulse"></i>`
	})
}

function addToCart(slug, url){
	    console.log('adding to cart.')
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'slug':slug})
		})
		.then((response) => {
		    console.log(response)
		    stop_reloading(slug);
		    if (response['url'].includes('login')){
		    iziToast.info({
              title: "Kindly",
              message: "Login first in order to add items to cart.",
              position: 'topRight'
            });
            setTimeout(function () {
             location.href = response['url']
            }, 5200);
            }
//		    if (response['statusText'] != 'OK'){
//		    iziToast.error({
//              title: response['status'],
//              message: response['statusText'],
//              position: 'topRight'
//            });
//            }
		   return response.json();
		})
		.then((data) => {
		    console.log(data)
		    if (data['message']){
                iziToast.success({
                  title: 'Added to cart:',
                  message: data['message'],
                  position: 'topRight'
                });
		    } else if (data['info']){
                iziToast.info({
                  title: 'Not Added to cart:',
                  message: data['info'],
                  position: 'topRight'
                });
		    }
		});
}