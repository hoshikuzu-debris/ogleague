document.querySelectorAll('.answer-comment-form').forEach(function(form){
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const url = form.getAttribute('action');
        const text = form.querySelector('input[type="text"]').value;
        const answerId = form.querySelector('input[type="text"]').getAttribute('name').replace('answer-comment-', '');

        fetch(url, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                'answer_id': answerId,
                'text': text,
            }),
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken,
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            form.parentNode.querySelector('.answer-comment-container').innerHTML = data.content
        }).catch(error => {
            console.log(error);
        });
    });
});