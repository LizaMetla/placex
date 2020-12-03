const filterBtn = document.querySelector('.filter-btn');
const searchForm = document.querySelector('.search__wrapper');
const costMin = document.querySelector('#id_cost_min');
const costMax = document.querySelector('#id_cost_max');
const costValueMin = document.querySelector('#cost_min_value');
const costValueMax = document.querySelector('#cost_max_value');

// filter bitton
if (filterBtn) {
    filterBtn.addEventListener('click', () => {
        if (searchForm.classList.contains('close')) {
            searchForm.classList.remove('close');
        } else {
            searchForm.classList.add('close');
        }
    });


    // render costs
    function inputRange(cost, selector) {
        selector.textContent = cost;
    }

    costMin.addEventListener('input', () => {
        inputRange(costMin.value, costValueMin);
    });

    costMax.addEventListener('input', () => {
        inputRange(costMax.value, costValueMax);
    });

    inputRange(costMin.value, costValueMin);
    inputRange(costMax.value, costValueMax);
}

// log-in window
const logInBtn = document.querySelector('#log-in-btn');
const logInWindow = document.querySelector('#log-in-window');
const formContainer = document.querySelector('.log-in-form-container');
const closeBtn = document.querySelector('.modal__close');

if (logInBtn) {
    logInBtn.addEventListener('click', () => {
        document.body.style.overflow = 'hidden';
        if (logInWindow.classList.contains('close')) {
            logInWindow.classList.remove('close');
        }
        if (formContainer.classList.contains('close')) {
            formContainer.classList.remove('close');
        }
    });
}

function closeLogInWindow() {
    logInWindow.classList.add('close');
    formContainer.classList.add('close');
}

closeBtn.addEventListener('click', () => {
    closeLogInWindow();
});

formContainer.addEventListener('click', (e) => {
    if (e.target === formContainer) {
        closeLogInWindow();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.code === 'Escape') {
        closeLogInWindow();
    }
});

// add photo in registration

$('#add-reg-photo').click(function() {$('#add__log-in-img').trigger('click')});

function previewFile(input){
    var file = $("input[id='add__log-in-img']").get(0).files[0];

    if(file){
        var reader = new FileReader();

        reader.onload = function(){
            $("#add-reg-photo").attr("src", reader.result);
            console.log(reader.result);
        }

        reader.readAsDataURL(file);
    }
}

// open modal window if user not autorised (add announcement)
const logInForm = document.querySelector('#log-in-form');

function autorisationInAddingAnnounce(autorisation, url) {
    console.log(url);
    if (!autorisation) {
        console.log(logInForm.action);
        logInForm.action = `${logInForm.action}?next=${url}`;
        console.log(logInForm.action);
        formContainer.classList.remove('close');
        logInWindow.classList.remove('close');
    } else {
        location.assign(url);
    }
}

// error in validation

function logInValidation(err) {
    if (err !== '') {
        const p = document.createElement('p');
        p.textContent = 'Логин или пароль введены неверно!';
        p.setAttribute('class', 'validation-error')
        document.querySelector('#log-in-password').after(p);
    }
}

logInValidation('');

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