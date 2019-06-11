#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/6/10 22:38 
# @Author : yangpingyan@gmail.com

import tensorflow as tf
import numpy as np
import time
from PIL import Image
from cnnlib.network import CNN


class RecognizeCaptcha(CNN):
    def __init__(self, model_save_dir):
        char_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        super(RecognizeCaptcha, self).__init__(35, 70, 4, char_set, model_save_dir)
        self.y_predict = self.model()

    def recognize_image(self, image_file):
        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess, self.model_save_dir)
            captcha_image = Image.open(image_file)
            test_image = np.array(captcha_image)  # 向量化
            test_image = self.convert2gray(test_image)
            test_image = test_image.flatten() / 255

            predict = tf.argmax(tf.reshape(self.y_predict, [-1, self.max_captcha, self.char_set_len]), 2)
            text_list = sess.run(predict, feed_dict={self.X: [test_image], self.keep_prob: 1.})
            predict_text = text_list[0].tolist()
            p_text = ""
            for p in predict_text:
                p_text += str(self.char_set[p])
            print("predict: {}".format(p_text))



def main():
    image_file ='c:/sample/local/1qY3_15600651829462104.png'

    rc = RecognizeCaptcha('model/')
    rc.recognize_image(image_file)

if __name__ == '__main__':
    main()
