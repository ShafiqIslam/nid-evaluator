from app.modules.evaluator.bd.image_classifier.available_classifier import AvailableClassifier
from app.modules.evaluator.bd.image_classifier.classifier import Classifier
from app.modules.evaluator.bd.image_classifier.naive import Naive
from app.modules.evaluator.bd.image_classifier.resnet50 import ResNet50


class ClassifierFactory:
    @staticmethod
    def get(filename: str, strategy: AvailableClassifier) -> Classifier:

        if strategy is AvailableClassifier.NAIVE:
            classifier_strategy = ClassifierFactory.get_naive_classifier()
        elif strategy is AvailableClassifier.RESNET50:
            classifier_strategy = ResNet50()
        else:
            classifier_strategy = ResNet50()

        classifier_strategy.set_image(filename)
        training_dataset, test_dataset = ClassifierFactory.get_classifier_data()
        classifier_strategy.set_dataset(training_dataset, test_dataset)

        classifier = Classifier()
        classifier.set_strategy(classifier_strategy)
        return classifier

    @staticmethod
    def get_classifier_data():
        training_dataset = []
        test_dataset = []
        return training_dataset, test_dataset

    @staticmethod
    def get_naive_classifier():
        naive = Naive()
        naive.set_network_layers([784, 30])
        naive.set_learning_rate(0.3)
        return naive
