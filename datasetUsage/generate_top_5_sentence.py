import csv
import sys

# 文件名列表
tsv_files = ['origin_sentence_part_1.tsv', 'origin_sentence_part_2.tsv', 'origin_sentence_part_3.tsv']
prob_files = ['origin_sentence_part_1.out', 'origin_sentence_part_2.out', 'origin_sentence_part_3.out']

# 临时存储未完成组的数据
temp_group = []

# 初始化claim_data结果列表
claim_data_results = []

# 初始化 result_sentences 列表
result_sentences = []

# 计数器，用于记录已处理的文件部分数量
processed_parts = 0

# 逐个读取和处理每个部分的文件
for tsv_file, prob_file in zip(tsv_files, prob_files):
    # 读取当前部分的 TSV 文件
    sentences = []
    with open(tsv_file, 'r', encoding='utf-8') as tsv_f:
        for line in tsv_f:
            fields = line.strip().split('\t')
            if len(fields) == 5:
                sentences.append(fields)
            else:
                print(f"Skipping malformed line in {tsv_file}: {fields}")
                print("\n\n!!!!!!!!!!!!!!!!!\n\n")
                exit(-1)

    # 读取当前部分的概率文件
    probs = []
    with open(prob_file, 'r', encoding='utf-8') as prob_f:
        for line in prob_f:
            try:
                probs.append(float(line.strip()))
            except ValueError:
                print(f"Skipping malformed line in {prob_file}: {line}")

    # 将概率添加到句子数据
    for sentence, prob in zip(sentences, probs):
        sentence.append(prob)

    # 合并临时存储的未完成组
    df_sentences = temp_group + sentences

    i = 0
    while i < len(df_sentences):
        # 获取当前行的 index 值
        group_size = int(df_sentences[i][0])

        # 检查 index 是否大于 0
        if group_size <= 0:
            print(f"Error: The index value {group_size} is not greater than 0. Exiting.")
            sys.exit(1)

        # 检查当前组是否完整
        if i + group_size <= len(df_sentences):
            # 当前组完整，处理这个组
            group_df = df_sentences[i:i + group_size]

            # 按概率值降序排序，取前5个句子
            group_df.sort(key=lambda x: x[5], reverse=True)
            top_sentences = group_df[:5]

            # 添加claim句子和对应的5个句子到claim_data_results
            claim_sentence = top_sentences[0][1]
            claim_data_results.append([0, claim_sentence, '[PAD]', -1, '[PAD]'])
            for row in top_sentences:
                claim_data_results.append([0, claim_sentence, 'None', row[3], row[4]])

            # 如果句子少于5个，用填充值补齐
            num_to_pad = 5 - len(top_sentences)
            if num_to_pad > 0:
                for _ in range(num_to_pad):
                    claim_data_results.append([0, claim_sentence, '[PAD]', -1, '[PAD]'])

            # 将结果追加到 result_sentences
            result_sentences.extend(top_sentences)

            # 写入 claim_data_results 到文件并清空列表
            with open('claim_data.tsv', 'a', encoding='utf-8', newline='') as output_file:
                writer = csv.writer(output_file, delimiter='\t')
                writer.writerows(claim_data_results)
            claim_data_results = []

            # 更新索引以处理下一个组
            i += group_size
        else:
            # 当前组不完整，将其存储到临时存储区
            temp_group = df_sentences[i:]
            break
    else:
        # 如果循环正常结束，清空临时存储区
        temp_group = []


print("Top 5 sentences and claim_data files created successfully.")
