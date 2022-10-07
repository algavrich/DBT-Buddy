'use strict';

// Need to edit this file to conform to Airbnb style guide

// Declare empty constants for chart data

const dates = [];
const sadnessScores = [];
const angerScores = [];
const fearScores = [];
const happinessScores = [];
const shameScores = [];

const urge1Scores = [];
const urge2Scores = [];
const urge3Scores = [];

const action1Vals = [];
const action2Vals = [];
let action1Yes = 0;
let action2Yes = 0;

const usedSkillsScores = [];

// Instantiate empty charts

const moodChart = new Chart(
    document.querySelector('#mood-chart'),
    {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'sadness',
            data: sadnessScores,
            borderColor: '#9bc4e2',
          },
          {
            label: 'anger',
            data: angerScores,
            borderColor: '#ea9999',
          },
          {
            label: 'fear',
            data: fearScores,
            borderColor: '#974c5e',
          },
          {
            label: 'happiness',
            data: happinessScores,
            borderColor: '#f8d664',
          },
          {
            label: 'shame',
            data: shameScores,
            borderColor: '#9478a7',
          },
        ],
      },
      options: {
        responsive: true
      },
    },
);

const urgeChart = new Chart(
    document.querySelector('#urge-chart'),
    {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: null,
            data: urge1Scores,
            borderColor: '#8a9a5b',
          },
          {
            label: null,
            data: urge2Scores,
            borderColor: '#cc8899',
          },
          {
            label: null,
            data: urge3Scores,
            borderColor: '#e5aa70',
          },
        ],
      },
      options: {
        responsive: true
      },
    },
);

const actionChart = new Chart(
    document.querySelector('#action-chart'),
    {
      type: 'bar',
      data: {
        labels: null,
        datasets: [
          {
            label: '# days done',
            data: null,
            backgroundColor: '#9bc4e2',
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
      },
    },
);

// Function to get current week's data and update charts with it

const updateCharts = () => {
    const currentDateString = document.querySelector('option').value;
    const queryString = new URLSearchParams(
        {date_string: currentDateString}).toString();
    const url = `/api/get-given-week?${queryString}`;
    fetch(url)
    .then((res) => res.json())
    .then((resData) => {
        if (resData.urges) {
            for (let i=0; i<3; i+=1) {
                urgeChart.data.datasets[i].label = resData.urges[i];
            }
        } else {
            for (let i=0; i<3; i+=1) {
                const iString = new String(i+1);
                urgeChart.data.datasets[i].label = resData[entries][0][`urge${iString} name`];
            }
        }
        if (resData.actions) {
            actionChart.data.labels = [resData.actions[0], resData.actions[1]]
        } else {
            actionChart.data.labels = [
                resData.entries[0][`action1 name`],
                resData.entries[0][`action2 name`]
            ];
        }

        dates.length = 0;
        sadnessScores.length = 0;
        angerScores.length = 0;
        fearScores.length = 0;
        happinessScores.length = 0;
        shameScores.length = 0;
        urge1Scores.length = 0;
        urge2Scores.length = 0;
        urge3Scores.length = 0;
        action1Vals.length = 0;
        action2Vals.length = 0;

        for (const day of resData.entries) {
            if (day) {
                dates.push(day.date);
                sadnessScores.push(day['sad score']);
                angerScores.push(day['angry score']);
                fearScores.push(day['fear score']);
                happinessScores.push(day['happy score']);
                shameScores.push(day['shame score']);
                urge1Scores.push(day['urge1 score']);
                urge2Scores.push(day['urge2 score']);
                urge3Scores.push(day['urge3 score']);
                action1Vals.push(day['action1 score']);
                action2Vals.push(day['action2 score']);

            } else {
                dates.push('no entry');
                sadnessScores.push(null);
                angerScores.push(null);
                fearScores.push(null);
                happinessScores.push(null);
                shameScores.push(null);
                urge1Scores.push(null);
                urge2Scores.push(null);
                urge3Scores.push(null);
                action1Vals.push(null);
                action2Vals.push(null);
            }
        }
        
        const valsToNums = (vals) => {
            let count = 0;
            for (const val of vals) {
                if (val === 'yes') {
                    count ++
                }
            }
            return count;
        };

        actionChart.data.datasets[0].data = [valsToNums(action1Vals), valsToNums(action2Vals)];

        moodChart.update();
        urgeChart.update();
        actionChart.update();
    });
};

updateCharts();

// Edit today's entry

const editTodayButton = document.querySelector('#edit-today');
const todayEntry = document.querySelector('#day6');
const editTodayForm = document.querySelector('#edit-today-form');
let clicked = false

if (editTodayButton) {
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
            updateCharts();
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
        const newSadnessScores = [];
        const newAngerScores = [];
        const newFearScores = [];
        const newHappinessScores = [];
        const newShameScores =[];

        const newUrge1Scores = [];
        const newUrge2Scores = [];
        const newUrge3Scores = [];

        for (let i=0; i<3; i+=1) {
            const iString = new String(i+1);
            urgeChart.data.datasets[i].label = resData[0][`urge${iString} name`];
        }

        for (const day of resData) {
            if (day) {
                newDates.push(day.date);
                newSadnessScores.push(day['sad score']);
                newAngerScores.push(day['angry score']);
                newFearScores.push(day['fear score']);
                newHappinessScores.push(day['happy score']);
                newShameScores.push(day['shame score']);
                newUrge1Scores.push(day['urge1 score']);
                newUrge2Scores.push(day['urge2 score']);
                newUrge3Scores.push(day['urge3 score']);

            } else {
                newDates.push('no entry');
                newSadnessScores.push(null);
                newAngerScores.push(null);
                newFearScores.push(null);
                newHappinessScores.push(null);
                newShameScores.push(null);
                newUrge1Scores.push(null);
                newUrge2Scores.push(null);
                newUrge3Scores.push(null);
            }
        }

        moodChart.data.labels = newDates;
        moodChart.data.datasets[0].data = newSadnessScores;
        moodChart.data.datasets[1].data = newAngerScores;
        moodChart.data.datasets[2].data = newFearScores;
        moodChart.data.datasets[3].data = newHappinessScores;
        moodChart.data.datasets[4].data = newShameScores;
        moodChart.update();

        urgeChart.data.labels = newDates;
        urgeChart.data.datasets[0].data = newUrge1Scores;
        urgeChart.data.datasets[1].data = newUrge2Scores;
        urgeChart.data.datasets[2].data = newUrge3Scores;
        urgeChart.update();
    });
});

// Handle med entry click

const medEntryButton = document.querySelector('#make-med-entry');

if (medEntryButton) {
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
}

