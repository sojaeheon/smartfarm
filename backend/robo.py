from roboflow import Roboflow

def sb_decision(disease_image):
    rf = Roboflow(api_key="sU34QbSDb0zkJY82W2tG")
    project = rf.workspace().project("strawberry_disease-n0bao")
    model = project.version(1).model

    strawberry_disease = {'Angular Leafspot':'각진반점', 'Blossom Blight':'꽃 곰팡이병','Anthracnose Fruit Rot':'탄저병','Gray Mold':'잿빛 곰팡이병','Leaf Spot':'세균모무늬병','Powdery Mildew Fruit':'과일흰가루병','Powdery Mildew Leaf':'잎 흰가루병'}
    # infer on a local image
    test = model.predict(disease_image, confidence=40, overlap=30).json()
    pre = strawberry_disease[test['predictions'][0]['class']]
    return pre