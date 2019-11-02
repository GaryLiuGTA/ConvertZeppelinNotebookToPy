import json
import codecs
from os import path

source_files = [r'C:\Users\t926528\Downloads\T926528_AdHoc_DAL_Testing.json', r'C:\Users\t926528\Downloads\_T926528_RTM_Manual.json']
extract_language = ['python', 'markdown']

for source_file in source_files:
    wrong_files = []
    if path.exists(source_file):        
        notebook = json.load(codecs.open(source_file, 'r', 'utf-8-sig'))
        cell_script = []
        script = ''
        for i in notebook['paragraphs']:
            language = i['config']['editorSetting']['language']
            code = i['text'].splitlines()
            if extract_language == None:
                languageFilter = True
            else:
                languageFilter = (language in extract_language)

            if languageFilter:
                para =code[1:]
                if len(para)>0:
                    if language == 'markdown':
                        para = '# ===================Markdown===================\n# '+'\n# '.join(para) + '\n# ================Markdown End=================='
                    else:
                        para = '\n'.join(para)
                    cell_script.append(para)
                    if 'results' in i.keys():
                        results = i['results']
                        if results['code'] == 'SUCCESS' and results['msg'][0]['type'] == 'TEXT':
                            cell_script.append('#===============Code Results================\n#' + results['msg'][0]['data'].replace('\n', '\n#') + '\n#===============End Results================')
        script = '\n\n'.join(cell_script)
        
        output_file = path.basename(source_file)
        output_path = source_file.replace(output_file, '')
        _, ext = path.splitext(source_file)
        if len(ext) > 0:
            output_file = output_file[:-len(ext)]
        output_file = output_path + output_file + '.py'
        
        j = 0
        while path.exists(output_file):
            if j-1 < 0:
                output_file = output_file[:-3]
            else:
                output_file = output_file[:-3][:-len(str(j-1))]
            output_file = output_file + str(j) + '.py'        
            j +=1
    #     output_file = output_path + output_file
        with open(output_file, 'w') as f:
            f.write(script)
    else:
        wrong_files.append(source_file)
if len(wrong_files) > 0:
    print(f'The following file(s) were not successfully exported due to file path error:')
    print('\n'.joint(wrong_files))

    
from spellchecker import SpellChecker
spell = SpellChecker()

def shuffle(char_list):
    #     if len(char_list) == 2:
#         if char_list[0] == char_list[1]:
#             return([[char_list[0], char_list[1]]])
#         else:
#             return([[char_list[0], char_list[1]],[char_list[1], char_list[0]]])
    if len(char_list) == 1:
        return([char_list])
    else:
        shuffle_list = []
        for char in set(char_list):
            sub_char_list = char_list[:char_list.index(char)]+char_list[char_list.index(char)+1:]
            for char_shuffled in shuffle(sub_char_list):
                shuffle_list.append([char] + char_shuffled)
    return(shuffle_list)
def generate_sub_list(char_list, size = 1):
    if size == 1:
        return([[char] for char in set(char_list)])
    else:
        sub_lists = []
        used_chars = []
        for char in set(char_list):
            sub_list = char_list[:char_list.index(char)]+char_list[char_list.index(char)+1:]
            for used_char in used_chars:
                sub_list = sub_list.replace(used_char, '')
            for clist in generate_sub_list(sub_list, size - 1):
                sub_lists.append([char] + clist)
            used_chars.append(char)
    return(sub_lists) 
def shuffle_all(char_list, min_n = 2, max_n = None):
    words = []
    if max_n is None:
        max_n = len(char_list)
    for i in range(min_n, max_n+1):
        sub_char_lists = generate_sub_list(char_list, i)
        for sub_char_list in sub_char_lists:
            for word in [''.join(chars) for chars in shuffle(sub_char_list)]:
                words.append(word)
    return(words)


words = shuffle_all('igbnne', 4, 7)
for word in sorted(words):
    for i in range(4, 7):
        if (
            len(word) == i #and
#             word[-2] == 'e' and 
#             word[1] == 'r'
           ):
            if spell.known([word]):
                print(word)