'use strict';

const editTodayButton = document.querySelector('#edit-today');
const todayEntry = document.querySelector('.diary-day');
const editTodayForm = document.querySelector('#edit-today-form');
let clicked = false

editTodayButton.addEventListener('click', () => {
    if (clicked) {
        clicked = false;
        todayEntry.style.display = 'block';
        editTodayForm.style.display = 'none';
        editTodayButton.innerHTML = 'Edit Today\'s Entry';
    } else {
        clicked = true;
        todayEntry.style.display = 'none';
        editTodayForm.style.display = 'inline-block';
        editTodayButton.innerHTML = 'Cancel';
    }
});