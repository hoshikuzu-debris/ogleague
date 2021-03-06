// チェックするお題がないときmodalは出現しない
const checkQuestionModalEl = document.getElementById('checkQuestionModal');
if (checkQuestionModalEl) {
    const checkQuestionModal = new bootstrap.Modal(checkQuestionModalEl, {
        backdrop: 'static',
        keyboard: false,
    });
    checkQuestionModal.show();

    // いいねボタンかう〜んボタンで呼ばれる
    document.getElementById('form-check-question').addEventListener('submit', (event) => {
        // デフォルトのイベントをキャンセルし、ページ遷移しないように!
        event.preventDefault();

        const submitter = event.submitter;
        const url = event.target.getAttribute('action');
        const question_id = submitter.getAttribute('name').replace('question-check-', '');
        const choice = submitter.getAttribute('value');
        const data = {
            'question_id': question_id,
            'choice': choice
        }

        fetch(url, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken,
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            if (data.success) {
                checkQuestionModal.hide();
            }
        }).catch(error => {
            console.log(error);
        });
    })

}

