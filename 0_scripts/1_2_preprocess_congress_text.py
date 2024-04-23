# Script to preprocess political texts:
# 1. Expands word contractions 
# 2. Removes stopwords and procedural words
# 3. Converts to lower case
# 4. Converts punctuations to white space
# 5. Tokenizes the text 
# 6. Only considers tokens that appear more than two times, not blanks, and not digits.
# 7. Replaces raw text with preprocessed text as the last column.
# Adapted from Rheault & Cochrane (2020)

from nltk.tokenize import ToktokTokenizer
import string
from sklearn.feature_extraction import text
from functools import reduce
import unicodedata
import pathlib

# Set path to folder that contains the text data working directory
proj_dir = pathlib.Path.cwd()

# Initiaze Tokenizer
tk = ToktokTokenizer()

stopwords = ['member','members','president',
    'hon','parliament','house','ask','asked','asks','question','questioned','questions','bills','bill',
    'party','parties','mp','mps','sir','madam','mr','gentleman','gentlemen','lady','ladies',
    'speaker','chair','motion','motions','vote','votes','order','yes','deputy','secretary',
    'chairman','chairwoman',
    'america','usa','american','americans',
    'pursuant','supply','supplementary','please','friend','s',
    'clause','amendment','i','ii','iii','section','sections', 'colleague', 'colleagues'] + list(text.ENGLISH_STOP_WORDS)

# For replacement of contractions.
contractions = {"you'd": 'you would', "he'd": 'he would', "she's": 'she is', "where'd": 'where did', "might've": 'might have', "he'll": 'he will', "they'll": 'they will',  "mightn't": 'might not', "you'd've": 'you would have', "shan't": 'shall not', "it'll": 'it will', "mayn't": 'may not', "couldn't": 'could not', "they'd": 'they would', "so've": 'so have', "needn't've": 'need not have', "they'll've": 'they will have', "it's": 'it is', "haven't": 'have not', "didn't": 'did not', "y'all'd": 'you all would', "needn't": 'need not', "who'll": 'who will', "wouldn't've": 'would not have', "when's": 'when is', "will've": 'will have', "it'd've": 'it would have', "what'll": 'what will', "that'd've": 'that would have', "y'all're": 'you all are', "let's": 'let us', "where've": 'where have', "o'clock": 'oclock', "when've": 'when have', "what're": 'what are', "should've": 'should have', "you've": 'you have', "they're": 'they are', "aren't": 'are not', "they've": 'they have', "it'd": 'it would', "i'll've": 'i will have', "they'd've": 'they would have', "you'll've": 'you will have', "wouldn't": 'would not', "we'd": 'we would', "hadn't've": 'had not have', "weren't": 'were not', "i'd": 'i would', "must've": 'must have', "what's": 'what is', "mustn't've": 'must not have', "what'll've": 'what will have', "ain't": 'aint', "doesn't": 'does not', "we'll": 'we will', "i'd've": 'i would have', "we've": 'we have', "oughtn't": 'ought not', "you're": 'you are', "who'll've": 'who will have', "shouldn't": 'should not', "can't've": 'cannot have', "i've": 'i have', "couldn't've": 'could not have', "why've": 'why have', "what've": 'what have', "can't": 'cannot', "don't": 'do not', "that'd": 'that would', "who's": 'who is', "would've": 'would have', "there'd": 'there would', "shouldn't've": 'should not have', "y'all": 'you all', "mustn't": 'must not', "she'll": 'she will', "hadn't": 'had not', "won't've": 'will not have', "why's": 'why is', "'cause": 'because', "wasn't": 'was not', "shan't've": 'shall not have', "ma'am": 'madam', "hasn't": 'has not', "to've": 'to have', "how'll": 'how will', "oughtn't've": 'ought not have', "he'll've": 'he will have', "we'd've": 'we would have', "won't": 'will not', "could've": 'could have', "isn't": 'is not', "she'll've": 'she will have', "we'll've": 'we will have', "you'll": 'you will', "who've": 'who have', "there's": 'there is', "y'all've": 'you all have', "we're": 'we are', "i'll": 'i will', "i'm": 'i am', "how's": 'how is', "she'd've": 'she would have', "sha'n't": 'shall not', "there'd've": 'there would have', "he's": 'he is', "it'll've": 'it will have', "that's": 'that is', "y'all'd've": 'you all would have', "he'd've": 'he would have', "how'd": 'how did', "where's": 'where is', "so's": 'so as', "she'd": 'she would', "mightn't've": 'might not have'}

def strip_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def clean_text(text):
    text = reduce(lambda a, kv: a.replace(*kv), contractions.items(), text.lower())
    text = text.replace('\t',' ').replace('\n',' ').replace('\r',' ')
    text = strip_accents(text)
    text = text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    tokens = tk.tokenize(text)
    tokens = [w for w in tokens if w not in stopwords and len(w)>2 and w!=' ' and not w.isdigit()]
    return ' '.join(tokens)


# new_text = "I see there's a lot ofimmigration going on in this area"
# match = re.search(r'\bimmigr\w*', new_text)
# if match: 
#     print("Pattern found.")
# else: 
#     print("Pattern not found.")

if __name__=="__main__":

    # Adjust path
    inpath = proj_dir/'2_build'/'congress.txt'
    outpath = proj_dir/'2_build'/'preprocessed_congress.txt'

    # Preprocessing file and saving as column #10.
    with open(outpath, 'w') as out_:
        with open(inpath, 'r') as infile_:
            idx=0
            for line in infile_:
                row_content = line.rstrip().split('\t')
                text = row_content[2]
                new_text = clean_text(text)
                if new_text!='':
                    out_.write(
                        row_content[0] + '\t' +        # Session
                        row_content[1] + '\t' +        # Speech ID, and skip the third column (i.e. the raw text), proceed to the rest 
                        row_content[3] + '\t' +        # Speaker ID
                        row_content[4] + '\t' +        # Speaker name
                        row_content[5] + '\t' +        # Chamber
                        row_content[6] + '\t' +        # State
                        row_content[7] + '\t' +        # Party
                        row_content[8] + '\t' +        # Majority
                        row_content[9] + '\t' +        # President
                        new_text + '\n'                # New preprocessed speech
                    )
                idx+=1
                if idx%100000==0:
                    print("Processed %d lines." %idx)