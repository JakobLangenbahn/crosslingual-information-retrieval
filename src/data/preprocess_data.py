""" Functions to implement possible preprocessing steps:
- Tokenization
- Removing white spaces
- Transform to lower case
- Removal of Punctuations
- Removal of Stopwords
- Lemmatization
- Total number of punctuation marks
- Count of different punctuation marks
- Number of words
- Number of unique words
- Number characters
- Number of different POS tags
- Number of different times
- Number of different Named Entities
- Number of Stopwords
- Sentiment Analysis

Possible next steps:
- Apply spelling correction
- Expanding Contractions
- Converting numbers into words or removing numbers
- Remove special characters
- Expanding abbreviations

"""
import pickle
import string
import re

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), round(run_time, 3)))
        return value

    return wrapper


@timer
def lemmatize(sentence_vector, nlp_language):
    """ Function to lemmatize an array of tokens.

        Args:
            sentence_vector (numpy.array): Array containing text
            nlp_language

        Returns:
            numpy.array: Array containing the lemmatized words

        """
    lemmatizer_language = nlp_language.get_pipe("lemmatizer")
    return sentence_vector.apply(lambda sentence: " ".join([token.lemma_ for token in nlp_language(sentence)]))


@timer
def tokenize_sentence(sentence_vector):
    """ Function to tokenize an array of sentences.

       Args:
           sentence_vector (numpy.array): Array containing text/sentences

       Returns:
           numpy.array: Array containing the individual tokens of the input sentence

       """
    return sentence_vector.apply(lambda sentence: word_tokenize(sentence))


@timer
def strip_whitespace(token_vector):
    """ Function to strip whitespaces of an array of sentences.

        Args:
            token_vector (numpy.array): Array containing text

        Returns:
            numpy.array: Array containing the individual tokens of the input sentence without possible whitespaces

        """
    return token_vector.apply(lambda word: list(map(str.strip, word)))


@timer
def lowercase(token_vector):
    """ Function to lowercase an array of sentences.

        Args:
            token_vector (numpy.array): Array containing tokenized sentence

        Returns:
            numpy.array: Array containing tokenized, lowercased sentence

        """
    return token_vector.apply(lambda row: list(map(str.lower, row)))


@timer
def remove_punctuation(token_vector):
    """ Function to remove punctuation out of an array of sentences

        Args:
            token_vector (numpy.array): Array containing tokenized, lowercased sentence

        Returns:
            numpy.array: Array containing tokenized sentence removed punctuation

        """
    punctuations = string.punctuation + "’" + "..." + "'"
    return token_vector.apply(lambda sentence: [word for word in sentence if word not in punctuations])


@timer
def remove_stopwords(token_vector, stopwords_language):
    """ Function to remove stopwords out of an array of sentences

        Args:
            token_vector (numpy.array): Array containing text
            stopwords_language (list): List of stopwords in a specific language

        Returns:
            numpy.array: Array containing tokenized sentence removed stopwords
        """
    return token_vector.apply(lambda sentence: [word for word in sentence if word not in stopwords_language])


@timer
def remove_numbers(token_vector):
    """ Function to remove numbers out of an array of sentences

        Args:
            token_vector (numpy.array): Array containing tokenized, lowercased sentence

        Returns:
            numpy.array: Array containing tokenized sentence removed numbers

        """
    translation_table = str.maketrans('', '', string.digits)
    return token_vector.apply(lambda sentence: [word.translate(translation_table) for word in sentence])


@timer
def create_cleaned_token_embedding(sentence_vector, nlp_language, stopwords_language):
    """ Function combine cleaning function for embedding-based features

    Args:
        sentence_vector (numpy.array): Array containing text
        nlp_language -> spacy package function to tag words
        stopwords_language

    Returns:
        numpy.array: Cleaned array as BoW

    """
    sentence_vector_lemmatized = lemmatize(sentence_vector, nlp_language)
    token_vector = tokenize_sentence(sentence_vector_lemmatized)
    token_vector_whitespace = strip_whitespace(token_vector)
    token_vector_lowercase = lowercase(token_vector_whitespace)
    token_vector_punctuation = remove_punctuation(token_vector_lowercase)
    token_vector_stopwords = remove_stopwords(token_vector_punctuation, stopwords_language)
    token_vector_preprocessed = remove_numbers(token_vector_stopwords)

    return token_vector_preprocessed


@timer
def create_cleaned_text(sentence_vector):
    """ Function combine cleaning function for text-based features

    Args:
        sentence_vector (numpy.array): Array containing text


    Returns:
        numpy.array: Cleaned array as BoW

    """
    token_vector = tokenize_sentence(sentence_vector)
    token_vector_whitespace = strip_whitespace(token_vector)
    token_vector_lowercase = lowercase(token_vector_whitespace)

    return token_vector_lowercase


@timer
def number_punctuations_total(sentence_vector):
    """ Function to generate the number of all punctuation marks in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array

       Returns:
           numpy.array: Array containing the total number of punctuation marks

       """
    # get the list of punctuation marks from the string package
    list_pm = list(string.punctuation)
    # Drop the end of sentence points, since it is not an differentiator between two sentences. And the data set may
    # translate two sentences or more into one.
    list_pm.remove('.')
    list_pm.append('...')

    return sentence_vector.apply(lambda sentence: len([word for word in sentence if word in list_pm]))


@timer
def number_words(sentence_vector):
    """ Function to generate the number of words in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array

       Returns:
           numpy.array: Array containing the total number of words

       """
    return sentence_vector.apply(
        lambda sentence: len([word for word in sentence if word not in string.punctuation]))


@timer
def number_unique_words(sentence_vector):
    """ Function to generate the number of unique words in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array

       Returns:
           numpy.array: Array containing the total number of unique words

       """
    return sentence_vector.apply(
        lambda sentence: len(np.unique([word for word in sentence if word not in string.punctuation])))


@timer
def number_punctuation_marks(sentence_vector, punctuation_mark):
    """ Function to generate the number of a given punctuation mark in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array
           punctuation_mark (str): Punctuation mark of interest

       Returns:
           numpy.array: Array containing the total number of this punctuation mark

       """
    return sentence_vector.apply(lambda sentence: len([word for word in sentence if word == punctuation_mark]))


@timer
def number_characters(sentence_vector):
    """ Function to generate the number of characters in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array

       Returns:
           numpy.array: Array containing the total number of characters

       """
    return sentence_vector.apply(lambda sentence:
                                 np.sum([len(word) for word in sentence if word not in string.punctuation]))


@timer
def average_characters(character_vector, word_vector):
    """ Function to generate the number of characters per word in a given vector of BoW-Sentences.

       Args:
           character_vector (numpy.array): array containing the amount of characters
           word_vector (numpy.array): array containing the amount of words

       Returns:
           numpy.array: Array containing the average amount of characters per word

       """
    return (character_vector / word_vector).replace(np.nan, 0).replace(np.inf, 0).replace(np.log(0), 0)


@timer
def number_pos(sentence_vector, nlp_language, pos):
    """ Function to generate the number of a given part-of-speech tag in a given vector of BoW-Sentences.

       Args:
           sentence_vector (numpy.array): BoW array
           nlp_language (str): Language of the array
           pos: a given part-of-speech tag

       Returns:
           numpy.array: Array containing the total number of a given part-of-speech tag

       """
    return sentence_vector.apply(lambda sentence: len([token for token in nlp_language(sentence) if token.pos_ == pos]))


@timer
def number_times(sentence_vector, nlp_language, tense):
    """ Function to generate the number of a given tense verb tag in a given vector of BoW-Sentences.

    Args:
           sentence_vector (numpy.array): BoW array
           nlp_language (str): Language of the array
           tense: a given verb tense tag

    Returns:
           numpy.array: Array containing the total number of verbs in a given tense

    """
    return sentence_vector.apply(lambda sentence: len([token for token in nlp_language(sentence) if token.morph.get(
        "Tense") == tense]))


@timer
def polarity(sentence_vector, textblob_language):
    """ Function to generate the polarity in a given vector of BoW-sentences

       Args:
           sentence_vector (numpy.array): BoW array
           textblob_language (str): Language of the array

       Returns:
           numpy.array: Array containing the polarity (sentiment analyses)

       """
    return sentence_vector.apply(lambda sentence: textblob_language(sentence).sentiment.polarity)


@timer
def subjectivity(sentence_vector, textblob_language):
    """ Function to generate the subjectivity in a given vector of BoW-sentences

        Args:
            sentence_vector (numpy.array): BoW array
            textblob_language (str): Language of the array

        Returns:
            numpy.array: Array containing the subjectivity (sentiment analyses)

        """
    return sentence_vector.apply(lambda sentence: textblob_language(sentence).sentiment.subjectivity)


@timer
def number_stopwords(sentence_vector, stopwords_language):
    """ Function to generate the number of stopwords in a given vector of BoW-Sentences.

        Args:
            sentence_vector (numpy.array): BoW array
            stopwords_language (str): Stopwords in the language of the array

        Returns:
            numpy.array: Array containing the total number of stopwords in a given language

        """
    return sentence_vector.apply(lambda sentence: len([word for word in sentence if word in stopwords_language]))


# def named_entities(sentence_vector, nlp_language):
#     """ unction to generate the subjectivity in a given vector of BoW-sentences
#
#         Args:
#             sentence_vector (numpy.array): BoW array
#             nlp_language (str): Language of the array
#
#         Returns:
#             numpy.array: Array containing the total number of named entities in a given language
#
#         """
#     return sentence_vector.apply(
#         lambda sentence: [name for name in nlp_language(sentence).ents])

@timer
def named_numbers(token_vector):
    """ Function to remove numbers out of an array of sentences

        Args:
            token_vector (numpy.array): Array containing tokenized, lowercased sentence

        Returns:
            numpy.array: Array containing tokenized sentence removed numbers

        """
    return token_vector.apply(lambda sentence: re.findall(r'\d+', sentence))


@timer
def load_embeddings(embedding_array_path,
                    embedding_dictionary_path):
    with open(embedding_array_path, 'rb') as fp:
        embedding_array = pickle.load(fp)
    with open(embedding_dictionary_path, 'rb') as fp:
        embedding_dictionary = pickle.load(fp)

    def normalize_array(array):
        norms = np.sqrt(np.sum(np.square(array), axis=1))
        norms[norms == 0] = 1
        norms = norms.reshape(-1, 1)
        array /= norms[:]
        return array

    embedding_array_normalized = normalize_array(np.vstack(embedding_array))

    return embedding_array_normalized, embedding_dictionary


@timer
def pca_embeddings(embedding_array_normalized, k=10):
    pca = PCA(n_components=k)
    principalComponents = pca.fit_transform(embedding_array_normalized)
    return np.asarray(principalComponents)


@timer
def word_embeddings(token_vector, embedding_array, embedding_dictionary):
    """ Function to create embeddings for the preprocessed words.

       Args:
           token_vector (numpy.array): Array containing text
           embedding_array (array): Path to the embedding array
           embedding_dictionary (dictionary): Path to the embedding dictionary

       Returns:
           pandas.Dataframe: Array containing arrays of the embeddings

       """

    def token_list_embedding(embedding_array, embedding_dictionary, token_list):
        """ Function to retrieve the embeddings from the array
        """
        word_embedding_dictionary = {}
        for i in range(len(token_list)):
            if embedding_dictionary.get(token_list[i]):
                word_embedding_dictionary[token_list[i]] = embedding_array[
                    embedding_dictionary.get(token_list[i])].tolist()
        embedding_dataframe = pd.DataFrame(word_embedding_dictionary)
        return embedding_dataframe

    return token_vector.apply(lambda token_list: token_list_embedding(embedding_array, embedding_dictionary,
                                                                      token_list))


@timer
def create_translation_dictionary(token_vector_source, token_vector_target,
                                  embedding_array_normalized_source, embedding_dictionary_source,
                                  embedding_array_normalized_target, embedding_dictionary_target):
    unique_token_source = set([item for sublist in token_vector_source for item in sublist])
    unique_token_target = set([item for sublist in token_vector_target for item in sublist])

    source_index = 0
    word_embedding_dictionary_source = {}
    embedding_subset_dictionary_source = {}
    for token in unique_token_source:
        if embedding_dictionary_source.get(token):
            word_embedding_dictionary_source[token] = embedding_array_normalized_source[
                embedding_dictionary_source.get(token)].tolist()
            embedding_subset_dictionary_source[source_index] = token
            source_index += 1

    target_index = 0
    word_embedding_dictionary_target = {}
    embedding_subset_dictionary_target = {}
    for token in unique_token_target:
        if embedding_dictionary_target.get(token):
            word_embedding_dictionary_target[token] = embedding_array_normalized_target[
                embedding_dictionary_target.get(token)].tolist()
            embedding_subset_dictionary_target[target_index] = token
            target_index += 1

    embedding_subset_source = np.array(list(word_embedding_dictionary_source.values()))
    embedding_subset_target = np.array(list(word_embedding_dictionary_target.values()))

    def translation(token, word_embedding_dictionary_source, embedding_subset_target,
                    embedding_subset_dictionary_target):
        norm_src_word_emb = word_embedding_dictionary_source[token]
        similarity_cos = np.dot(norm_src_word_emb, np.transpose(embedding_subset_target))
        most_similar_trg_index = np.argsort(-similarity_cos)[0].tolist()
        return embedding_subset_dictionary_target[most_similar_trg_index]

    translation_to_target_source = {}
    for token in unique_token_source:
        if embedding_dictionary_source.get(token):
            translation_to_target_source[token] = translation(token, word_embedding_dictionary_source,
                                                              embedding_subset_target,
                                                              embedding_subset_dictionary_target)

    translation_to_source_target = {}
    for token in unique_token_target:
        if embedding_dictionary_target.get(token):
            translation_to_source_target[token] = translation(token, word_embedding_dictionary_target,
                                                              embedding_subset_source,
                                                              embedding_subset_dictionary_source)

    return translation_to_target_source, translation_to_source_target


@timer
def translate_words(token_vector, translation_dictionary):
    def calculate_translations(word_list, translation_dictionary):
        translation_list = []
        for word in word_list:
            try:
                translation_list.append(translation_dictionary[word])
            except KeyError:
                continue
        return translation_list

    return token_vector.apply(lambda token_list: calculate_translations(token_list, translation_dictionary))

@timer
def sentence_embedding_average(embedding_token_vector):
    """ Function to create average sentence embedding
       Args:
           embedding_token_vector (numpy.array): Array containing embedding array of the token

       Returns:
           numpy.array: Array containing average of the embeddings
       """
    return embedding_token_vector.apply(lambda embedding_token: [embedding_token.mean(axis=1)])


@timer
def tf_idf_vector(token_vector):
    def identity_tokenizer(text):
        return text

    vectorizer = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False)
    vectors = vectorizer.fit_transform(token_vector)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df_tf_idf = pd.DataFrame(denselist, columns=feature_names)
    return df_tf_idf.to_dict(orient='records')


@timer
def sentence_embedding_tf_idf(embedding_array_dataframe, tf_idf_dict_vec):
    """ Function to create tf-idf weighted sentence embedding

        Args:
            token_vector (numpy.array): Array containing text
            embedding_array (array): Path to the embedding array
            embedding_dictionary (dictionary): Path to the embedding dictionary

        Returns:
            numpy.array: Array containing tf-idf weighted embedding
        """
    df = pd.DataFrame()
    df['embedding_array_vec'] = embedding_array_dataframe
    df['tf_idf_dict_vec'] = tf_idf_dict_vec

    def aggregate_tf_idf_embedding(embedding_dataframe, tf_idf_dict):
        for i in range(embedding_dataframe.shape[1]):
            embedding_dataframe[embedding_dataframe.columns[i]] = embedding_dataframe[embedding_dataframe.columns[i]] * \
                                                                  tf_idf_dict[embedding_dataframe.columns[i]]
        return [pd.Series(embedding_dataframe.values.mean(axis=1))]

    weighted_average = df.apply(lambda x: aggregate_tf_idf_embedding(x.embedding_array_vec, x.tf_idf_dict_vec), axis=1)

    return weighted_average
