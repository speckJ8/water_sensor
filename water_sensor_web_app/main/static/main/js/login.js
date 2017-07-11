/**
 * takes the username and password entered and tries to login with the server
 */
doLogin = () => {

    var usernameField = document.getElementById('username');
    var usernameFieldWrapper = document.getElementById('username-field');    
    var passwordField = document.getElementById('password');
    var passwordFieldWrapper = document.getElementById('password-field');
    

    // POST data
    var data = {
        username: usernameField.value,
        password: passwordField.value
    }

    // to add the CSRF token
    addCSRF(data);

    $.post(DO_LOGIN_PATH, data)
    .done((result) => {

        jsonRes = JSON.parse(result);

        if (jsonRes.state == 'ok') {
            window.location.href = window.location.origin + HOME_PATH;
        } else {
            if (jsonRes.err == 'username') {
                // clear fields and show error in username field
                usernameField.value = '';
                passwordField.value = '';
                usernameFieldWrapper.classList.add('is-invalid');
            } else if (jsonRes.err == 'password') {
                // clear password field and show error in password field
                passwordField.value = '';
                passwordFieldWrapper.classList.add('is-invalid');
            }
        }

    })
    .fail(() => {

        showErrorDialog('Erro de conexão');

    });
}