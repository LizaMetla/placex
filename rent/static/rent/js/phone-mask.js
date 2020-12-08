// mask for phone
var phone = document.querySelector('#phone');

// phone.onclick = function() {
//     phone.value = "+375";
// }

if (phone) {
  phone.addEventListener('click', () => {
    if (phone.value === '') {
      phone.value = "+375 (";
    }
  });
  
  phone.addEventListener('focus', () => {
    if (phone.value === '') {
      phone.value = "+375 (";
    }
  });
  
  var old = 0;
  
  phone.addEventListener('keyup', (e) => {
    if (e.code !== 'Backspace' && e.code !== 'Delete') {
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
        
      if (curLen > 19)
        phone.value = phone.value.substring(0, 19);
  
      if (phone.value.length !== 19) {
        console.log(phone.value.length)
        phone.setCustomValidity('Номер телефона введен неверно! Пожалуйста, повторите ввод.');
      } else {
        phone.setCustomValidity('');
      }

       old++;
    }
  });
}

// phone.onkeydown = function() {
//     var curLen = phone.value.length;
    
//     if (curLen < old){
//       old--;
//       return;
//     }
    
//     if (curLen == 4) 
//     	phone.value = phone.value + " (";
      
//     if (curLen == 8)
//     	phone.value = phone.value + ") ";
      
//      if (curLen == 13)
//     	phone.value = phone.value + "-"; 
      
//      if (curLen == 16)
//     	phone.value = phone.value + "-";  
      
//      if (curLen > 18)
//     	phone.value = phone.value.substring(0, phone.value.length - 1);
      
//     if (curLen !== 19) {
//       phone.setCustomValidity('Номер телефона введен неверно! Пожалуйста, повторите ввод.');
//     }

//      old++;
// }