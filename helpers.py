from deep_translator import GoogleTranslator


def translate(sentence, source, target):
    translation_result = GoogleTranslator(
        source=source, target=target).translate(sentence)
    return translation_result
