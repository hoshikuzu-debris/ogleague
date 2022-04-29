function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


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