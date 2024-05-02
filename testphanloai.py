# import pickle, os
# import regex as re
# from sklearn.metrics import classification_report
# from underthesea import word_tokenize
# import unicodedata
# import pandas as pd
# import time

# MODEL_PATH = "C:/Users/Hi/Desktop"

# bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
#                   ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
#                   ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
#                   ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
#                   ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
#                   ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
#                   ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
#                   ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
#                   ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
#                   ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
#                   ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
#                   ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]

# bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

# nguyen_am_to_ids = {}

# for i in range(len(bang_nguyen_am)):
#     for j in range(len(bang_nguyen_am[i]) - 1):
#         nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

# # check sơ thì chưa có chuẩn hóa này từ thư viện nào hết trơn
# def standardize_vietnamese_accents_w(word):
#     if not is_valid_vietnam_word(word):
#         return word

#     chars = list(word)
#     dau_cau = 0
#     nguyen_am_index = []
#     qu_or_gi = False
#     for index, char in enumerate(chars):
#         x, y = nguyen_am_to_ids.get(char, (-1, -1)) # nếu mà không có thì mặc định trả về -1,-1
#         if x == -1:
#             continue
#         elif x == 9:  # check qu
#             if index != 0 and chars[index - 1] == 'q':
#                 chars[index] = 'u'
#                 qu_or_gi = True
#         elif x == 5:  # check gi
#             if index != 0 and chars[index - 1] == 'g':
#                 chars[index] = 'i'
#                 qu_or_gi = True
#         if y != 0:
#             dau_cau = y
#             chars[index] = bang_nguyen_am[x][0]
#         if not qu_or_gi or index != 1:
#             nguyen_am_index.append(index)
#     if len(nguyen_am_index) < 2:
#         if qu_or_gi:
#             if len(chars) == 2:
#                 x, y = nguyen_am_to_ids.get(chars[1])
#                 chars[1] = bang_nguyen_am[x][dau_cau]
#             else:
#                 x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
#                 if x != -1:
#                     chars[2] = bang_nguyen_am[x][dau_cau]
#                 else:
#                     chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
#             return ''.join(chars)
#         return word

#     for index in nguyen_am_index:
#         x, y = nguyen_am_to_ids[chars[index]]
#         if x == 4 or x == 8:  # ê, ơ
#             chars[index] = bang_nguyen_am[x][dau_cau]
#             return ''.join(chars)

#     if len(nguyen_am_index) == 2:
#         if nguyen_am_index[-1] == len(chars) - 1:
#             x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
#             chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
#         else:
#             x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
#             chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
#     else:
#         x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
#         chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
#     return ''.join(chars)


# def is_valid_vietnam_word(word):
#     chars = list(word)
#     nguyen_am_index = -1
#     for index, char in enumerate(chars):
#         x, y = nguyen_am_to_ids.get(char, (-1, -1))
#         if x != -1:
#             if nguyen_am_index == -1:
#                 nguyen_am_index = index
#             else:
#                 if index - nguyen_am_index != 1:
#                     return False
#                 nguyen_am_index = index
#     return True


# def standardize_vietnamese_accents(sentence):
#     words = sentence.split()
#     for index, word in enumerate(words):
#         # ^p{P}* : bắt đầu bằng 0 hoặc nhiều dấu câu
#         # [\p{L}.]*\p{L}+ : tiếp theo là 0 hoặc nhiều ký tự chữ hoặc dấu chấm, sau đó là ít nhất một ký tự chữ
#         # \p{P}*$ : kết thúc bằng 0 hoặc nhiều dấu câu
#         # r'\1/\2/\3' : bắt đầu bằng dấu câu, tiếp theo là từ đã chuẩn hóa, kết thúc bằng dấu câu (là 3 cái dòng trên á)
#         # p{X} là kiểu tìm các ký tự có tính chất X
#             # P : Punctuation (dấu câu), L : Letter (chữ cái) (check trang 5 word elastic)
#         cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
#         if len(cw) == 3:
#             cw[1] = standardize_vietnamese_accents_w(cw[1])
#         words[index] = ''.join(cw)
#     return ' '.join(words)

# def text_preprocess(document):
#     # chuẩn hóa unicode
#     document = unicodedata.normalize('NFC', document)
#     # chuẩn hóa cách gõ dấu tiếng Việt
#     document = standardize_vietnamese_accents(document)
#     # tách từ
#     document = word_tokenize(document, format="text")
#     # đưa về lower
#     document = document.lower()
#     # xóa các ký tự không cần thiết
#     document = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',document)
#     # xóa khoảng trắng thừa
#     document = re.sub(r'\s+', ' ', document).strip()
#     return document

# start_time = time.time()
# data = pd.read_csv("D:/temp/Giải trí.csv")

# sampled_data = data.sample(n=20000)
# sampled_data.to_csv("D:/temp/Giải trí.csv", index=False)

# sampled_data["content"] = sampled_data["content"].apply(text_preprocess)
# print("uow")
# sampled_data.to_csv("D:/temp/Giải trí.csv", index = False)

# end_time = time.time()
# thoi_gian_chay = end_time - start_time
# print("Thời gian chạy đoạn mã:", thoi_gian_chay, "giây")

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle, os
# import time
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline


titles = ["Công nghệ", "Giáo dục", "Giải trí", "Khoa học", "Kinh tế", "Nhà đất", "Pháp luật",
          "Thế giới", "Thể thao", "Văn hóa", "Xe cộ", "Xã hội", "Đời sống"]

titles_train_path = ["D:/KLTN/QLCN/data/train/" + title + ".csv" for title in titles]
titles_test_path = ["D:/KLTN/QLCN/data/test/" + title + ".csv" for title in titles]

def make_data(title_path):
  texts = []
  labels = []
  for path in title_path:
    df = pd.read_csv(path)
    texts.extend(df['content'].tolist())
    labels.extend(df['cate'].tolist())
  return texts, labels

train_text, train_labels = make_data(titles_train_path)
test_text, test_labels = make_data(titles_test_path)

lb_encoder = LabelEncoder()
lb_encoder.fit(train_labels)

# pickle.dump(lb_encoder, open(os.path.join("D:/KLTN/QLCN/data/models", "label_encoder.pkl"), 'wb'))

train_labels = lb_encoder.transform(train_labels)
test_labels = lb_encoder.transform(test_labels)

# print(lb_encoder.classes_)

# MODEL_PATH = "D:/KLTN/QLCN/data/models"

# start_time = time.time()
# text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1,1),
#                                              max_df=0.8,
#                                              max_features=None)), 
#                      ('tfidf', TfidfTransformer()), 
#                      ('clf', MultinomialNB())
#                     ])
# text_clf = text_clf.fit(train_text, train_labels)

# train_time = time.time() - start_time
# print('Done training Naive Bayes in', train_time, 'seconds.')

# # Save model
# pickle.dump(text_clf, open(os.path.join(MODEL_PATH, "naive_bayes.pkl"), 'wb'))

    


# from sklearn.linear_model import LogisticRegression
    
# start_time = time.time()
# text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1,1),
#                                              max_df=0.8,
#                                              max_features=None)), 
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', LogisticRegression(solver='lbfgs', 
#                                                 multi_class='auto',
#                                                 max_iter=10000))
#                     ])
# text_clf = text_clf.fit(train_text, train_labels)

# train_time = time.time() - start_time
# print('Done training Linear Classifier in', train_time, 'seconds.')

# # Save model
# pickle.dump(text_clf, open(os.path.join(MODEL_PATH, "linear_classifier.pkl"), 'wb'))


# from sklearn.svm import SVC

# start_time = time.time()
# text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1,1),
#                                              max_df=0.8,
#                                              max_features=None)), 
#                      ('tfidf', TfidfTransformer()),
#                      ('clf', SVC(gamma='scale'))
#                     ])
# text_clf = text_clf.fit(train_text, train_labels)

# train_time = time.time() - start_time
# print('Done training SVM in', train_time, 'seconds.')

# # Save model
# pickle.dump(text_clf, open(os.path.join(MODEL_PATH, "svm.pkl"), 'wb'))



MODEL_PATH = "D:/KLTN/QLCN/data/models"

# Naive Bayes
model = pickle.load(open(os.path.join(MODEL_PATH,"naive_bayes.pkl"), 'rb'))
y_pred = model.predict(test_text)
print('Naive Bayes, Accuracy =', np.mean(y_pred == test_labels))

# Linear Classifier
model = pickle.load(open(os.path.join(MODEL_PATH,"linear_classifier.pkl"), 'rb'))
y_pred = model.predict(test_text)
print('Linear Classifier, Accuracy =', np.mean(y_pred == test_labels))

# # SVM
# model = pickle.load(open(os.path.join(MODEL_PATH,"svm.pkl"), 'rb'))
# y_pred = model.predict(test_text)
# print('SVM, Accuracy =', np.mean(y_pred == test_labels))



# Xem kết quả trên từng nhãn
from sklearn.metrics import classification_report

nb_model = pickle.load(open(os.path.join(MODEL_PATH,"naive_bayes.pkl"), 'rb'))
y_pred = nb_model.predict(test_text)
print(classification_report(test_labels, y_pred, target_names=list(lb_encoder.classes_)))

from sklearn.metrics import classification_report

lr_model = pickle.load(open(os.path.join(MODEL_PATH,"linear_classifier.pkl"), 'rb'))
y_pred = lr_model.predict(test_text)
print(classification_report(test_labels, y_pred, target_names=list(lb_encoder.classes_)))




