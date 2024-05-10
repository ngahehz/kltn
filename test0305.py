from underthesea import word_tokenize

document = "ờ t muốn check coi thí dù hòa đồng và hoà đồng có giống nhau không, hợp tác, hòa đồng"
document = word_tokenize(document, format="text")
print(document)