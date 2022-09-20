'use strict';

const editTodayButton = document.querySelector('#edit-today');
const todayEntry = document.querySelector('#day6');
const editTodayForm = document.querySelector('#edit-today-form');
let clicked = false

editTodayButton.addEventListener('click', () => {
    if (clicked) {
        clicked = false;
        todayEntry.style.display = 'inline-block';
        editTodayForm.style.display = 'none';
        editTodayButton.innerHTML = 'Edit Today\'s Entry';
    } else {
        clicked = true;
        todayEntry.style.display = 'none';
        editTodayForm.style.display = 'inline-block';
        editTodayButton.innerHTML = 'Cancel';
    }
});

editTodayForm.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const action1Buttons = document.querySelectorAll('input[name="action-1"]');
    let action1 = null;
    for (const button of action1Buttons) {
        if (button.checked) {
            action1 = button.value;
            break;
        }
    }

    const action2Buttons = document.querySelectorAll('input[name="action-2"]');
    let action2 = null;
    for (const button of action2Buttons) {
        if (button.checked) {
            action2 = button.value;
            break;
        }
    }

    const formInputs = {
        sad_score: document.querySelector('#sad').value,
        angry_score: document.querySelector('#angry').value,
        fear_score: document.querySelector('#fear').value,
        happy_score: document.querySelector('#happy').value,
        shame_score: document.querySelector('#shame').value,
        urge1_score: document.querySelector('#urge-1').value,
        urge2_score: document.querySelector('#urge-2').value,
        urge3_score: document.querySelector('#urge-3').value,
        action1_score: action1,
        action2_score: action2,
        used_skills: document.querySelector('#used-skills').value,
    };

    fetch('/api/update-today-entry', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((res) => res.json())
    .then((resData) => {
        alert(resData.status);
        clicked = false;
        todayEntry.style.display = 'inline-block';
        editTodayForm.style.display = 'none';
        editTodayButton.innerHTML = 'Edit Today\'s Entry';
        document.querySelector('#day6 .show-sad').innerHTML = `Sadness: ${formInputs.sad_score}`;
        document.querySelector('#day6 .show-angry').innerHTML = `Anger: ${formInputs.angry_score}`;
        document.querySelector('#day6 .show-fear').innerHTML = `Fear: ${formInputs.fear_score}`;
        document.querySelector('#day6 .show-happy').innerHTML = `Happiness: ${formInputs.happy_score}`;
        document.querySelector('#day6 .show-shame').innerHTML = `Shame: ${formInputs.shame_score}`;
        document.querySelector('#day6 .show-urge1 span').innerHTML = `${formInputs.urge1_score}`;
        document.querySelector('#day6 .show-urge2 span').innerHTML = `${formInputs.urge2_score}`;
        document.querySelector('#day6 .show-urge3 span').innerHTML = `${formInputs.urge3_score}`;
        document.querySelector('#day6 .show-action1 span').innerHTML = `${formInputs.action1_score}`;
        document.querySelector('#day6 .show-action2 span').innerHTML = `${formInputs.action2_score}`;
        document.querySelector('#day6 .show-used-skills').innerHTML = `Used Skills: ${formInputs.used_skills}`;
    });
});