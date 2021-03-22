# 하나의 모듈에 넣어주기

# 전처리
import os
import re
from PIL import Image

# mat 삭제 함수 만들기
# 확장자 .mat이 뭔지 모르겠으니 지워야지~
def delete_mat(data_list):
    for i, data in enumerate (data_list): # 인덱스 준 이유
    basename = os.path.basename(data)
    _, file = basename.split('.')

        if file == 'mat':
            del data_list[i]  # 여기서 쓰려고!
    return data_list   # 주피터 노트북처럼 결과 가지고 있는게 아니라서 return 해줘야함


# channel 수 확인
# 3채널이 있을 수 있고 흑백 1채널, 4채널도 있을 수 있음
# 방법 1) 4채널 -> 3채널로 바꾸거나
# 방법 2) 4채널을 지우자

# 방법2 - 4채널 삭제 (RGB만 이용할게)
def delete_4_channel(data_list):
    for i,data in enumerate(data_list):
        image_data = Image.open(data) # 중요
        mode = image_data.mode        # 중요

        # mode : 이미지의 채널 형태 (어떻게 생겼는지 알려준다)
        # 3채널이면 mode가 RGB
        if mode != 'RGB':
            del data_list[i]
    return data_list

# 라벨 인코딩
def label_encoding(data_list):
    # 방법 1
    class_list = []
    for data in data_list:    # data = images/Egyptian_Mau_223.jpg
        basename = os.path.basename(data)   # basename = Egyptian_Mau_223.jpg
        label = os.path.splitext(basename)[0]   # label = Egyptian_Mau_223

        label = re.sub("_\d","",label)   #  Egyptian_Mau : 숫자 지워주는 역할

        if label in class_list:  # 중복 있으면 pass
            continue
        else:
            class_list.append(label)  # 라벨의 갯수
            
    # 클래스 안에 있던 것을 인덱스 붙여서 딕셔너리 형태로 만들어준다.
    class_to_index = {cls : i for i, cls in enumerate(class_list)}
    return class_to_index   