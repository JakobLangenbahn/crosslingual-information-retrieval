import numpy as np
import pandas as pd


class DataSet:
    def __init__(self, preprocessed_class):
        self.preprocessed_dataframe = preprocessed_class.preprocessed_dataframe
        self.preprocessed_source = preprocessed_class.preprocessed_source
        self.preprocessed_target = preprocessed_class.preprocessed_target
        self.dataset = pd.DataFrame

    def get_sample(self, n):
        """ Method to generate a sample set of 2n with n correct examples and n wrong examples. """
        random_sample_right = self.preprocessed_dataframe.sample(n).reset_index(drop=True)
        random_sample_wrong = pd.concat([self.preprocessed_source.sample(n).reset_index(drop=True),
                                         self.preprocessed_target.sample(n).reset_index(drop=True)],
                                        axis=1)
        random_sample_wrong["Translation"] = np.zeros((int(random_sample_wrong.shape[0]), 1),
                                                      dtype=np.int8)

        self.dataset = pd.concat([random_sample_right, random_sample_wrong]).reset_index(drop=True)
