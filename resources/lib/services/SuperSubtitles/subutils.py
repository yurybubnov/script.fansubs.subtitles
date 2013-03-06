# coding=iso-8859-2
import re
import os

def lang_hun2eng(hunlang):
  languages = {
            

    "alb�n"              :  "Albanian",
    "arab"               :  "Arabic",
    "bolg�r"             :  "Bulgarian",
    "k�nai"              :  "Chinese",
    "horv�t"             :  "Croatian",
    "cseh"               :  "Czech",
    "d�n"                :  "Danish",
    "holland"            :  "Dutch",
    "angol"              :  "English",
    "�szt"               :  "Estonian",
    "finn"               :  "Finnish",
    "francia"            :  "French",
    "n�met"              :  "German",
    "g�r�g"              :  "Greek",
    "h�ber"              :  "Hebrew",
    "hindi"              :  "Hindi",
    "magyar"             :  "Hungarian",
    "olasz"              :  "Italian",
    "jap�n"              :  "Japanese",
    "koreai"             :  "Korean",
    "lett"               :  "Latvian",
    "litv�n"             :  "Lithuanian",
    "maced�n"            :  "Macedonian",
    "norv�g"             :  "Norwegian",
    "lengyel"            :  "Polish",
    "portug�l"           :  "Portuguese",
    "rom�n"              :  "Romanian",
    "orosz"              :  "Russian",
    "szerb"              :  "Serbian",
    "szlov�k"            :  "Slovak",
    "szlov�n"            :  "Slovenian",
    "spanyol"            :  "Spanish",
    "sv�d"               :  "Swedish",
    "t�r�k"              :  "Turkish",

  }
  return languages[ hunlang.lower() ] 

def clean_title(title):
    for char in ['[', ']', '_', '(', ')','.','-', '  ', '  ', '  ']: 
       title = title.replace(char, ' ')
    title = title.strip()
    return title
  
  
def filename_match_exact(movie_file, sub_file):
    movie_file = os.path.basename(movie_file).lower()
    sub_file = os.path.basename(sub_file).lower()
    i = movie_file.rfind(".")
    if i > 0: movie_file = movie_file[:i]
    movie_file = clean_title(movie_file)
    sub_file = clean_title(sub_file)
    return sub_file.startswith(movie_file)
    
  
def filename_match_tvshow(movie_file, sub_file):
    regex_expressions = [ '[Ss]([0-9]+)[][._-]*[Ee]([0-9]+)([^\\\\/]*)$',
                        '[\._ \-]([0-9]+)x([0-9]+)([^\\/]*)',                     # foo.1x09 
                        '[\._ \-]([0-9]+)([0-9][0-9])([\._ \-][^\\/]*)',          # foo.109
                        '([0-9]+)([0-9][0-9])([\._ \-][^\\/]*)',
                        '[\\\\/\\._ -]([0-9]+)([0-9][0-9])[^\\/]*',
                        'Season ([0-9]+) - Episode ([0-9]+)[^\\/]*',
                        '[\\\\/\\._ -][0]*([0-9]+)x[0]*([0-9]+)[^\\/]*',
                        '[[Ss]([0-9]+)\]_\[[Ee]([0-9]+)([^\\/]*)'                 #foo_[s01]_[e01]
                        '[\._ \-][Ss]([0-9]+)[\.\-]?[Ee]([0-9]+)([^\\/]*)'        #foo, s01e01, foo.s01.e01, foo.s01-e01
                        ]
    sub_info = ""
    is_tvshow = 0
   
    for regex in regex_expressions:
        movie_matches = re.findall(regex, movie_file)                  
        if len(movie_matches) > 0 : 
            is_tvshow = 1
            break
    
    if (is_tvshow == 0): return False
        
    for regex in regex_expressions:       
        sub_matches = re.findall(regex, sub_file)
        if len(sub_matches) > 0 :
            if ((int(sub_matches[0][0]) == int(movie_matches[0][0])) and (int(sub_matches[0][1]) == int(movie_matches[0][1]))):
                return True

    return False

def remove_parenthesized_parts(str):
    removed = ""
    while True:
        parenth = re.search("\([^\)]+\)", str)
        if not parenth: break
        begin, end = parenth.span()
        removed = removed + parenth.group(0)
        str = str[:begin] + str[end:]
    return str, removed

