'use strict';

const medTrack = document.querySelector('#med-track');
const yesButton = document.querySelector('#m-track-yes');
const noButton = document.querySelector('#m-track-no');
const medReminders = document.querySelector('#show-med-rem');

medTrack.addEventListener('click', (evt) => {
    if (evt.target === yesButton) {
        medReminders.style.display = 'block';
    } else if (evt.target === noButton) {
        medReminders.style.display = 'none';
    }
});