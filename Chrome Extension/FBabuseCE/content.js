isON = false

chrome.runtime.onMessage.addListener(function(request){
	isON = request
	console.log(isON)
});

var position = $(window).scrollTop();

$(window).scroll(function() {
  if(isON){
	  	var scroll = $(window).scrollTop();
	  if (scroll > position) {

		posts = document.querySelectorAll('div[data-testid="post_message"]')
		comments = document.querySelectorAll('div[data-testid="UFI2Comment/body"]')
	    
	   
		for (var i = 0; i < posts.length; i++) {
			req(posts[i])
		}

		for (var i = 0; i < comments.length; i++) {
			req(comments[i])
		}

	    position = scroll + 1500;
	  }
  }
  
});


function req(el){
	$.post( "http://127.0.0.1:5000/", {
	    javascript_data: el.innerText}, 
	    function( data ) {
			if (data == 'True'){				
				el.style.backgroundColor = 'grey'
				al = el.querySelectorAll('*')
				for (var i = 0; i < al.length; i++) {
					al[i].style.color = 'grey'
					al[i].style.backgroundColor = 'grey'
				}
			}
	});
}

