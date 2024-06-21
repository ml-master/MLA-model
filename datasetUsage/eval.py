import numpy as np

# 给定的标签
labels = ["real", "fake", "NOT ENOUGH INFO"]

# 读取 claim_data.out 文件中的数据
with open('claim_data.out', 'r') as f:
    data = f.readlines()

# 将数据转换为numpy数组
probabilities = np.array([[float(num) for num in line.split()] for line in data])

# 找到每一行中概率最大的索引
max_indices = np.argmax(probabilities, axis=1)

# 根据索引获取对应的标签
predicted_labels = [labels[idx] for idx in max_indices]

# 读取 labels.txt 文件中的真实标签
with open('labels.txt', 'r') as f:
    true_labels = [line.strip() for line in f]

# 计算正确率
correct_count = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == pred)
accuracy = correct_count / len(true_labels)

print(f"Accuracy: {accuracy * 100:.2f}%")
