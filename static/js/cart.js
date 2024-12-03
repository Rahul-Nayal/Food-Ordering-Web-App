var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0; i<updateBtns.length ; i++){
	updateBtns[i].addEventListener('click',function(){
		var dishId = this.dataset.dish
		var action = this.dataset.action
		console.log('dishId:' , dishId , 'action : ',action )
		console.log('User : ',user)

		if (user == 'AnonymousUser'){
			console.log('Not logged in')
		}
		else{
			updateUserOrder(dishId,action)
		}
	})
}

function updateUserOrder(dishId,action){
	console.log('user is authenticated ,sending data...')

	var url = '/update_item/'
	console.log('URL : ',url)
	fetch (url,{
		method:'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'dishId': dishId, 'action': action})
	})
	.then((response)=>{
		return response.json();
	})

	.then((data)=>{
		location.reload()
	})

}