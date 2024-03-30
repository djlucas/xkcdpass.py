#!/usr/bin/env python3
import random
import os
import argparse
import math
import sys

def set_template_vals(template):
  global num_words, word_len_min, word_len_max, case_trans
  global separators, pad_digits_pre, pad_digits_post
  global padding_type, pad_to_length, padding_chars
  global padding_chars_pre, padding_chars_post
  match template:
    case 'STD':
      num_words          = 3
      word_len_min       = 4
      word_len_max       = 6
      case_trans         = "capitalize"
      separators         = "@%^&*_+~?'/"
      pad_digits_pre     = 0
      pad_digits_post    = 2
      padding_type       = "fixed"
      pad_to_length      = 0
      padding_chars      = "!@$%^&=~?"
      padding_chars_pre  = 1
      padding_chars_post = 1
    case 'WSE':
      num_words          = 2
      word_len_min       = 5
      word_len_max       = 6
      case_trans         = "capitalize"
      separators         = "!#$^*-_=+"
      pad_digits_pre     = 0
      pad_digits_post    = 2
      padding_type       = "adapt"
      pad_to_length      = 16
      padding_chars      = "!#$^*=+"
      padding_chars_pre  = 0
      padding_chars_post = 0
    case 'ALT':
      num_words          = 3
      word_len_min       = 4
      word_len_max       = 6
      case_trans         = "capitalize"
      separators         = ""
      pad_digits_pre     = 2
      pad_digits_post    = 0
      padding_type       = "fixed"
      pad_to_length      = 0
      padding_chars      = "!@$%^&*+=~?"
      padding_chars_pre  = 0
      padding_chars_post = 2
    case 'STR':
      num_words          = 3
      word_len_min       = 5
      word_len_max       = 9
      case_trans         = "capitalize"
      separators         = "!@$%^&*-_+=|~?"
      pad_digits_pre     = 3
      pad_digits_post    = 3
      padding_type       = "fixed"
      pad_to_length      = 0
      padding_chars      = "!@$%^&*_+=~?"
      padding_chars_pre  = 2
      padding_chars_post = 2
    case _:
      print("The preset '" + preset + "' is not valid. Proceeding with the 'STD' preset...")
      set_params(STD)

def set_case_trans(case_trans, wordlist):
  new_wordlist = []
  match case_trans:
    case 'alternating':
      t = 0
      for word in wordlist:
        if t == 1:
          new_word = word.upper()
          t = 0
        else:
          new_word = word.lower()
          t = 1
        new_wordlist.append(new_word)
    case 'upper':
      for word in wordlist:
        new_word = word.upper()
        new_wordlist.append(new_word)
    case 'lower':
      for word in wordlist:
        new_word = word.lower()
        new_wordlist.append(new_word)
    case 'random':
      for word in wordlist:
        new_word = ""
        for letter in word:
          docap = random.choice('01')
          if docap == '0':
            new_word = new_word + letter.lower()
          else:
            new_word = new_word + letter.upper()
        new_wordlist.append(new_word)
    case 'capitalize':
      for word in wordlist:
        new_word = word.capitalize()
        new_wordlist.append(new_word)
    case 'as-is':
      new_wordlist = wordlist
  return new_wordlist

def get_separator(separators):
  separator = random.choice(separators)
  return separator

def get_padding(padding_chars):
  padding_char = random.choice(padding_chars)
  return padding_char

def get_pad_digits(num):
  count = 1
  new_string = ""
  while count <= num:
    new_num = random.choice('0123456789')
    new_string = new_string + new_num
    count += 1
  return new_string

def find_dict():
  common_word_files = ["/usr/share/dict/xkcdpass.txt",
                       "/usr/share/cracklib/cracklib-dict",
                       "/usr/share/dict/words"]
  for file in common_word_files:
    if os.path.isfile(file):
      return file

def get_wordlist(dictionary, word_len_min, word_len_max, num_words):
  if word_len_min < 1:
    sys.stderr.write("ERROR:The minimum length cannot be 0\n")
    sys.exit(1)
  words = []
  with open(dictionary) as wordlist:
    for line in wordlist:
      new_word = line.strip()
      if not "'" in new_word:
        if len(new_word) <= word_len_max:
          if len(new_word) >= word_len_min:
            words.append(new_word)
  wordlist = random.choices(words, k = num_words)
  return wordlist

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dictionary",
                    type=str,
                    help="optional wordlist (one word per line)",
                    metavar="PATH")
parser.add_argument("-t", "--template",
                    type=str,
                    choices=['STD', 'WSE', 'ALT', 'STR'],
                    help="Use a predefined template [STD|WSE|ALT|STR]",
                    metavar="VAL")
parser.add_argument("-N", "--passcount",
                    default = 3,
                    type=int,
                    help="Number of password options to return",
                    metavar="NUM")
parser.add_argument("-n", "--numwords",
                    type=int,
                    help="Number of words in password",
                    metavar="NUM")
parser.add_argument("-m", "--minlength",
                    type=int,
                    help="Minumum length of words",
                    metavar="NUM")
parser.add_argument("-M", "--maxlength",
                    type=int,
                    help="Maximum length of words",
                    metavar="NUM")
parser.add_argument("-c", "--casetransform",
                    type=str,
                    choices=['alternating', 'upper', 'lower', 'random', 'capitalize', 'as-is'],
                    help="Method: [upper|lower|random|capitalize|as-is]",
                    metavar="VAL")
parser.add_argument("-s", "--separators",
                    type=str,
                    help="One or more characters used as a separator",
                    metavar="STRING")
parser.add_argument("-p", "--paddigitspre",
                    type=int,
                    help="Number of padding digits at the start of the password",
                    metavar="NUM")
parser.add_argument("-P", "--paddigitspost", 
                    type=int,
                    help="Number of padding digits at the end of the password",
                    metavar="NUM")
parser.add_argument("-T", "--paddingtype",
                    type=str,
                    choices=['adapt', 'fixed'],
                    help="Select the padding characters type: [adapt|fixed]",
                    metavar="VAL")
parser.add_argument("-C", "--paddingchars", 
                    type=str,
                    help="One or more characters used for pre or post padding",
                    metavar="STRING")
parser.add_argument("-l", "--padtolength",
                    type=int,
                    help="Length of final password if using adapt pad type",
                    metavar="NUM")
parser.add_argument("-x", "--padcharspre",
                    type=int,
                    help="Number of padding chars at the start of the password",
                    metavar="NUM")
parser.add_argument("-X", "--padcharspost",
                    type=int,
                    help="Number of padding chars at the end of the password",
                    metavar="NUM")
args = parser.parse_args()

if args.dictionary:
  dictionary = args.dictionary
else:
  dictionary = find_dict()

# Arguments should override templates, so just
# get set the template values right off the bat
if args.template:
  template = args.template
else:
  template = 'STD'
set_template_vals(template)

passcount = args.passcount

if args.numwords:
  num_words = args.numwords

if args.minlength:
  word_len_min = args.minlength

if args.maxlength:
  word_lin_max = args.maxlength

if args.casetransform:
  case_trans = args.casetransform

if args.separators:
  separators = args.separators

if args.paddigitspre:
  pad_digits_pre = args.paddigtspre

if args.paddigitspost:
  pad_digits_post = args.paddigitspost

if args.paddingtype:
  padding_type = args.paddingtype

if args.padtolength:
  pad_to_length = args.padtolength

if args.paddingchars:
  padding_chars = args.paddingchars

if args.padcharspre:
  padding_chars_pre = args.padcharspre

if args.padcharspost:
  padding_chars_post = args.padcharspost

pcount = 1
while pcount <= passcount:
  wordlist = get_wordlist(dictionary, word_len_min, word_len_max, num_words)
  pcount += 1
  transwordlist = set_case_trans(case_trans, wordlist)
