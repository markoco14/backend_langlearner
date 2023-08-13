import pinyin

def convert_to_chinese_with_pinyin(chinese_content):
    content_with_pinyin = []
    for sentence in chinese_content:
        pinyin_sentence = []
        for character in sentence:
            py = pinyin.get(character)
            pinyin_sentence.append({
                "chinese": character,
                "pinyin": ''.join([item for sublist in py for item in sublist])
            })
        content_with_pinyin.append(pinyin_sentence)
    return content_with_pinyin