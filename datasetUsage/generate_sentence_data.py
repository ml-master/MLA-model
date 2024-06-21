import os
import sqlite3
import drqa.tokenizers
from drqa.tokenizers import CoreNLPTokenizer
from drqa.retriever import TfidfDocRanker
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# 确保 nltk punkt 数据已下载
nltk.download('punkt')

# 设置环境变量
os.environ['CLASSPATH'] = '/mnt/DrQA/data/corenlp/*'
drqa.tokenizers.set_default('corenlp_classpath', '/mnt/DrQA/data/corenlp/*')

# 初始化分词器
tok = CoreNLPTokenizer()
print(tok.tokenize('hello world').words())  # Should complete immediately

# 打印以确认运行到此处
print("Initialization complete\n")

# 初始化检索器
ranker = TfidfDocRanker(
    tfidf_path='/mnt/DrQA/data/wikipedia/docs-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
    strict=False
)

# 读取texts.txt的所有行作为queries
with open("texts.txt", "r", encoding="utf-8") as file:
    queries = [line.strip() for line in file.readlines()]

# 连接到SQLite数据库
db_path = '/mnt/DrQA/data/wikipedia/docs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 准备写入TSV文件
with open("origin_sentence.tsv", "w", encoding="utf-8") as file:
    total_queries = len(queries)
    for i, text_a in enumerate(queries, start=1):
        # 使用检索器查找相关文档
        doc_names, doc_scores = ranker.closest_docs(text_a, k=1)

        # 打印相关文档名称和评分
        print("Top document:")
        for name, score in zip(doc_names, doc_scores):
            print(f"{name}: {score}")

        # 处理第一个文档
        if doc_names:
            cursor.execute("SELECT text FROM documents WHERE id=?", (doc_names[0],))
            row = cursor.fetchone()
            if row:
                document = row[0]
                # 使用nltk对文档进行分句
                sentences = sent_tokenize(document)
                # print("\nSentences with more than 20 words:")
                long_sentences = [sentence for sentence in sentences if len(word_tokenize(sentence)) > 20]
                
                if not long_sentences:
                    print(f"No long sentences found in document: {doc_names[0]}")
                    exit(1)

                index = len(long_sentences)
                label = 0
                title = doc_names[0]  # 使用文档名称作为title
                for sentence in long_sentences:
                    words = word_tokenize(sentence)
                    # if len(words) > 20:
                    #print(" ".join(words))
                    sentence_cleaned = sentence.replace('\n', ' ').replace('\t', ' ').strip()
                    # 生成TSV行
                    tsv_line = f"{index}\t{text_a}\t{title}\t{label}\t{sentence_cleaned}"
                    file.write(tsv_line + "\n")
                    # index += 1
            else:
                print(f"Document not found in database: {doc_names[0]}")
                exit(1)
        else:
            print(f"No documents found for query: {text_a}")
            exit(1)

        # 打印进度
        print(f"Processed {i}/{total_queries} queries")

# 关闭数据库连接
conn.close()

print("TSV file created successfully.")
