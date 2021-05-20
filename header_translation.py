import argparse
import re
from deep_translator import GoogleTranslator

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)


def main():
    input_file = parser.parse_args().file

    input_file = open(input_file, 'r')

    lines = input_file.readlines()
    with open('ENG_pretty_headers.po', 'w', encoding='utf8') as outfile:
        for line in lines:
            if '#: spoonbill/locales/schema.json:1' in lines[lines.index(line)-1]:
                msgstr = line.replace('/', ' ')
                msgstr = re.sub(r"(\w)([A-Z])", r"\1 \2", msgstr).replace('msgid ', '').replace('"', '').strip().title()
                msgstr = f'msgstr "{msgstr}"\n'
                lines[lines.index(line)+1] = msgstr
            outfile.writelines(line)
    outfile.close()

    with open('ES_pretty_headers.po', 'w', encoding='utf8') as outfile:
        for line in lines:
            if '#: spoonbill/locales/schema.json:1' in lines[lines.index(line) - 1]:
                eng = lines[lines.index(line)+1]
                eng = eng.replace('msgstr "', '').replace('"', '').replace('\n', '').split(' ')

                spa = [GoogleTranslator(source='en', target='es').translate(word) for word in eng]

                translated = 'msgstr "'
                for word in spa:
                    translated += word + ' '
                translated = translated.strip() + '"\n'

                lines[lines.index(line) + 1] = translated
            outfile.writelines(line)
    outfile.close()
    input_file.close()


if __name__ == '__main__':
    main()
