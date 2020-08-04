import os
from typing import Optional
import keras
import pickle
import numpy as np
import cv2
from app import App
from app.modules.evaluator.bd.image_classifier.classifier_strategy import ClassifierStrategy
from app.modules.evaluator.bd.nid_format import NIDFormat


class ResNet50(ClassifierStrategy):
    MINI_BATCH_SIZE = 30
    EPOCHS = 10
    NO_OF_CLASS = 3

    def __init__(self):
        pass

    def classify(self) -> Optional[NIDFormat]:
        model = keras.models.load_model(self._get_model_path())
        with open(self._get_class_file_path(), 'rb') as file:
            classes = pickle.load(file)

        image = cv2.imread(self.filename)
        model_input = np.array(image).reshape((1, 32, 32, 3)).astype('float32') / 255
        predictions = model.predict(model_input).ravel()
        prediction = np.argmax(predictions)
        classified_as = classes[prediction].lower()
        return None if classified_as is "none" else classified_as

    @staticmethod
    def _get_model_path():
        return os.path.join(App.models_folder, 'resnet_50.h5')

    @staticmethod
    def _get_class_file_path():
        return os.path.join(App.models_folder, 'classes.pkl')

    def get_model(self):
        if os.path.isfile(self._get_model_path()):
            return keras.models.load_model(self._get_model_path())

        return self.create_model()

    def create_model(self):
        inputs = keras.layers.Input(shape=(None, None, 3))
        outputs = keras.layers.ZeroPadding2D(padding=3, name='padding_conv1')(inputs)
        outputs = keras.layers.Conv2D(64, (7, 7), strides=(2, 2), use_bias=False, name='conv1')(outputs)
        outputs = keras.layers.BatchNormalization(axis=3, epsilon=1e-5, name='bn_conv1')(outputs)
        outputs = keras.layers.Activation('relu', name='conv1_relu')(outputs)
        outputs = keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same', name='pool1')(outputs)
        outputs = self._create_convolution_block(outputs, 3, [64, 64, 256], stage=2, block='a', strides=(1, 1))
        outputs = self._create_identity_block(outputs, 3, [64, 64, 256], stage=2, block='b')
        outputs = self._create_identity_block(outputs, 3, [64, 64, 256], stage=2, block='c')
        outputs = self._create_convolution_block(outputs, 3, [128, 128, 512], stage=3, block='a')
        outputs = self._create_identity_block(outputs, 3, [128, 128, 512], stage=3, block='b')
        outputs = self._create_identity_block(outputs, 3, [128, 128, 512], stage=3, block='c')
        outputs = self._create_identity_block(outputs, 3, [128, 128, 512], stage=3, block='d')
        outputs = self._create_convolution_block(outputs, 3, [256, 256, 1024], stage=4, block='a')
        outputs = self._create_identity_block(outputs, 3, [256, 256, 1024], stage=4, block='b')
        outputs = self._create_identity_block(outputs, 3, [256, 256, 1024], stage=4, block='c')
        outputs = self._create_identity_block(outputs, 3, [256, 256, 1024], stage=4, block='d')
        outputs = self._create_identity_block(outputs, 3, [256, 256, 1024], stage=4, block='e')
        outputs = self._create_identity_block(outputs, 3, [256, 256, 1024], stage=4, block='f')
        outputs = self._create_convolution_block(outputs, 3, [512, 512, 2048], stage=5, block='a')
        outputs = self._create_identity_block(outputs, 3, [512, 512, 2048], stage=5, block='b')
        outputs = self._create_identity_block(outputs, 3, [512, 512, 2048], stage=5, block='c')
        outputs = keras.layers.GlobalAveragePooling2D(name='pool5')(outputs)
        outputs = keras.layers.Dense(self.NO_OF_CLASS, activation='softmax', name='fc1000')(outputs)
        model = keras.models.Model(inputs=inputs, outputs=outputs)
        print()
        print(model.summary(), '\n')
        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.adam(lr=0.01, clipnorm=0.001), metrics=['accuracy'])
        return model

    @staticmethod
    def _create_identity_block(input_layer, kernel_size, filters, stage, block):
        filters1, filters2, filters3 = filters
        conv_name_base = 'res' + str(stage) + block + '_branch'
        bn_name_base = 'bn' + str(stage) + block + '_branch'
        # Create layers
        output = keras.layers.Conv2D(filters1, (1, 1), kernel_initializer='he_normal', name=conv_name_base + '2a')(
            input_layer)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2a')(output)
        output = keras.layers.Activation('relu')(output)
        output = keras.layers.Conv2D(filters2, kernel_size, padding='same', kernel_initializer='he_normal', name=conv_name_base + '2b')(output)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2b')(output)
        output = keras.layers.Activation('relu')(output)
        output = keras.layers.Conv2D(filters3, (1, 1), kernel_initializer='he_normal', name=conv_name_base + '2c')(output)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2c')(output)
        output = keras.layers.add([output, input_layer])
        output = keras.layers.Activation('relu')(output)
        return output

    @staticmethod
    def _create_convolution_block(input_layer, kernel_size, filters, stage, block, strides=(2, 2)):
        filters1, filters2, filters3 = filters
        conv_name_base = 'res' + str(stage) + block + '_branch'
        bn_name_base = 'bn' + str(stage) + block + '_branch'
        # Create block layers
        output = keras.layers.Conv2D(filters1, (1, 1), strides=strides, kernel_initializer='he_normal', name=conv_name_base + '2a')(input_layer)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2a')(output)
        output = keras.layers.Activation('relu')(output)
        output = keras.layers.Conv2D(filters2, kernel_size, padding='same', kernel_initializer='he_normal', name=conv_name_base + '2b')(output)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2b')(output)
        output = keras.layers.Activation('relu')(output)
        output = keras.layers.Conv2D(filters3, (1, 1), kernel_initializer='he_normal', name=conv_name_base + '2c')(output)
        output = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '2c')(output)
        shortcut = keras.layers.Conv2D(filters3, (1, 1), strides=strides, kernel_initializer='he_normal', name=conv_name_base + '1')(input_layer)
        shortcut = keras.layers.BatchNormalization(axis=3, name=bn_name_base + '1')(shortcut)
        output = keras.layers.add([output, shortcut])
        output = keras.layers.Activation('relu')(output)
        return output

    def train(self):
        img_width, img_height = 32, 32
        model = self.get_model()
        # Create a data generator for training
        train_data_generator = keras.preprocessing.image.ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        # Create a data generator for validation
        validation_data_generator = keras.preprocessing.image.ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        # Create a train generator
        train_generator = train_data_generator.flow_from_directory(
            self.training_dataset,
            target_size=(img_width, img_height),
            batch_size=self.MINI_BATCH_SIZE,
            color_mode='rgb',
            shuffle=True,
            class_mode='categorical')
        # Create a test generator
        validation_generator = validation_data_generator.flow_from_directory(
            self.test_dataset,
            target_size=(img_width, img_height),
            batch_size=self.MINI_BATCH_SIZE,
            color_mode='rgb',
            shuffle=True,
            class_mode='categorical')
        # Start training, fit the model
        model.fit_generator(
            train_generator,
            steps_per_epoch=len(self.training_dataset) // self.MINI_BATCH_SIZE,
            validation_data=validation_generator,
            validation_steps=len(self.test_dataset) // self.MINI_BATCH_SIZE,
            epochs=self.EPOCHS)
        # Save model to disk
        model.save(self._get_model_path())

        # Get labels
        labels = train_generator.class_indices
        # Invert labels
        classes = {}
        for key, value in labels.items():
            classes[value] = key.capitalize()
        with open(self._get_class_file_path(), 'wb') as file:
            pickle.dump(classes, file)
        print('Saved classes to disk!')
