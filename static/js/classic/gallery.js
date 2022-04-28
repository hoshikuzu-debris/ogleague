// 検索ボタンで呼ばれる
document.getElementById('ajax-search-post').addEventListener('submit', e => {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

    const text = encodeURIComponent(document.getElementById('id_text').value);
    const url = document.getElementById('ajax-search-post').getAttribute('action');
    const url_query = `${url}?text=${text}`;
    const postArea = document.getElementById('posts');
    const questionListArea = document.querySelector('.question_list')

    fetch(url_query).then(response => {
            return response.json();
        }).then(response => {
            //console.log("response question-list:" + response.question_list)
            postArea.innerHTML = '';
            questionListArea.innerHTML = '';
            for(const question of response.question_list){
                const a = document.createElement('a');
                const gallery_list_url = document.getElementById('gallery-list').getAttribute('href'); // navbarのギャラリー一覧のリンクを取得している
                const a_href = `${gallery_list_url}${question.id}/`;
                a.setAttribute("href", a_href);
                a.setAttribute("class", "d-block");
                a.textContent = question.text;
                postArea.appendChild(a);
            }
        }).catch(error => {
            console.log(error);
    });
});