import json

# 文件名
input_filename = 'gossipcop_v3-1_style_based_fake.json'
output_texts_filename = 'texts.txt'
output_labels_filename = 'labels.txt'

# 读取JSON文件
with open(input_filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

texts = []
labels = []

# 提取文本和标签
for key, value in data.items():
    origin_text = value['origin_text'].replace('\n', ' ').replace('\t', ' ')
    generated_text = value['generated_text'].replace('\n', ' ').replace('\t', ' ')
    label1 = value['origin_label']
    label2 = value['generated_label']
    texts.append(origin_text)
    texts.append(generated_text)
    labels.append(label1)
    labels.append(label2)

# 将文本写入文件
with open(output_texts_filename, 'w', encoding='utf-8') as text_file:
    for text in texts:
        text_file.write(text + '\n')

# 将标签写入文件
with open(output_labels_filename, 'w', encoding='utf-8') as label_file:
    for label in labels:
        label_file.write(label + '\n')

print(f'Texts have been written to {output_texts_filename}')
print(f'Labels have been written to {output_labels_filename}')
