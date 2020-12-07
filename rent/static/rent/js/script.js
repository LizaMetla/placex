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

function autorisationInAddingAnnounce(autorisation, url, baseUrl) {
    if (!autorisation) {
        logInForm.action = `${baseUrl}?next=${url}`;
        formContainer.classList.remove('close');
        logInWindow.classList.remove('close');
    } else {
        location.assign(url);
    }
}

// error in validation

function logInValidation() {

    const err = document.querySelector('#v-login-errors').value;

    if (err !== '') {
        const p = document.createElement('p');
        p.textContent = 'Логин или пароль введены неверно!';
        p.setAttribute('class', 'validation-error')
        document.querySelector('#log-in-password').after(p);
        $("#log-in-btn").click();
    }
}

logInValidation();

// slider
function sliderFunc(arrImages) {
    const imageinSlider = document.querySelector('img.mfp-img');
    const sliderImg = imageinSlider.parentElement;
    
    const divPrev = document.createElement('div');
    divPrev.setAttribute('class', 'prevSlider');
    sliderImg.before(divPrev);   
    
    const divNext = document.createElement('div');
    divNext.setAttribute('class', 'nextSlider');
    sliderImg.after(divNext);

    const prevArrow = document.createElement('i');
    const nextArrow = document.createElement('i');
    function addArrowIcon(selector, element, className) {
        element.setAttribute('class', `fa ${className} fa-5x`);
        selector.append(element);
    }
    addArrowIcon(divPrev, prevArrow, 'fa-arrow-left');
    addArrowIcon(divNext, nextArrow, 'fa-arrow-right');
    
    function addActions(element) {
        element.addEventListener('mouseenter', () => {
            element.style.opacity = '.2';
        });
        element.addEventListener('mouseleave', () => {
            element.style.opacity = '.1';
        });
    }
    addActions(divPrev);
    addActions(divNext);

    let sliderIndex = 1;

    for (let i = 0; i < arrImages.length; i++) {
        if (imageinSlider.src.slice(21) === arrImages[i]) {
            sliderIndex = i + 1;
        }
    }

    function sliderWork(images) {
        const prev = document.querySelector('.prevSlider');
        const next = document.querySelector('.nextSlider');

        function showSlides(n) {
            if (n > images.length) {
                sliderIndex = 1;
            }

            if (n < 1) {
                sliderIndex = images.length;
            }

            imageinSlider.src = `${imageinSlider.src.slice(0, 21)}${images[sliderIndex - 1]}`;
        }

        showSlides(sliderIndex);

        function plusSlides(n) {
            showSlides(sliderIndex += n);
        }

        prev.addEventListener('click', () => {
            plusSlides(-1);
        });

        document.addEventListener('keydown', (e) => {
            if (e.code === 'ArrowLeft') {
                plusSlides(-1);
            }
        });

        next.addEventListener('click', () => {
            plusSlides(1);
        });

        document.addEventListener('keydown', (e) => {
            if (e.code === 'ArrowRight') {
                plusSlides(1);
            }
        });
    }
    sliderWork(arrImages);
}

//
$(document).ready(function () {
    var urlblock = $('#code');
    urlblock.focus(function () {
        urlblock.select();
    });
    $('#v-copy-btn').click(function () {
        urlblock.select();
        document.execCommand("copy");
    });
});