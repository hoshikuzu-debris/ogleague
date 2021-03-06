document.querySelectorAll('.favorite-form').forEach(function(form){
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const url = event.target.getAttribute('action');
        const answerId = event.submitter.getAttribute('name').replace('favorite-', '');

        fetch(url, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                'answer_id': answerId
            }),
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken,
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            event.submitter.parentNode.innerHTML = data.content
        }).catch(error => {
            console.log(error);
        });
    });
});