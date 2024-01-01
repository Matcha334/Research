def process_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 偶数行を削除 (リストのインデックスは0から始まるため、奇数インデックスが偶数行に対応)
    lines = [line for i, line in enumerate(lines) if i % 2 == 0]

    # 先頭から1600行を残す
    lines = lines[:1600]

    with open(output_file, 'w') as file:
        file.writelines(lines)

# スクリプトを使う例
input_file = 'mubase.txt'  # 入力ファイルのパス
output_file = 'mubase.txt'  # 出力ファイルのパス
process_file(input_file, output_file)
