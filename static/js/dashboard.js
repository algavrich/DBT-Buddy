'use strict';

// Need to edit this file to conform to Airbnb style guide

// Render chart(s) on (re)load

const dates = [];
const sadness = [];
const anger = [];
const fear = [];
const happiness = [];
const shame =[];

const currentDateString = document.querySelector('option').value;
const queryString = new URLSearchParams(
    {date_string: currentDateString}).toString();
const url = `/api/get-given-week?${queryString}`;
fetch(url)
.then((res) => res.json())
.then((resData) => {
    //
    for (const day of resData) {
        if (day) {
            dates.push(day.date);
            sadness.push(day['sad score']);
            anger.push(day['angry score']);
            fear.push(day['fear score']);
            happiness.push(day['happy score']);
            shame.push(day['shame score']);
        } else {
            dates.push('no entry');
            sadness.push(null);
            anger.push(null);
            fear.push(null);
            happiness.push(null);
            shame.push(null);
        }
    }
    moodChart.update();
});

const moodChart = new Chart(
    document.querySelector('#mood-chart'),
    {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'sadness',
            data: sadness,
            borderColor: '#1236a3',
          },
          {
            label: 'anger',
            data: anger,
            borderColor: '#b82f2f',
          },
          {
            label: 'fear',
            data: fear,
            borderColor: '#630d24',
          },
          {
            label: 'happiness',
            data: happiness,
            borderColor: '#ff9a55',
          },
          {
            label: 'shame',
            data: shame,
            borderColor: '#9478a7',
          },
        ],
      },
    },
);

// Edit today's entry

const editTodayButton = document.querySelector('#edit-today');
const todayEntry = document.querySelector('#day6');
const editTodayForm = document.querySelector('#edit-today-form');
let clicked = false

if (editTodayButton != null) {
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
    
        const action2Buttons = document.querySelectorAll(
            'input[name="action-2"]');
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
            method: 'PUT',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((res) => res.json())
        .then((resData) => {
            clicked = false;
            todayEntry.style.display = 'inline-block';
            editTodayForm.style.display = 'none';
            editTodayButton.innerHTML = 'Edit Today\'s Entry';
            document.querySelector('#day6 .show-sad')
            .innerHTML = `Sadness: ${resData['sad score']}`;
            document.querySelector('#day6 .show-angry')
            .innerHTML = `Anger: ${resData['angry score']}`;
            document.querySelector('#day6 .show-fear')
            .innerHTML = `Fear: ${resData['fear score']}`;
            document.querySelector('#day6 .show-happy')
            .innerHTML = `Happiness: ${resData['happy score']}`;
            document.querySelector('#day6 .show-shame')
            .innerHTML = `Shame: ${resData['shame score']}`;
            document.querySelector('#day6 .show-urge1')
            .innerHTML = `${resData['urge1 name']}: 
                ${resData['urge1 score']}`;
            document.querySelector('#day6 .show-urge2')
            .innerHTML = `${resData['urge2 name']}: 
                ${resData['urge2 score']}`;
            document.querySelector('#day6 .show-urge3')
            .innerHTML = `${resData['urge3 name']}: 
                ${resData['urge3 score']}`;
            document.querySelector('#day6 .show-action1')
            .innerHTML = `${resData['action1 name']}: 
                ${resData['action1 score']}`;
            document.querySelector('#day6 .show-action2')
            .innerHTML = `${resData['action2 name']}: 
                ${resData['action2 score']}`;
            document.querySelector('#day6 .show-used-skills')
            .innerHTML = `Used Skills: ${resData['skills used']}`;
        });
    });
}

// View past weeks

const selectWeekMenu = document.querySelector('#select-week')
const diaryDays = document.querySelectorAll('.diary-day')

selectWeekMenu.addEventListener('change', (evt) => {
    evt.preventDefault();
    
    const queryString = new URLSearchParams(
        {date_string: evt.target.value}).toString();
    const url = `/api/get-given-week?${queryString}`;
    fetch(url)
    .then((res) => res.json())
    .then((resData) =>{
        for (let i=0; i<7; i+=1) {
            const showDate = document.querySelector(
                `#day${i} .show-date`);
            const showSad = document.querySelector(
                `#day${i} .show-sad`);
            const showAngry = document.querySelector(
                `#day${i} .show-angry`);
            const showFear = document.querySelector(
                `#day${i} .show-fear`);
            const showHappy = document.querySelector(
                `#day${i} .show-happy`);
            const showShame = document.querySelector(
                `#day${i} .show-shame`);
            const showUrge1 = document.querySelector(
                `#day${i} .show-urge1`);
            const showUrge2 = document.querySelector(
                `#day${i} .show-urge2`);
            const showUrge3 = document.querySelector(
                `#day${i} .show-urge3`);
            const showAction1 = document.querySelector(
                `#day${i} .show-action1`);
            const showAction2 = document.querySelector(
                `#day${i} .show-action2`);
            const showUsedSkills = document.querySelector(
                `#day${i} .show-used-skills`);

            if (resData[i] !== null) {
                showDate.innerHTML = `${resData[i]['date']}`;
                showSad.innerHTML = `Sadness: ${resData[i]['sad score']}`;
                showAngry.innerHTML = `Anger: ${resData[i]['angry score']}`;
                showFear.innerHTML = `Fear: ${resData[i]['fear score']}`;
                showHappy.innerHTML = `Happiness: 
                    ${resData[i]['happy score']}`;
                showShame.innerHTML = `Shame: ${resData[i]['shame score']}`;
                showUrge1.innerHTML = `${resData[i]['urge1 name']}: 
                    ${resData[i]['urge1 score']}`;
                showUrge2.innerHTML = `${resData[i]['urge2 name']}: 
                    ${resData[i]['urge2 score']}`;
                showUrge3.innerHTML = `${resData[i]['urge3 name']}: 
                    ${resData[i]['urge3 score']}`;
                showAction1.innerHTML = `${resData[i]['action1 name']}: 
                    ${resData[i]['action1 score']}`;
                showAction2.innerHTML = `${resData[i]['action2 name']}: 
                    ${resData[i]['action2 score']}`;
                showUsedSkills.innerHTML = `Used Skills: 
                    ${resData[i]['skills used']}`;
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
        const newDates = [];
        const newSadness = [];
        const newAnger = [];
        const newFear = [];
        const newHappiness = [];
        const newShame =[];
        for (const day of resData) {
            if (day) {
                newDates.push(day.date);
                newSadness.push(day['sad score']);
                newAnger.push(day['angry score']);
                newFear.push(day['fear score']);
                newHappiness.push(day['happy score']);
                newShame.push(day['shame score']);
            } else {
                newDates.push('no entry');
                newSadness.push(null);
                newAnger.push(null);
                newFear.push(null);
                newHappiness.push(null);
                newShame.push(null);
            }
        }
        moodChart.data.labels = newDates;
        moodChart.data.datasets[0].data = newSadness;
        moodChart.data.datasets[1].data = newAnger;
        moodChart.data.datasets[2].data = newFear;
        moodChart.data.datasets[3].data = newHappiness;
        moodChart.data.datasets[4].data = newShame;
        moodChart.update();

    });
});

const medEntryButton = document.querySelector('#make-med-entry');

medEntryButton.addEventListener('click', () => {
    fetch('/api/new-med-entry', {
        method: 'POST',
    })
    .then((res) => res.json())
    .then((resData) => {
        if (resData.success) {
            document.querySelector('#med-status h4')
            .innerHTML = 'You already took your medication today';
            medEntryButton.style.display = 'none';
        }
    });
});

