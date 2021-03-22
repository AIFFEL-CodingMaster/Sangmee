import os
import re
from glob import glob
from PIL import Image
import tensorflow as tf 

class MakeTFRecord:  # TFRecord 만드는 클래스
    IMG_SIZE = 224   # 이미지 사이즈 224로 고정

    def __init__(self,data_list,tfr_path,data_class):
        self.data_list = data_list
        self.tfr_path = tfr_path
        self.data_class = data_class

    # tf record 내에서만 이용할 경우 앞에 _써주는 약속
    # TF writer를 만드는 함수 - 
    def _make_tf_writer(self):   
        writer = tf.io.TFRecordWriter(self.tfr_path) 
        # TFRecordWriter() 사용해서 TFRecord 파일로 저장해준다.
        return writer

    # The following functions can be used to convert a value to a type compatible
    # with tf.Example.
    # 그대로 복사해오고 class안에 넣어줄거라 staticmethod 추가해준다. 그냥 복붙 부분이다.
    @staticmethod
    def _bytes_feature(value):
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy() # BytesList won’t unpack a string from an EagerTensor.
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
    @staticmethod
    def _float_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))
    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


    def _make_tfrecord(self):
        writer = self._make_tf_writer()
        n = 0

        for data in self.data_list:
            image = Image.open(data)   # 이미지 열기
            image = image.resize((self.IMG_SIZE,self.IMG_SIZE))

            #tf record는 byte로 구성
            image_to_byte = image.tobytes()
            basename = os.path.basename(data)   # basename = Egyptian_Mau_223.jpg
            label = os.path.splitext(basename)[0]   # label = Egyptian_Mau_223

            label = re.sub("_\d","",label)   #  Egyptian_Mau : 숫자 지워주는 역할
            label_num = self.data_class[label]

            #tf.train.Example 이용하여 Feature message 생성 
            # - Feature를 딕셔너리 형태로 정의하고 적합한 형태로 변환
            # key - feature name
            # value - tf.Example에 적합한 타입
            example = tf.train.Example(feature=tf.train.Features(feature={
                "image" : self._bytes_feature(image_to_byte),
                "label" : self._int64_feature(label_num)
                # byte로 바꾼 이미지를 byte_feature의 입력으로 넣어줌
            }))

            #tf.train.Example 객체를 writer. 를 통해 TFRecord 파일로 저장
            writer.write(example.SerializeToString()) # SerializeToString함수를 통해 binary string으로 변환
            n +=1
        writer.close() # writer close 해주기 - 공식임..
        print(f"{n}개의 데이터, TFRecord 완성!!")


    @classmethod
    def change_img_size(cls,image_size):
        cls.IMG_SIZE = image_size
    
    def __call__(self):  # 클래스 호출하면 이 메세지 바로 뜸
        print("tfrecord 만들기 시작")
        self._make_tfrecord()

    # tfr = MakeTFRecord()