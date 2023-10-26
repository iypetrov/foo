import unittest

from src.generation.util import is_valid_model, extract_words_from_model, convert_model_to_snake_case, \
    convert_model_to_kebab_case, \
    convert_word_to_one_starting_with_lower_case, convert_model_to_de_sentence


class TestIsValidModel(unittest.TestCase):

    def test_valid_models(self):
        valid_models = ['Model', 'AnotherModel', 'ValidModelWithOnlyLetters']
        for model in valid_models:
            with self.subTest(model=model):
                result = is_valid_model(model)
                self.assertTrue(result)

    def test_invalid_models(self):
        invalid_models = ['invalidModel', 'invalid_Model', '123InvalidModel', 'invalid_model!', '']
        for model in invalid_models:
            with self.subTest(model=model):
                result = is_valid_model(model)
                self.assertFalse(result)


class TestExtractWordsFromModel(unittest.TestCase):

    def test_empty_string(self):
        result = extract_words_from_model('')
        self.assertEqual(result, [])

    def test_single_word(self):
        result = extract_words_from_model('example')
        self.assertEqual(result, ['example'])

    def test_camel_case(self):
        result = extract_words_from_model('CamelCaseString')
        self.assertEqual(result, ['Camel', 'Case', 'String'])


class TestConvertModelToSnakeCase(unittest.TestCase):

    def test_empty_string(self):
        result = convert_model_to_snake_case('')
        self.assertEqual(result, '')

    def test_single_word(self):
        result = convert_model_to_snake_case('example')
        self.assertEqual(result, 'EXAMPLE')

    def test_multiple_words(self):
        result = convert_model_to_snake_case('CamelCaseString')
        self.assertEqual(result, 'CAMEL_CASE_STRING')


class TestConvertModelToKebabCase(unittest.TestCase):

    def test_empty_string(self):
        result = convert_model_to_kebab_case('')
        self.assertEqual(result, '')

    def test_single_word(self):
        result = convert_model_to_kebab_case('example')
        self.assertEqual(result, 'example')

    def test_multiple_words(self):
        result = convert_model_to_kebab_case('KebabCaseString')
        self.assertEqual(result, 'kebab-case-string')


class TestConvertWordToOneStartingWithLowerCase(unittest.TestCase):

    def test_empty_string(self):
        result = convert_word_to_one_starting_with_lower_case('')
        self.assertEqual(result, '')

    def test_single_word(self):
        result = convert_word_to_one_starting_with_lower_case('example')
        self.assertEqual(result, 'example')

    def test_multiple_words(self):
        result = convert_word_to_one_starting_with_lower_case('SomeFuckedUpString')
        self.assertEqual(result, 'someFuckedUpString')


class TestTranslationToDEFromModel(unittest.TestCase):

    def test_translation(self):
        result = convert_model_to_de_sentence('WeeklyResponsibility')
        self.assertNotEqual(result, '')


if __name__ == '__main__':
    unittest.main()
