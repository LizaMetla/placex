const filterBtn = document.querySelector('.filter-btn');
const searchForm = document.querySelector('.search__wrapper');
const costMin = document.querySelector('#id_cost_min');
const costMax = document.querySelector('#id_cost_max');
const costValueMin = document.querySelector('#cost_min_value');
const costValueMax = document.querySelector('#cost_max_value');

// filter bitton
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

// log-in window
const logInBtn = document.querySelector('#log-in-btn');
const logInWindow = document.querySelector('#log-in-window');
const formContainer = document.querySelector('.log-in-form-container');
const closeBtn = document.querySelector('.modal__close');

logInBtn.addEventListener('click', () => {
    if (logInWindow.classList.contains('close')) {
        logInWindow.classList.remove('close');
    }
    if (formContainer.classList.contains('close')) {
        formContainer.classList.remove('close');
    }
});

function closeLogInWindow() {
    logInWindow.classList.add('close');
    formContainer.classList.add('close');
}

closeBtn.addEventListener('click', () => {
    closeLogInWindow();
});

formContainer.addEventListener('click', () => {
    closeLogInWindow();
});