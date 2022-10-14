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

// Hide canvases


const moodChartDiv = document.querySelector('#show-mood-chart');
const urgeChartDiv = document.querySelector('#show-urge-chart');
const actionChartDiv = document.querySelector('#show-action-chart');
const SkillsChartDiv = document.querySelector('#show-skills-chart');

urgeChartDiv.style.display = 'none';
actionChartDiv.style.display = 'none';
SkillsChartDiv.style.display = 'none';

// Instantiate empty charts

Chart.defaults.color = '#3b1605';

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
        maintainAspectRatio: false,
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
            label: '',
            data: urge1Scores,
            borderColor: '#8a9a5b',
            backgroundColor: '#9478a7',
          },
          {
            label: '',
            data: urge2Scores,
            borderColor: '#cc8899',
            backgroundColor: '#cc8899',
          },
          {
            label: '',
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
        maintainAspectRatio: false,
      },
    },
);

const actionChart = new Chart(
    document.querySelector('#action-chart'),
    {
      type: 'bar',
      data: {
        labels: ['', ''],
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
        maintainAspectRatio: false,
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
        maintainAspectRatio: false,
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

const namesFromWeek = (week) => {
    let urge1Name = null;
    let urge2Name = null;
    let urge3Name = null;
    let action1Name = null;
    let action2Name = null;
    for (const day of week.entries) {
        if ("sad score" in day) {
            urge1Name = day["urge1 name"];
            urge2Name = day["urge2 name"];
            urge3Name = day["urge3 name"];
            action1Name = day["action1 name"];
            action2Name = day["action2 name"];
            break;
        }
    }
    const names = {
        urge1: urge1Name,
        urge2: urge2Name,
        urge3: urge3Name,
        action1: action1Name,
        action2: action2Name,
    };
    return names;
};

// Function to get current week's data and update charts with it

const currentDateString = document.querySelector('option').value;

const updateWeek = (dateString) => {
    const queryString = new URLSearchParams(
        {date_string: dateString}).toString();
    const url = `/api/get-given-week?${queryString}`;
    fetch(url)
    .then((res) => res.json())
    .then((resData) => {
        const urge1Name = document.querySelector('#urge1-name');
        const urge2Name = document.querySelector('#urge2-name');
        const urge3Name = document.querySelector('#urge3-name');
        const action1Name = document.querySelector('#action1-name');
        const action2Name = document.querySelector('#action2-name');
        const urgeNames = [urge1Name, urge2Name, urge3Name];
        const actionNames = [action1Name, action2Name];

        if (resData.urges) {
            for (let i=0; i<3; i+=1) {
                urgeChart.data.datasets[i].label = resData.urges[i];
                urgeNames[i].innerHTML = resData.urges[i];
            }
            actionChart.data.labels = [resData.actions[0], resData.actions[1]];
            actionNames[0].innerHTML = resData.actions[0];
            actionNames[1].innerHTML = resData.actions[1];
        } else {
            const names = namesFromWeek(resData);
            for (let i=0; i<3; i+=1) {
                urgeChart.data.datasets[i].label = names[`urge${i+1}`];
                urgeNames[i].innerHTML = names[`urge${i+1}`];
            }
            actionChart.data.labels = [names.action1, names.action2];
            actionNames[0].innerHTML = [names.action1];
            actionNames[1].innerHTML = [names.action2];
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
        usedSkillsScores.length = 0;

        for (const day of resData.entries) {
            dates.push(day.date);
            if (day) {
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

        const dateEls = document.querySelectorAll(
            '#table-dates .table-date'
        );

        for (let i=0; i<7; i+=1) {
            dateEls[i].innerHTML = dates[i];
        }

        const sadnessEls = document.querySelectorAll(
            '#table-sadness .table-score'
        );
        const angerEls = document.querySelectorAll(
            '#table-anger .table-score'
        );
        const fearEls = document.querySelectorAll(
            '#table-fear .table-score'
        );
        const happinessEls = document.querySelectorAll(
            '#table-happiness .table-score'
        );
        const shameEls = document.querySelectorAll(
            '#table-shame .table-score'
        );
        const urge1Els = document.querySelectorAll(
            '#table-urge1 .table-score'
        );
        const urge2Els = document.querySelectorAll(
            '#table-urge2 .table-score'
        );
        const urge3Els = document.querySelectorAll(
            '#table-urge3 .table-score'
        );
        const action1Els = document.querySelectorAll(
            '#table-action1 .table-score'
        );
        const action2Els = document.querySelectorAll(
            '#table-action2 .table-score'
        );
        const usedSkillsEls = document.querySelectorAll(
            '#table-used-skills .table-score'
        );

        for (let i=0; i<7; i+=1) {
            if (sadnessScores[i] == null) {
                sadnessEls[i].innerHTML = '&nbsp;';
                angerEls[i].innerHTML = '&nbsp;';
                fearEls[i].innerHTML = '&nbsp;';
                happinessEls[i].innerHTML = '&nbsp;';
                shameEls[i].innerHTML = '&nbsp;';
                urge1Els[i].innerHTML = '&nbsp;';
                urge2Els[i].innerHTML = '&nbsp;';
                urge3Els[i].innerHTML = '&nbsp;';
                action1Els[i].innerHTML = '&nbsp;';
                action2Els[i].innerHTML = '&nbsp;';
                usedSkillsEls[i].innerHTML = '&nbsp;';
            } else {
                sadnessEls[i].innerHTML = sadnessScores[i];
                angerEls[i].innerHTML = angerScores[i];
                fearEls[i].innerHTML = fearScores[i];
                happinessEls[i].innerHTML = happinessScores[i];
                shameEls[i].innerHTML = shameScores[i];
                urge1Els[i].innerHTML = urge1Scores[i];
                urge2Els[i].innerHTML = urge2Scores[i];
                urge3Els[i].innerHTML = urge3Scores[i];
                action1Els[i].innerHTML = action1Vals[i];
                action2Els[i].innerHTML = action2Vals[i];
                usedSkillsEls[i].innerHTML = usedSkillsScores[i];
            }
        }

        actionChart.data.datasets[0].data = [valsToNums(action1Vals), valsToNums(action2Vals)];

        moodChart.update();
        urgeChart.update();
        actionChart.update();
        skillsChart.update();
    });
};

updateWeek(currentDateString);

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

            updateWeek(currentDateString);
        });
    });
}

// View past weeks

const selectWeekMenu = document.querySelector('#select-week');

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

        updateWeek(evt.target.value);
    });
});

// Select chart

const selectChartMenu = document.querySelector('#select-chart');

selectChartMenu.addEventListener('change', (evt) => {
    if (evt.target.value == 'mood-chart') {
        moodChartDiv.style.display = '';
        urgeChartDiv.style.display = 'none';
        actionChartDiv.style.display = 'none';
        SkillsChartDiv.style.display = 'none';
    } else if (evt.target.value == 'urge-chart'){
        moodChartDiv.style.display = 'none';
        urgeChartDiv.style.display = '';
        actionChartDiv.style.display = 'none';
        SkillsChartDiv.style.display = 'none';
    } else if (evt.target.value == 'action-chart') {
        moodChartDiv.style.display = 'none';
        urgeChartDiv.style.display = 'none';
        actionChartDiv.style.display = '';
        SkillsChartDiv.style.display = 'none';
    } else {
        moodChartDiv.style.display = 'none';
        urgeChartDiv.style.display = 'none';
        actionChartDiv.style.display = 'none';
        SkillsChartDiv.style.display = '';
    }
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