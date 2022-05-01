const fileInput = document.querySelector('input[type="file"]');
const imgQuestion = document.querySelector('.img-question-container');


fileInput.addEventListener('change', function() {
    const file = this.files[0];
    const reader = new FileReader();
    const img = document.createElement("img");

    console.log(imgQuestion);
    console.log(fileInput);

    // imgQuestion.innerHTML = " ";
    // dataURL形式で画像ファイルを読み込む
    reader.readAsDataURL(file);

    // 画像ファイルの読込が終了した時の処理
    reader.onload = function () {
        img.setAttribute("src", reader.result);
        //img.setAttribute("class", "img-fluid");
        img.setAttribute("alt", "お題画像");
        img.classList.add('img-fluid');
        //img.style.setProperty("max-width", "100%");
        //img.style.setProperty("max-height", "100%");
        imgQuestion.appendChild(img);
    };
});