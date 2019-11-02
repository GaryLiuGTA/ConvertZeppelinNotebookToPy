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

    
