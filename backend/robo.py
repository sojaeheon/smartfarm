from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont

# 딸기 병해진단 부분
def sb_decision(disease_image):
    rf = Roboflow(api_key="sU34QbSDb0zkJY82W2tG")
    project = rf.workspace().project("strawberry_disease-n0bao")
    model = project.version(1).model

    strawberry_disease = {'Angular Leafspot':'각진반점', 'Blossom Blight':'꽃 곰팡이병','Anthracnose Fruit Rot':'탄저병','Gray Mold':'잿빛 곰팡이병','Leaf Spot':'세균모무늬병','Powdery Mildew Fruit':'과일흰가루병','Powdery Mildew Leaf':'잎 흰가루병'}
    # infer on a local image
    test = model.predict(disease_image, confidence=40, overlap=30).json()
    print(test)
    pre = strawberry_disease[test['predictions'][0]['class']]
    return pre, test


# 바운딩 박스 부분
def draw_bounding_box(disease_image, predictions, disease_name):
    # 이미지 열기
    image = Image.open(disease_image)
    draw = ImageDraw.Draw(image)

    # 한국어를 지원하는 두꺼운 폰트 설정
    try:
        font = ImageFont.truetype("malgunbd.ttf", 16)  # Malgun Gothic Bold 폰트
    except IOError:
        font = ImageFont.load_default()  # 기본 폰트로 대체

    # 예측된 각 객체에 대해 바운딩 박스 그리기
    for pred in predictions['predictions']:
        x = pred['x']
        y = pred['y']
        width = pred['width']
        height = pred['height']

        # 바운딩 박스 좌표 계산
        left = x - width / 2
        top = y - height / 2
        right = x + width / 2
        bottom = y + height / 2

        # 바운딩 박스 그리기
        draw.rectangle([left, top, right, bottom], outline="blue", width=5)

        # 텍스트 크기 계산
        text = disease_name
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # 텍스트 배경 그리기
        text_background = [left, top - text_height - 2, left + text_width + 4, top]
        draw.rectangle(text_background, fill="blue")

        # 그림자 효과 추가 (검은색 텍스트를 약간 이동시켜서 그림자 효과를 만듭니다)
        shadow_offset = 1  # 그림자의 오프셋
        draw.text((left + 2 + shadow_offset, top - text_height - 2 + shadow_offset), text, fill="black", font=font)

        # 텍스트 그리기 (파란색 배경 위에 흰색 글씨)
        draw.text((left + 2, top - text_height - 2), text, fill="white", font=font)

    return image


# disease_image_path = 'white.jfif'

# name,test_data= sb_decision(disease_image_path)

# image_with_bounding_box = draw_bounding_box(disease_image_path, test_data,name)

# # 바운딩 박스가 그려진 이미지 저장
# image_with_bounding_box.save("output_with_bounding_box.jpg")