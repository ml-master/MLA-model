# 合并 out 文件
prob_files = ['origin_sentence_part_1.out', 'origin_sentence_part_2.out', 'origin_sentence_part_3.out']
with open('sentence_select_result.out', 'w', encoding='utf-8') as outfile:
    for prob_file in prob_files:
        with open(prob_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                outfile.write(line)
