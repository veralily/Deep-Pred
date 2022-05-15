import pandas as pd
from nltk.util import ngrams
import collections
import numpy as np


class Repetition(object):
    def __init__(self, ngram=4):
        # vrama91: updated the value below based on discussion with Hovey
        self.ngram = ngram

    def get_repetition(self, sentence):
        sixgrams = ngrams(sentence.split(), self.ngram)
        result = collections.Counter(sixgrams)
        count = 0
        for k, v in dict(result).items():
            if v > 1:
                count += 1
        score = 0 if len(result) == 0 else count / float(len(result))

        return dict(result), score

    def compute_score(self, res_dict):
        """
        Computes Rouge-L score given a set of reference and candidate sentences for the dataset
        Invoked by evaluate_captions.py
        :param hypo_for_image: dict : candidate / inference sentences with "image name" key and "tokenized sentences" as values
        :param ref_for_image: dict : reference MS-COCO sentences with "image name" key and "tokenized sentences" as values
        :returns: average_score: float (mean ROUGE-L score computed by averaging scores for all the images)
        """
        score = []
        sentences = res_dict.values()
        for sentence in sentences:
            result, repetition_ratio = self.get_repetition(sentence[0])

            score.append(repetition_ratio)

        average_score = np.mean(np.array(score))
        print("len score:", len(score))
        return average_score, np.array(score)

    def method(self):
        return "Repetition"
