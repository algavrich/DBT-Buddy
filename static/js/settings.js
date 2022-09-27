'use strict';

// DRYer???

const textPrefPs = document.querySelectorAll('.text-pref');

 for (const textPrefP of textPrefPs) {
    textPrefP.addEventListener('click', (evt) => {
        const inputField = evt.target.parentElement.querySelector('input');
        if (inputField.style.display !== 'inline-block') {
            inputField.style.display = 'inline-block';
            evt.target.style.display = 'none';
            document.querySelector('#submit-button input').style.display = 'block';
        }
    });
}

const radioPrefPs = document.querySelectorAll('.radio-pref');

 for (const radioPrefP of radioPrefPs) {
    radioPrefP.addEventListener('click', (evt) => {
        // maybe wrap fields and labels in divs to target both at once
        const inputFields = evt.target.parentElement.querySelectorAll('input');
        const labels = evt.target.parentElement.querySelectorAll('label');
        for (let i=0; i<2; i+=1) {
            if (inputFields[i].style.display !== 'inline-block') {
                inputFields[i].style.display = 'inline-block';
                labels[i].style.display = 'inline-block';
                evt.target.style.display = 'none';
                document.querySelector('#submit-button input').style.display = 'block';
            }
        }
    });
}

document.querySelector('#preferences form')
.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const fName = document.querySelector('#fname-input').value;
    const email = document.querySelector('#email-input').value;
    const phoneNumber = document.querySelector('#phone-number-input').value;
    const urge1 = document.querySelector('#urge-1-input').value;
    const urge2 = document.querySelector('#urge-2-input').value;
    const urge3 = document.querySelector('#urge-3-input').value;
    const oldUrge1ID = document.querySelector('#urge-1-input').dataset.oldUrgeId;
    const oldUrge2ID = document.querySelector('#urge-2-input').dataset.oldUrgeId;
    const oldUrge3ID = document.querySelector('#urge-3-input').dataset.oldUrgeId;
    const action1 = document.querySelector('#action-1-input').value;
    const action2 = document.querySelector('#action-2-input').value;
    const oldAction1ID = document.querySelector('#action-1-input').dataset.oldActionId;
    const oldAction2ID = document.querySelector('#action-2-input').dataset.oldActionId;
    const entryReminderRadios = document.querySelectorAll(
        'input[name="entry-reminders-input"]');
    let entryReminders = null;
    for (const radio of entryReminderRadios) {
        if (radio.checked) {
            entryReminders = radio.value;
        }
    }
    const medTrackRadios = document.querySelectorAll(
        'input[name="med-tracking-input"]');
    let medTracking = null;
    for (const radio of medTrackRadios) {
        if (radio.checked) {
            medTracking = radio.value;
        }
    }
    const medReminderRadios = document.querySelectorAll(
        'input[name="med-reminders-input"]');
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
        phone_number: phoneNumber,
        urge1: urge1,
        urge2: urge2,
        urge3: urge3,
        old_urge1_id: oldUrge1ID,
        old_urge2_id: oldUrge2ID,
        old_urge3_id: oldUrge3ID,
        action1: action1,
        action2: action2,
        old_action1_id: oldAction1ID,
        old_action2_id: oldAction2ID,
        entry_reminders: entryReminders,
        med_tracking: medTracking,
        med_reminders: medReminders,
    };

    fetch('/api/update-settings', {
        method: 'PUT',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((res) => res.json())
    .then((resData) => {
        console.log(resData);
        if (resData.success === true) {
            window.location.href = "/settings";
        } else {
            window.scrollTo(0, 0);
        }
    });
});