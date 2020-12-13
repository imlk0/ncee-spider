# -*- coding: utf-8 -*-
from PIL import Image
import base64
import io
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import argparse
import yaml
import os

from keras.utils import np_utils, plot_model
from keras.models import Model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.callbacks import EarlyStopping
from keras.layers import Conv2D, MaxPooling2D, Input

import fetch
import resolver
import db


def parse_opt():
    parser = argparse.ArgumentParser(
        description='tool to train model for captcha recognition', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('mode', action="store", choices=[
                        'fetch', 'train', 'test'], help='sub_command. \nfetch: fetch more captcha image from website\ntrain: train model using all captcha data in db\ntest: test captcha recognition effect on online data', type=str)
    parser.add_argument('-m', action="store", dest='model_file', type=str, required=False,
                        help='model file path')
    parser.add_argument('-c', action="store", dest='config_file', type=str, required=False,
                        help='config file path, default is ./configuration.yaml')
    args = parser.parse_args()
    return args


def load_conf(args):
    if args.config_file is None:
        config = yaml.safe_load(open((os.path.dirname(__file__) if '__file__' in globals() and len(
            os.path.dirname(__file__)) > 0 else '.') + '/configuration.yaml'))
    else:
        config = yaml.safe_load(open(args.config_file))
    return config


label_keys = list('0123456789') + list('abcdefghijklmnopqrstuvwxyz')
label_cats = list(range(len(label_keys)))

map_key_to_cat = dict(zip(label_keys, label_cats))
map_cat_to_key = dict(zip(label_cats, label_keys))


def img_to_model_input(img):
    return np.array(Image.open(io.BytesIO(base64.b64decode(img))))


def prepare_dataset():
    n_label = len(label_keys)
    data = db.query_recognized_captchas()
    txts = list(map(lambda x: list(x['txt'].lower()), data))
    txts = list(map(lambda x: np.concatenate(
        list(map(lambda x: np.eye(n_label)[map_key_to_cat[x]].reshape((1, -1)), x)), axis=0), txts))
    imgs = list(map(lambda x: img_to_model_input(x['img']), data))
    x_data = np.array(imgs)
    y_data = np.array(txts)
    X_train, X_test, Y_train, Y_test = train_test_split(
        x_data, y_data, test_size=0.3, random_state=42)
    return X_train, X_test, Y_train, Y_test


def create_model(input_shape, output_shape):
    main_input = Input(shape=input_shape)
    x = main_input

    x = Conv2D(32, kernel_size=(3, 3),
               input_shape=input_shape, padding='same')(x)
    x = Activation('relu')(x)
    x = Conv2D(32, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same')(x)

    x = Dropout(0.25)(x)

    x = Conv2D(64, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = Conv2D(64, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same')(x)

    x = Dropout(0.25)(x)

    x = Conv2D(128, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = Conv2D(128, kernel_size=(3, 3), padding='same')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(2, 2), padding='same')(x)

    x = Dropout(0.25)(x)

    x = Flatten()(x)

    def create_conn(x):
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(output_shape[1], activation='softmax')(x)
        return x
    x0 = create_conn(x)
    x1 = create_conn(x)
    x2 = create_conn(x)
    x3 = create_conn(x)

    model = Model(inputs=[main_input], outputs=[x0, x1, x2, x3])
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    return model


def load_model(model_path):
    from keras.models import load_model
    model = load_model(model_path)
    return model


def img_predect(model, img):
    X = img_to_model_input(img)
    y_pred = np.array(model.predict(np.array([X]))).swapaxes(0, 1)[0]
    predictions = np.argmax(y_pred, axis=1)
    return ''.join(list(map(lambda x: map_cat_to_key[x], predictions)))


if __name__ == "__main__":
    args = parse_opt()
    config = load_conf(args)
    db.init()
    if args.mode == 'fetch':
        while True:
            base64img, cookie = fetch.get_captcha()
            ocr, limited = fetch.baidu_ocr(
                config, fetch.captcha_to_img(base64img))
            if limited:  # ocr request limited
                print('ocr service request limit reached, we will exit!!!')
                exit(-1)
            if ocr is None:
                continue
            print('query a unexisted student')
            content = fetch.query_student('111111111', '1111', ocr, cookie)
            state_code = resolver.get_state_code(content)
            print('state_code: {}'.format(state_code))
            if state_code == 2:
                print('captcha was recognized, apped it to database')
                db.insert_recognized_captcha(base64img, ocr)
    elif args.mode == 'train':
        if args.model_file is None:
            print("module path is is required, please use `-m` option to specific it")
            exit(-1)
        X_train, X_test, Y_train, Y_test = prepare_dataset()
        model = create_model(X_train[0].shape, Y_train[0].shape)
        callbacks = [EarlyStopping(monitor='val_acc', patience=5, verbose=1)]
        batch_size = 64
        n_epochs = 30
        history = model.fit(X_train, list(Y_train.swapaxes(0, 1)), batch_size=batch_size, epochs=n_epochs,
                            verbose=1, validation_data=(X_test, list(Y_test.swapaxes(0, 1))), callbacks=callbacks)
        model.save(args.model_file)
    elif args.mode == 'test':
        if args.model_file is None:
            print("module path is is required, please use `-m` option to specific it")
            exit(-1)
        model = load_model(args.model_file)
        # plot_model(model, to_file=r'./model.png', show_shapes=True)
        count_all = 0
        count_right = 0
        while True:
            base64img, cookie = fetch.get_captcha()
            ocr = img_predect(model, base64img)
            # img = Image.open(io.BytesIO(base64.b64decode(base64img)))
            # img.show()
            content = fetch.query_student('111111111', '1111', ocr, cookie)
            count_all += 1
            state_code = resolver.get_state_code(content)
            if state_code == 2:
                count_right += 1
                db.insert_recognized_captcha(base64img, ocr)
            print('captcha: {}, ocr: {}, state_code: {}, right: {}, acc: {}'.format(
                base64img[-32:], ocr, state_code, state_code == 2, count_right / count_all))
