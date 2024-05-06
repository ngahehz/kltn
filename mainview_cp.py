import pickle, os
import regex as re
from sklearn.metrics import classification_report
from underthesea import word_tokenize
import unicodedata, time

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

def chuan_hoa_dau_tu_tieng_viet(word):
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
            # for index2 in nguyen_am_index:
            #     if index2 != index:
            #         x, y = nguyen_am_to_ids[chars[index]]
            #         chars[index2] = bang_nguyen_am[x][0]
            return ''.join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            # chars[nguyen_am_index[1]] = bang_nguyen_am[x][0]
        else:
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
        # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[2]]]
        # chars[nguyen_am_index[2]] = bang_nguyen_am[x][0]
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


def chuan_hoa_dau_cau_tieng_viet(sentence):
    # sentence = sentence.lower() # chỗ này mà bỏ đi là nó lạ lắm nè
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        # print(cw)
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)

def text_preprocess(document):
    document = document.lower() # phải đưa về chữ thường trước cái tokenization
    document = re.sub(r'https?://\S+', '', document)
    document = re.sub(r'\[\d+(?:,\s?\d+)*\]', '', document)
    # chuẩn hóa unicode
    document = unicodedata.normalize('NFC', document)
    # document = convert_unicode(document)
    # chuẩn hóa cách gõ dấu tiếng Việt
    document = chuan_hoa_dau_cau_tieng_viet(document)
    # tách từ
    document = word_tokenize(document, format="text")
    # xóa các ký tự không cần thiết
    document = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',document)
    # xóa khoảng trắng thừa
    document = re.sub(r'\s+', ' ', document).strip()
    return document

with open("D:/KLTN/QLCN/data/vietnamese-stopwords-dash.txt", "r", encoding='utf-8') as file:
    stopword_list = file.read().splitlines()

def remove_stopwords(line):
    words = []
    for word in line.strip().split():
        if word not in stopword_list:
            words.append(word)
    return ' '.join(words)


label_encoder = pickle.load(open(os.path.join(MODEL_PATH,"label_encoder.pkl"), 'rb'))


# from docx import Document
# file_path = "C:/Users/Hi/Desktop/pj dtmn.docx"
# document = Document(file_path)
# all_text = ""
# for paragraph in document.paragraphs:
#     all_text += paragraph.text + "\n"

# import PyPDF2
# file_path = "C:/Users/Hi/Desktop/9F9B291C-5A9E-11EE-90B6-F71C97318934.pdf" #cái này bất ổn quá
# # file_path = "D:/AI+/Các hệ thống thông minh.pdf"

# with open(file_path, 'rb') as file:
#     reader = PyPDF2.PdfReader(file)
    
#     all_text = ""
#     for page_number in range(len(reader.pages)):
#         page = reader.pages[page_number]
#         all_text += page.extract_text()
        

print("a")
# all_text = """Bắc nồi lên bếp, cho vào khoảng 200ml nước, đổ gói rau củ khô nằm trong gói mì vào. Thả mì vào luộc trong khoảng 3 phút rồi cho cho gói gia vị vào.
# Dùng nĩa từ từ làm tơi phần mì này ra, cho 3 con tôm, cẩn thận đập 1 quả trứng gà và thêm 1 muỗng cà phê dầu ớt. Đậy nắp lai và nấu thêm 2 phút nữa thì tắt bếp.
# Gắp mì tôm và topping cho vào chén rồi rưới nước mì vào. Cẩn thận cho đặt trứng lên trên cùng, trộn đều và thưởng thức nhé!"""

# all_text = text_preprocess(all_text)
# all_text = remove_stopwords(all_text)


# model = pickle.load(open(os.path.join(MODEL_PATH,"naive_bayes.pkl"), 'rb'))
model1 = pickle.load(open(os.path.join(MODEL_PATH,"svm.pkl"), 'rb'))
model2 = pickle.load(open(os.path.join(MODEL_PATH,"naive_bayes.pkl"), 'rb'))
model3 = pickle.load(open(os.path.join(MODEL_PATH,"linear_classifier.pkl"), 'rb'))

# for model in [ model2, model3]:
#     probabilities = model.predict_proba([all_text])[0]

#     # Sắp xếp các xác suất theo thứ tự giảm dần và lấy hai lớp có xác suất cao nhất
#     top_labels_indices = probabilities.argsort()[-2:][::-1]
#     top_labels = model.classes_[top_labels_indices]

#     top_probabilities = probabilities[top_labels_indices]

#     # In ra nhãn và xác suất
#     for label, prob in zip(top_labels, top_probabilities):
#         print(f"Nhãn: {label}, Xác suất: {prob:.4f}")

# label = model1.predict([all_text])
# print('Predict label:', label_encoder.inverse_transform(label))

# label = model2.predict([all_text])
# print('Predict label:', label_encoder.inverse_transform(label))

# label = model3.predict([all_text])
# print('Predict label:', label_encoder.inverse_transform(label))

def temp (text):
    text = text_preprocess(text)
    text = remove_stopwords(text)

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

