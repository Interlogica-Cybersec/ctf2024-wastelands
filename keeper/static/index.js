form.addEventListener("submit", event => {
    event.preventDefault();
    result.innerText = 'Waiting for a response from the keeper';
    const formData = new FormData();
    formData.append('message', document.getElementById('message').value);
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (!data.granted) {
            document.body.classList.remove('turn-green')
            document.body.classList.add('turn-red')
            setTimeout(() => document.body.classList.remove('turn-red'), 2000)
        } else {
            document.body.classList.remove('turn-red')
            document.body.classList.add('turn-green')
            setTimeout(() => document.body.classList.remove('turn-green'), 2000)
        }
        result.innerText = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
})