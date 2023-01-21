// Onclick of the button
document.querySelector("button").onclick = function () {  
    eel.setup()(function(){                      
      // Update the div with a random number returned by python
      document.querySelector(".random_number").innerHTML = 10;
    })
  }