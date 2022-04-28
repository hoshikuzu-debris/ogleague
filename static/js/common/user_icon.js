// 初期表示時はCroppieを非表示
//$('#icon_croppie').css('display','none');

$upload_crop = $('#icon_croppie').croppie({
    viewport: {
        width: 200,
        height: 200,
        type: 'circle'
    },
    boundary: {
        width: 200,
        height: 200
    },
});


const iconModal = new bootstrap.Modal(document.getElementById('iconModal'), {});
const fileInput = document.querySelector('input[type="file"]');

$("#upload_icon").on('change', function(event){
    iconModal.show();
});


document.getElementById('iconModal').addEventListener('show.bs.modal', function(ev) {
    console.log('show.bs.modal');

    $upload_crop.croppie('bind', {
        url: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdj+P///38ACfsD/QVDRcoAAAAASUVORK5CYII=", // 白の1px画像データ
    }).then(function() {
        console.log('bind complete');
    });

});


document.getElementById('iconModal').addEventListener('shown.bs.modal', function() {
    console.log('shown.bs.modal');

    let file = fileInput.files[0];
    let reader = new FileReader();

    // dataURL形式で画像ファイルを読み込む
    reader.readAsDataURL(file);

    // 画像ファイルの読込が終了した時の処理
    reader.onload = function () {
        $upload_crop.croppie('bind', {
            url: reader.result,
        }).then(function() {
            console.log('bind complete');
            // fileInputの中身を空にする
            fileInput.value = "";
        });
    };
});


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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#icon_submit').on('click', function(event) {
    console.log('click');
    let confirm = window.confirm("プロフィール画像を登録してよろしいですか？");
    if (confirm) {
        $upload_crop.croppie('result',{
            type: 'base64',
            circle: true,
        }).then(function(response) {
            console.log(response);
            const url = event.target.dataset.url;
            console.log("response:" + response);
            console.log("event.target:" + event.target);
            // console.log("url:" + url);

            // $('#icon_cropped').html(" ");
            //$('#user-icon').attr({'src': response, });

            // 'class': 'rounded-circle .border .border-0'


            $.ajax({
                'url': url,
                'type': 'POST',
                'data': {
                    'image': response,
                },
                'dataType': 'json'
            }).done( data => {
                $('#modal-dismiss').click()
                $('#user-icon').attr({'src': data.imageURL, });
            });
        });
    }
});