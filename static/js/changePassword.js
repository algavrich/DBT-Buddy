'use strict';

const changePasswordForm = document.querySelector('form');

changePasswordForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
    
    const currentPassword = document.querySelector(
        '#current-password-input'
    ).value;
    const newPassword1 = document.querySelector(
        '#new-password-input-1'
    ).value;
    const newPassword2 = document.querySelector(
        '#new-password-input-2'
    ).value;

    if (currentPassword.match(/[A-Z]/) 
        && currentPassword.match(/[a-z]/) 
        && currentPassword.match(/[0-9]/)
        && currentPassword.match(
            /[!@#$%\^&\*\(\)-_=\+\[\]\{\}\\\|;:'"\,<\.>\/\?~`]/
        )
        && currentPassword.length >= 8) {
        const url = `
            /api/check-current-password?current_password=${currentPassword}
        `;
        fetch(url)
        .then((res) => res.json())
        .then((resData) => {
            // Could condense with switch case 
            if (resData.match === true) {
                if (newPassword1 === newPassword2) {
                    if (newPassword1 !== currentPassword) {
                        if (newPassword1.match(/[A-Z]/) 
                            && newPassword1.match(/[a-z]/) 
                            && newPassword1.match(/[0-9]/)
                            && newPassword1.match(
                                /[!@#$%\^&\*\(\)-_=\+\[\]\{\}\\\|;:'"\,<\.>\/\?~`]/
                            )
                            && newPassword1.length >= 8) {
                            fetch('/api/update-password', {
                            method: 'PUT',
                            body: JSON.stringify({new_password: newPassword1}),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            })
                            .then((res) => res.json())
                            .then((resData) => {
                                if (resData.success) {
                                    window.location.href = '/settings';
                                } else {
                                    window.scrollTo(0, 0);
                                }
                            });
                        } else {
                            alert('New password doesn\'t meet requirements');
                        }
                    } else {
                        alert('New password must be different from your old one')
                    } 
                } else {
                    alert('New password doesn\'t match');
                }
            } else {
                alert('Incorrect current password');
            }
        });
    } else {
        alert('Current password does not meet requirements');
    }
});