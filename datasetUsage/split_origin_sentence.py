import os

def split_large_file(file_path, num_parts):
    file_handles = []
    for i in range(num_parts):
        file_name = f'origin_sentence_part_{i+1}.tsv'
        file_handles.append(open(file_name, 'w', encoding='utf-8'))

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline()
            for handle in file_handles:
                handle.write(header)

            line_count = sum(1 for line in file)
            file.seek(0)
            file.readline()  # Skip the header
            part_size = line_count // num_parts

            current_part = 0
            for i, line in enumerate(file):
                if i > 0 and i % part_size == 0 and current_part < num_parts - 1:
                    current_part += 1
                file_handles[current_part].write(line)

    finally:
        for handle in file_handles:
            handle.close()

if __name__ == "__main__":
    file_path = 'origin_sentence.tsv'
    num_parts = 3

    if os.path.exists(file_path):
        split_large_file(file_path, num_parts)
        print(f"File split into {num_parts} parts successfully.")
    else:
        print(f"File {file_path} does not exist.")
