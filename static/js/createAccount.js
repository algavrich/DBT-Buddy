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

const createAccountForm = document.querySelector('#create-account-form');

createAccountForm.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const password1 = document.querySelector('#password').value;
    const password2 = document.querySelector('#password-2').value;

    if (password1 === password2) {
        if (password1.match(/[A-Z]/) 
        && password1.match(/[a-z]/) 
        && password1.match(/[0-9]/)
        && password1.match(/[!@#$%\^&\*\(\)-_=\+\[\]\{\}\\\|;:'"\,<\.>\/\?~`]/)
        && password1.length >= 8) {
            const fName = document.querySelector('#fname').value;
            const email = document.querySelector('#email').value;
            const phoneNumber = document.querySelector('#phone-number').value;
            const urge1 = document.querySelector('#urge-1').value;
            const urge2 = document.querySelector('#urge-2').value;
            const urge3 = document.querySelector('#urge-3').value;
            const action1 = document.querySelector('#action-1').value;
            const action2 = document.querySelector('#action-2').value;
            const entryReminderRadios = document.querySelectorAll(
                'input[name="entry-reminders"]');
            let entryReminders = null;
            for (const radio of entryReminderRadios) {
                if (radio.checked) {
                    entryReminders = radio.value;
                }
            }
            const medTrackRadios = document.querySelectorAll(
                'input[name="med-tracking"]');
            let medTracking = null;
            for (const radio of medTrackRadios) {
                if (radio.checked) {
                    medTracking = radio.value;
                }
            }
            const medReminderRadios = document.querySelectorAll(
                'input[name="med-reminders"]');
            let medReminders = null;
            if (medTracking === 'no') {
                medReminders = 'no';
            } else {
                for (const radio of medReminderRadios) {
                    if (radio.checked) {
                        medReminders = radio.value;
                    }
                }
            }
            const formInputs = {
                fname: fName,
                email: email,
                password: password1,
                phone_number: phoneNumber,
                urge1: urge1,
                urge2: urge2,
                urge3: urge3,
                action1: action1,
                action2: action2,
                entry_reminders: entryReminders,
                med_tracking: medTracking,
                med_reminders: medReminders,
            };
            console.log(formInputs);
            fetch('/api/create-account', {
                method: 'POST',
                body: JSON.stringify(formInputs),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then((res) => res.json())
            .then((resData) => {
                if (resData.success === true) {
                    window.location.href = "/";
                } else {
                    window.location.href = "/create-account";
                }
            });
        } else {
            alert('Password doesn\'t meet requirements');
        }
    } else {
        alert('Password doesn\'t match');
    }
});