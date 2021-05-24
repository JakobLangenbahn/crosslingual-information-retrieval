""" Class for creating a parallel sentence dataset.
"""

import pandas as pd

from src.features.sentence_based import difference_numerical, relative_difference_numerical, \
    normalized_difference_numerical


class FeatureGeneration:
    """ Class for generating features from preprocessed parallel sentences.

    Attributes:
        preprocessed_dataset (dataframe): Preprocessed dataset
        feature_dataframe (dataframe): Dataset containing feature for training a model
        feature_difference_list (list): List of preprocessed columns that should be compared
    """
    def __init__(self, dataset):
        """ Initialize dataframe by importing europarl data for source and target

        Args:
            dataset (str): Path of the europarl source dataset
        """
        self.preprocessed_dataset = dataset
        self.feature_dataframe = pd.DataFrame()
        self.feature_difference_list = [
            'number_punctuations_total', 'number_words',
            'number_unique_words', 'number_!', 'number_"',
            'number_#', 'number_$', 'number_%',
            'number_&', "number_'", 'number_(',
            'number_)', 'number_*', 'number_+',
            'number_,', 'number_-', 'number_.',
            'number_/', 'number_:', 'number_;',
            'number_<', 'number_=', 'number_>',
            'number_?', 'number_@', 'number_[',
            "number_\\", "number_]", "number_^",
            'number__', 'number_`', 'number_{',
            'number_|', 'number_}', 'number_~',
            'number_characters', 'characters_avg',
            'number_ADJ', 'number_ADP',
            'number_ADV', 'number_AUX', 'number_CONJ',
            'number_CCONJ', 'number_DET', 'number_INTJ',
            'number_NOUN', 'number_NUM', 'number_PRT',
            'number_PRON', 'number_PROPN', 'number_SCONJ',
            'number_SYM', 'number_VERB', 'number_X',
            'number_Pres', 'number_Past', 'number_',
            'score_polarity', 'score_subjectivity',
            'number_stopwords']

    def feature_generation(self):
        """ Create comparative features of preprocessed columns.
        """
        for feature in self.feature_difference_list:
            self.feature_dataframe[f"{feature}_difference"] = difference_numerical(
                self.preprocessed_dataset[f"{feature}_source"], self.preprocessed_dataset[f"{feature}_target"])
            self.feature_dataframe[f"{feature}_difference_relative"] = relative_difference_numerical(
                self.preprocessed_dataset[f"{feature}_source"], self.preprocessed_dataset[f"{feature}_target"])
            self.feature_dataframe[f"{feature}_difference_normalized"] = normalized_difference_numerical(
                self.preprocessed_dataset[f"{feature}_source"], self.preprocessed_dataset[f"{feature}_target"],
                (self.preprocessed_dataset["number_punctuations_total_source"] + self.preprocessed_dataset[
                    "number_words_source"]),
                (self.preprocessed_dataset["number_punctuations_total_target"] + self.preprocessed_dataset[
                    "number_words_target"]))
        self.feature_dataframe["Translation"] = self.preprocessed_dataset["Translation"]
