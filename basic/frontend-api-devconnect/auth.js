let form = document.getElementById('login-form');
form.addEventListener('submit', (e) => {
    e.preventDefault()
    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }

    // ! sending authentication to the backend
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // ! getting and setting tokens
        console.log('DATA', data.access);
        if(data.access){
            localStorage.setItem('$(api-token)$', data.access)
            document.querySelector('.connect').innerHTML = `${formData.username} your connection was successful`; 
            window.location = 'file:///C:/xampp/htdocs/frontend-api-devconnect/projects-list.html'
        } else {
            alert('Username OR password');
        }
    })
})