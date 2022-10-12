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
            label: 'Sadness',
            data: sadnessScores,
            borderColor: '#9bc4e2',
            backgroundColor: '#9bc4e2',
          },
          {
            label: 'Anger',
            data: angerScores,
            borderColor: '#ea9999',
            backgroundColor: '#ea9999',
          },
          {
            label: 'Fear',
            data: fearScores,
            borderColor: '#974c5e',
            backgroundColor: '#974c5e',
          },
          {
            label: 'Happiness',
            data: happinessScores,
            borderColor: '#f8d664',
            backgroundColor: '#f8d664',
          },
          {
            label: 'Shame',
            data: shameScores,
            borderColor: '#9478a7',
            backgroundColor: '#9478a7',
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 5,
            },
        },
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
            backgroundColor: '#9478a7',
          },
          {
            label: null,
            data: urge2Scores,
            borderColor: '#cc8899',
            backgroundColor: '#cc8899',
          },
          {
            label: null,
            data: urge3Scores,
            borderColor: '#e5aa70',
            backgroundColor: '#e5aa70',
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 5,
            },
        },
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
            label: '# Days Done',
            data: null,
            backgroundColor: '#9bc4e2',
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                min: 0,
                max: 7,
            },
        },
      },
    },
);

const skillsChart = new Chart(
    document.querySelector('#skills-chart'),
    {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Used Skills',
            data: usedSkillsScores,
            borderColor: '#cc8899',
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 7,
            },
        },
      },
    },
);

const valsToNums = (vals) => {
    let count = 0;
    for (const val of vals) {
        if (val === 'yes') {
            count ++
        }
    }
    return count;
};

// Function to get current week's data and update charts with it

const currentDateString = document.querySelector('option').value;

const updateCharts = (dateString) => {
    const queryString = new URLSearchParams(
        {date_string: dateString}).toString();
    const url = `/api/get-given-week?${queryString}`;
    fetch(url)
    .then((res) => res.json())
    .then((resData) => {
        for (let i=0; i<3; i+=1) {
            urgeChart.data.datasets[i].label = resData.urges[i];
        }
        actionChart.data.labels = [resData.actions[0], resData.actions[1]];

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
        usedSkillsScores.length = 0;

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
                usedSkillsScores.push(day['skills used'])

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
                usedSkillsScores.push(null);
            }
        }

        actionChart.data.datasets[0].data = [valsToNums(action1Vals), valsToNums(action2Vals)];

        moodChart.update();
        urgeChart.update();
        actionChart.update();
        skillsChart.update();
    });
};

updateCharts(currentDateString);

// Edit today's entry

const editTodayButton = document.querySelector('#edit-today');
const todayEntryTDs = document.querySelectorAll('.day6');
const editTodayForm = document.querySelector('#edit-today-form');
let clicked = false

if (editTodayButton) {
    editTodayButton.addEventListener('click', () => {
        if (clicked) {
            clicked = false;
            for (const el of todayEntryTDs) {
                el.style.display = '';
            }
            editTodayForm.style.display = 'none';
            editTodayButton.innerHTML = 'Edit Today\'s Entry';
        } else {
            clicked = true;
            for (const el of todayEntryTDs) {
                el.style.display = 'none';
            }
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
            for (const el of todayEntryTDs) {
                el.style.display = '';
            }
            editTodayForm.style.display = 'none';
            editTodayButton.innerHTML = 'Edit Today\'s Entry';
            todayEntryTDs[1]
            .innerHTML = `${resData['sad score']}`;
            todayEntryTDs[2]
            .innerHTML = `${resData['angry score']}`;
            todayEntryTDs[3]
            .innerHTML = `${resData['fear score']}`;
            todayEntryTDs[4]
            .innerHTML = `${resData['happy score']}`;
            todayEntryTDs[5]
            .innerHTML = `${resData['shame score']}`;
            todayEntryTDs[6]
            .innerHTML = `${resData['urge1 score']}`;
            todayEntryTDs[7]
            .innerHTML = `${resData['urge2 score']}`;
            todayEntryTDs[8]
            .innerHTML = `${resData['urge3 score']}`;
            todayEntryTDs[9]
            .innerHTML = `${resData['action1 score']}`;
            todayEntryTDs[10]
            .innerHTML = `${resData['action2 score']}`;
            todayEntryTDs[11]
            .innerHTML = `${resData['skills used']}`;

            updateCharts(currentDateString);
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
    .then((resData) => {
        for (let i=0; i<7; i+=1) {
            const givenDayTDs = document.querySelectorAll(`.day${i}`);
            // const showDate = document.querySelector(
            //     `#day${i} .show-date`);
            // const showSad = document.querySelector(
            //     `#day${i} .show-sad`);
            // const showAngry = document.querySelector(
            //     `#day${i} .show-angry`);
            // const showFear = document.querySelector(
            //     `#day${i} .show-fear`);
            // const showHappy = document.querySelector(
            //     `#day${i} .show-happy`);
            // const showShame = document.querySelector(
            //     `#day${i} .show-shame`);
            // const showUrge1 = document.querySelector(
            //     `#day${i} .show-urge1`);
            // const showUrge2 = document.querySelector(
            //     `#day${i} .show-urge2`);
            // const showUrge3 = document.querySelector(
            //     `#day${i} .show-urge3`);
            // const showAction1 = document.querySelector(
            //     `#day${i} .show-action1`);
            // const showAction2 = document.querySelector(
            //     `#day${i} .show-action2`);
            // const showUsedSkills = document.querySelector(
            //     `#day${i} .show-used-skills`);

            givenDayTDs[0].innerHTML = `${resData.entries[i]['date']}`;

            if (Object.keys(resData.entries[i]).length > 1) {
                givenDayTDs[1].innerHTML = `${resData.entries[i]['sad score']}`;
                givenDayTDs[2].innerHTML = `${resData.entries[i]['angry score']}`;
                givenDayTDs[3].innerHTML = `${resData.entries[i]['fear score']}`;
                givenDayTDs[4].innerHTML = `${resData.entries[i]['happy score']}`;
                givenDayTDs[5].innerHTML = `${resData.entries[i]['shame score']}`;
                givenDayTDs[6].innerHTML = `${resData.entries[i]['urge1 score']}`;
                givenDayTDs[7].innerHTML = `${resData.entries[i]['urge2 score']}`;
                givenDayTDs[8].innerHTML = `${resData.entries[i]['urge3 score']}`;
                givenDayTDs[9].innerHTML = `${resData.entries[i]['action1 score']}`;
                givenDayTDs[10].innerHTML = `${resData.entries[i]['action2 score']}`;
                givenDayTDs[11].innerHTML = `${resData.entries[i]['skills used']}`;

            } else {
                givenDayTDs[1].innerHTML = '&nbsp;';
                givenDayTDs[2].innerHTML = '&nbsp;';
                givenDayTDs[3].innerHTML = '&nbsp;';
                givenDayTDs[4].innerHTML = '&nbsp;';
                givenDayTDs[5].innerHTML = '&nbsp;';
                givenDayTDs[6].innerHTML = `&nbsp;`;
                givenDayTDs[7].innerHTML = `&nbsp;`;
                givenDayTDs[8].innerHTML = `&nbsp;`;
                givenDayTDs[9].innerHTML = `&nbsp;`;
                givenDayTDs[10].innerHTML = `&nbsp;`;
                givenDayTDs[11].innerHTML = '&nbsp;';
            }
        }

        updateCharts(evt.target.value);
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