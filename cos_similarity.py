
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, string, numpy
# import MySQLdb as mysql
# db = mysql.connect(
#                    user='medpay',
#                    passwd='meddiPASSpay4',
#                    db='medpay')
# cur = db.cursor()

# query = "select distinct HCPCS_DESCRIPTION from medicareMaster limit 5;"

# cur.execute(query)

# documents = cur.fetchall()
lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

documents = open('descriptions.txt', 'r').readlines()
documents = [x.strip() for x in documents] 

print("\nEXAMPLES:\n")
for i in range(100, 105):
  print(documents[i])
print('\n')

input = input('Description: ')
input = input.strip()

documents.append(input)
index = len(documents) - 1
# index = 0
# for i in range(0, len(documents)):
#   if (documents[i] == input):
#     index = i
#     break


TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
def cos_similarity(textlist):
    tfidf = TfidfVec.fit_transform(textlist)
    # return tfidf
    return (tfidf * tfidf.T).toarray()

similarity = cos_similarity(documents)

sim_d = similarity[index]
sim_d = [(index, s) for (index, s) in enumerate(sim_d)]

sim_d = sorted(sim_d, key = lambda x: x[1], reverse = True)
sim_d = sim_d[0:10]
for i, s in sim_d:
  print("(" + str(i) + ") " + documents[i])
  print("score " + str(s) + "\n")