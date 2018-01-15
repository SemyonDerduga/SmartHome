'use strict';

const recalcPrice = () => {
    const priceElement = document.getElementById('price');
    let totalPrice = 0;

    for (let product of document.getElementsByClassName('product')) {
        const countElement = product.getElementsByClassName('count')[0];
        const count = parseInt(countElement.value);
        const priceElement = product.getElementsByClassName('price')[0];
        const price = parseFloat(priceElement.innerHTML.replace(',', '.'));

        totalPrice += count * price;
    }

    priceElement.innerHTML = `${totalPrice}₽`;
};

for (let countElement of document.getElementsByClassName('count')) {
    countElement.addEventListener('change', recalcPrice);
}
recalcPrice();