from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from common.models import Profile
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

import base64
from io import BytesIO
from PIL import Image


@login_required
def icon_upload(request):
    ''' プロフィール編集画面からPOSTされた画像データの保存処理 '''
    def base64_to_pil(img_str):
        if "base64," in img_str:
            # DARA URI の場合、data:[<mediatype>][;base64], を除く
            img_str = img_str.split(",")[1]
        img_raw = base64.b64decode(img_str)
        img = Image.open(BytesIO(img_raw))

        return img

    # base64 文字列
    img_base64 = request.POST.get('image')

    # PIL.Image 形式に変換する。
    img = base64_to_pil(img_base64)

    date = timezone.now()
    file_name = '/image/common/user_icon/' + str(request.user.id) + '_' + date.strftime("%Y%m%d%H%M%S") + '.png'
    img.save(str(settings.MEDIA_ROOT) + file_name)

    # 保存した画像を登録
    profile = get_object_or_404(Profile, pk=request.user.profile.id)
    profile.icon = file_name
    profile.save()

    data = {'imageURL' : profile.icon.url}
    return JsonResponse(data)