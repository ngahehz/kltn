# import json

# def get_icons_color():
#     with open('json-styles/dashboard_style.json', 'r') as file:
#         data = json.load(file)
#     return data["QSettings"][0]["ThemeSettings"][0]["CustomTheme"][0]["Icons-color"]
import numpy as np
import pickle, os
import regex as re
import unicodedata
import py_vncorenlp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

# model_vncore_path = "setting"

if not os.path.exists("models"):
    py_vncorenlp.download_model()
    
if 'rdrsegmenter' not in globals():
    # vncorenlp_path = model_vncore_path + '/VnCoreNLP.jar'
    rdrsegmenter = py_vncorenlp.VnCoreNLP()

MODEL_PATH = "D:/KLTN/QLCN/data/models"

bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                  ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                  ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                  ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                  ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                  ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                  ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                  ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                  ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                  ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                  ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                  ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]

bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

nguyen_am_to_ids = {}

for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

def standardize_vietnamese_accents_w(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = list(word)
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)
    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return ''.join(chars)
        return word

    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            return ''.join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
        else:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    return ''.join(chars)

def is_valid_vietnam_word(word):
    chars = list(word)
    nguyen_am_index = -1
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x != -1:
            if nguyen_am_index == -1:
                nguyen_am_index = index
            else:
                if index - nguyen_am_index != 1:
                    return False
                nguyen_am_index = index
    return True


def standardize_vietnamese_accents(sentence):
    words = sentence.split()
    for index, word in enumerate(words):
        # ^p{P}* : bắt đầu bằng 0 hoặc nhiều dấu câu
        # [\p{L}.]*\p{L}+ : tiếp theo là 0 hoặc nhiều ký tự chữ hoặc dấu chấm, sau đó là ít nhất một ký tự chữ
        # \p{P}*$ : kết thúc bằng 0 hoặc nhiều dấu câu
        # r'\1/\2/\3' : bắt đầu bằng dấu câu, tiếp theo là từ đã chuẩn hóa, kết thúc bằng dấu câu (là 3 cái dòng trên á)
        # p{X} là kiểu tìm các ký tự có tính chất X
            # P : Punctuation (dấu câu), L : Letter (chữ cái) (check trang 5 word elastic)
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        if len(cw) == 3:
            cw[1] = standardize_vietnamese_accents_w(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)

def text_preprocess(document):
    document = document.lower() # phải đưa về chữ thường trước cái tokenization
    document = re.sub(r'https?://\S+', '', document) # bỏ link
    document = re.sub(r'\[\d+(?:,\s?\d+)*\]', '', document) # bỏ số trong ngoặc vuông
    # chuẩn hóa unicode
    document = unicodedata.normalize('NFC', document)
    # tách từ
    document = ' '.join(rdrsegmenter.word_segment(document))
    # bỏ stopword
    document = remove_stopwords(document) # phân loại thì bỏ còn không thì từ từ t tính sau
    # # chuẩn hóa cách gõ dấu tiếng Việt # bỏ đi tại vì cái vncore nó có chuẩn hóa theo kiểu của nó rồi
    # document = standardize_vietnamese_accents(document)
    # xóa các ký tự không cần thiết
    document = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    return document

with open("D:/KLTN/QLCN/data/vietnamese-stopwords-dash.txt", "r", encoding='utf-8') as file:
    stopword_vi_list = file.read().splitlines()
with open("D:/KLTN/QLCN/data/english-stopwords.txt", "r", encoding='utf-8') as file:
    stopword_eng_list = file.read().splitlines()

def remove_stopwords(line):
    words = []
    for word in line.strip().split():
        if word not in stopword_vi_list and word not in stopword_eng_list:
            words.append(word)
    return ' '.join(words)


label_encoder = pickle.load(open(os.path.join(MODEL_PATH,"label_encoder.pkl"), 'rb'))
model1 = pickle.load(open(os.path.join(MODEL_PATH,"svm.pkl"), 'rb'))
model2 = pickle.load(open(os.path.join(MODEL_PATH,"naive_bayes.pkl"), 'rb'))
model3 = pickle.load(open(os.path.join(MODEL_PATH,"linear_classifier.pkl"), 'rb'))


def predict_tag (text):
    text = text_preprocess(text)

    probabilities = model3.predict_proba([text])[0]
    top_labels_indices = probabilities.argsort()[-2:][::-1]
    top_labels = model3.classes_[top_labels_indices]

    top_probabilities = probabilities[top_labels_indices]

    # In ra nhãn và xác suất
    for label, prob in zip(top_labels, top_probabilities):
        print(f"Nhãn: {label}, Xác suất: {prob:.4f}")

    if abs(top_probabilities[0] - top_probabilities[1]) <= 0.3:
        lb = [label_encoder.inverse_transform([x]) for x in top_labels]
        return lb
    elif top_probabilities[0] > top_probabilities[1]:
        return label_encoder.inverse_transform([top_labels[0]])
    else:
        return label_encoder.inverse_transform([top_labels[1]])



def summarizer(text):
    contents = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(contents)  
    if len(contents) <= 10:
        n_clusters = 3 
    elif len(contents) <= 20:
        n_clusters = 5 
    else:
        n_clusters = 7  
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    avg = []
    for j in range(n_clusters):
        idx = np.where(kmeans.labels_ == j)[0]
        avg.append(np.mean(idx))
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    ordering = sorted(range(n_clusters), key=lambda k: avg[k])
    summary = " ".join([contents[closest[idx]] for idx in ordering])

    return summary


















