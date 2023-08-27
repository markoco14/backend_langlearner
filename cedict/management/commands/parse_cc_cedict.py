from django.core.management.base import BaseCommand
import time
from cedict.models import Word
# If you decide to save data to your Django database, import the necessary model(s):
# from your_app.models import Word

class Command(BaseCommand):
    help = 'Parse the CC-CEDICT Chinese-English dictionary into a list of dictionaries'

    def parse_line(self, line, list_of_words, lines_not_2, row):
        if line[0] == '#':
            return 0
        
        if line[0] == '%':
            return 0
        # print('base line', line)
        # INITIATE WORD OBJECT TO HOLD DATA
        wordObject = {}
        if line == '':
            return 0
        line = line.rstrip('/')
        split_line = line.split(' /')
        length = len(split_line)
        if length != 2:
            lines_not_2 = lines_not_2 + 1
        # print('split on / line', split_line)
        # print('length of line', length)
        characters = split_line[0]
        # print('characters:', characters)
        trad_simp_pin = split_line[0].split(' [')
        # print('trad_simp_pin:', trad_simp_pin)
        traditional = trad_simp_pin[0].split(" ")[0]
        # print('traditional:', traditional)
        simplified = trad_simp_pin[0].split(" ")[1]
        # print('simplified:', simplified)
        pinyin = trad_simp_pin[1].rstrip(']')
        # print('pinyin:', pinyin)
        english = split_line[1]
        # print('english:', english)
        if row == 181:
            print(simplified)
        

        # APPEND STORED VARIABLES INTO HOLDER OBJECT (wordObject)
        wordObject['traditional'] = traditional
        wordObject['simplified'] = simplified
        wordObject['pinyin'] = pinyin
        wordObject['english'] = english

        # APPEND HOLDER OBJECTS INTO LIST OF WORDS
        list_of_words.append(wordObject)

    def remove_surnames(self, list_of_words):
        for x in range(len(list_of_words)-1, -1, -1):
            if "surname " in list_of_words[x]['english']:
                if list_of_words[x]['traditional'] == list_of_words[x+1]['traditional']:
                    list_of_words.pop(x)

    def handle(self, *args, **kwargs):
        read_start_time = time.time()
        with open('./cedict/management/cedict_ts.u8') as file:
            text = file.read()
            lines = text.split('\n')
            dict_lines = list(lines)
            
        list_of_words = []
        
        self.stdout.write("Parsing dictionary . . .")
        lines_not_2 = 0
        number_of_lines = 1
        row = 1
        for line in dict_lines:
            self.parse_line(line, list_of_words, lines_not_2, row) 
            row = row + 1
            number_of_lines = number_of_lines + 1

        print('lines longer than 2:', lines_not_2)
        print('number of lines:', number_of_lines)

        self.stdout.write("Removing Surnames . . .")
        self.remove_surnames(list_of_words)


        self.stdout.write(self.style.SUCCESS('Done!'))
        read_end_time = time.time()
        read_duration = read_end_time - read_start_time

        write_start_time = time.time()
        # Optional: To save to the Django database (ensure model is created & imported)
        # self.stdout.write("Saving to database (this may take a few minutes) . . .")
        # for one_dict in list_of_words:
        #     new_word = Word(traditional=one_dict["traditional"], 
        #                     simplified=one_dict["simplified"], 
        #                     english=one_dict["english"], 
        #                     pinyin=one_dict["pinyin"])
        #     new_word.save()
        # words = [Word(traditional=word["traditional"], 
        #       simplified=word["simplified"], 
        #       english=word["english"], 
        #       pinyin=word["pinyin"]) for word in list_of_words]

        # Word.objects.bulk_create(words, batch_size=5000)

        write_end_time = time.time()
        write_duration = write_end_time - write_start_time
        print(f"The read took {read_duration:.2f} seconds to run.")
        print(f"The write took {write_duration:.2f} seconds to run.")