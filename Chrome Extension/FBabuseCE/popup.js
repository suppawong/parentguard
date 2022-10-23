btn = document.querySelector('button')
var isON
if(isON){
	btn.style.backgroundColor = 'green'	
}else{
	btn.style.backgroundColor = 'red'
}
document.addEventListener('DOMContentLoaded', function () {
	document.querySelector('button').addEventListener('click', onclick, false)

	function onclick(){
		chrome.tabs.query({currentWindow: true, active: true}, 
			function (tabs){

				if(isON){
					isON = false
				}else{
					isON = true
				}

				if(isON){
					btn.style.backgroundColor = 'green'	
				}else{
					btn.style.backgroundColor = 'red'
				}
				chrome.tabs.sendMessage(tabs[0].id, isON)
		})
	}
}, false)