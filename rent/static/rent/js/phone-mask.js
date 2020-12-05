// mask for phone
var phone = document.querySelector('#phone');

phone.onclick = function() {
    phone.value = "+375";
}

var old = 0;

phone.onkeydown = function() {
    var curLen = phone.value.length;
    
    if (curLen < old){
      old--;
      return;
    }
    
    if (curLen == 4) 
    	phone.value = phone.value + " (";
      
    if (curLen == 8)
    	phone.value = phone.value + ") ";
      
     if (curLen == 13)
    	phone.value = phone.value + "-"; 
      
     if (curLen == 16)
    	phone.value = phone.value + "-";  
      
     if (curLen > 18)
    	phone.value = phone.value.substring(0, phone.value.length - 1);
      
     old++;
}