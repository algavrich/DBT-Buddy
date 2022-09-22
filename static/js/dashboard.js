'use strict';

// Need to edit this file to conform to Airbnb style guide

// Edit today's entry

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

    const action1Buttons = document.querySelectorAll(
        'input[name="action-1"]');
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
        document.querySelector('#day6 .show-sad')
        .innerHTML = `Sadness: ${formInputs.sad_score}`;
        document.querySelector('#day6 .show-angry')
        .innerHTML = `Anger: ${formInputs.angry_score}`;
        document.querySelector('#day6 .show-fear')
        .innerHTML = `Fear: ${formInputs.fear_score}`;
        document.querySelector('#day6 .show-happy')
        .innerHTML = `Happiness: ${formInputs.happy_score}`;
        document.querySelector('#day6 .show-shame')
        .innerHTML = `Shame: ${formInputs.shame_score}`;
        document.querySelector('#day6 .show-urge1 span')
        .innerHTML = `${formInputs.urge1_score}`;
        document.querySelector('#day6 .show-urge2 span')
        .innerHTML = `${formInputs.urge2_score}`;
        document.querySelector('#day6 .show-urge3 span')
        .innerHTML = `${formInputs.urge3_score}`;
        document.querySelector('#day6 .show-action1 span')
        .innerHTML = `${formInputs.action1_score}`;
        document.querySelector('#day6 .show-action2 span')
        .innerHTML = `${formInputs.action2_score}`;
        document.querySelector('#day6 .show-used-skills')
        .innerHTML = `Used Skills: ${formInputs.used_skills}`;
    });
});

// View past weeks

const selectWeekMenu = document.querySelector('#select-week')
const diaryDays = document.querySelectorAll('.diary-day')

selectWeekMenu.addEventListener('change', (evt) => {
    evt.preventDefault();
    
    const queryString = new URLSearchParams({date_string: evt.target.value}).toString();
    const url = `/api/get-given-week?${queryString}`;
    fetch(url)
    .then((res) => res.json())
    .then((resData) =>{
        for (let i=0; i<7; i+=1) {
            const showDate = document.querySelector(
                `#day${i} .show-date`);
            const showSad = document.querySelector(
                `#day${i} .show-sad span`);
            const showAngry = document.querySelector(
                `#day${i} .show-angry span`);
            const showFear = document.querySelector(
                `#day${i} .show-fear span`);
            const showHappy = document.querySelector(
                `#day${i} .show-happy span`);
            const showShame = document.querySelector(
                `#day${i} .show-shame span`);
            const showUrge1 = document.querySelector(
                `#day${i} .show-urge1 span`);
            const showUrge2 = document.querySelector(
                `#day${i} .show-urge2 span`);
            const showUrge3 = document.querySelector(
                `#day${i} .show-urge3 span`);
            const showAction1 = document.querySelector(
                `#day${i} .show-action1 span`);
            const showAction2 = document.querySelector(
                `#day${i} .show-action2 span`);
            const showUsedSkills = document.querySelector(
                `#day${i} .show-used-skills span`);

            if (resData[i] !== null) {
                showDate.innerHTML = `${resData[i]['date']}`;
                showSad.innerHTML = `${resData[i]['sad score']}`;
                showAngry.innerHTML = `${resData[i]['angry score']}`;
                showFear.innerHTML = `${resData[i]['fear score']}`;
                showHappy
                .innerHTML = `${resData[i]['happy score']}`;
                showShame.innerHTML = `${resData[i]['shame score']}`;
                showUrge1.innerHTML = `${resData[i]['urge1 score']}`;
                showUrge2.innerHTML = `${resData[i]['urge2 score']}`;
                showUrge3.innerHTML = `${resData[i]['urge3 score']}`;
                showAction1.innerHTML = `${resData[i]['action1 score']}`;
                showAction2.innerHTML = `${resData[i]['action2 score']}`;
                showUsedSkills
                .innerHTML = `${resData[i]['skills used']}`;
            } else {
                showDate.innerHTML = '<h4>No Entry</h4>';
                showSad.innerHTML = '';
                showAngry.innerHTML = '';
                showFear.innerHTML = '';
                showHappy.innerHTML = '';
                showShame.innerHTML = '';
                showUrge1.innerHTML = ``;
                showUrge2.innerHTML = ``;
                showUrge3.innerHTML = ``;
                showAction1.innerHTML = ``;
                showAction2.innerHTML = ``;
                showUsedSkills.innerHTML = '';
            }
        }
    });
});