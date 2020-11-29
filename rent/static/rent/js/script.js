const filterBtn = document.querySelector('.filter-btn');
const searchForm = document.querySelector('.search__wrapper');
const costMin = document.querySelector('#id_cost_min');
const costMax = document.querySelector('#id_cost_max');
const costValueMin = document.querySelector('#cost_min_value');
const costValueMax = document.querySelector('#cost_max_value');

filterBtn.addEventListener('click', () => {
    if (searchForm.classList.contains('close')) {
        searchForm.classList.remove('close');
    } else {
        searchForm.classList.add('close');
    }
});

// const costValue = document.createElement('p');

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