
console.log("Apply for training.")
var applyBtns = $('.apply-btn')
function stop_reloading(slug) {
  $('#'+slug).html(`<i class="fe fe-book"></i> Apply`);
}
for (i = 0; i < applyBtns.length; i++) {
	applyBtns[i].addEventListener('click', function(){
		var slug = this.dataset.slug
		var url = this.dataset.url
		console.log('Slug:', slug)
        ApplyForTraining(slug, url)
        console.log(this)
        this.innerHTML = `<i class="fas fa-redo-alt fa-pulse"></i>`
	})
}

function ApplyForTraining(slug, url){
	    console.log('applying ...')
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
		   return response.json();
		})
		.then((data) => {
		    console.log(data)
		    if (data['message']){
                iziToast.success({
                  title: 'Applied:',
                  message: data['message'],
                  position: 'topRight'
                });
		    } else if (data['info']){
                iziToast.info({
                  title: 'Not Applied:',
                  message: data['info'],
                  position: 'topRight'
                });
		    }
		});
}