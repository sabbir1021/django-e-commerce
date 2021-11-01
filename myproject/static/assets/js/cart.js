// cart js

var updatebtns = document.getElementsByClassName('update-cart')

for (var i=0; i < updatebtns.length; i++) {
    updatebtns[i].addEventListener('click', function(){
        var productId = this.dataset.product 
        var action = this.dataset.action
        console.log('productId:',productId,'Action:',action)
        console.log('User:',user)
        if(user === "AnonymousUser"){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId,action){
    console.log('user is logged in, send data..')
    var url = '/cart/update_item/'
    
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('date:', data)
        location.reload()
    })
}

// cart js end


