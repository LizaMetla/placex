// mask for phone
var phone = document.querySelector('#phone');

if (phone) {
  phone.addEventListener('focus', () => {
    if (phone.value === '') {
      phone.value = "+375 (";
    }
  });
  
  var old = 0;
  
  phone.addEventListener('keyup', (e) => {
    var curLen = phone.value.length;
    if (e.code !== 'Backspace' && e.code !== 'Delete') {
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

       old++;
    }

    if (curLen !== 19) {
      phone.setCustomValidity('Номер телефона введен неверно! Пожалуйста, повторите ввод.');
    } else {
      phone.setCustomValidity('');
    }
  });
}
