import pandas as pd
import os

# Đọc excel
card_info_path = r'.\card_info.xlsx'
card_info = pd.read_excel(card_info_path, engine='openpyxl')

# Check folder tồn tại không
# Nếu không tồn tại thì thực hiện tạo mới
if not os.path.exists(".\data"):
    os.mkdir(".\data")

#Lưu trữ tên ngân hàng
bank_names:list = card_info['Bank name'].unique().tolist()
with open(r'.\data\bank_name.txt', 'w', encoding='utf-8') as f:
    for i,bank_name in enumerate(bank_names):
        #id, bank name
        f.write(f'{i}, {bank_name}')
        f.write("\n")

# Lưu trữ loại thẻ
card_types:list = card_info['Card type'].unique().tolist()
with open(r'.\data\card_type.txt', 'w', encoding='utf-8') as f:
    for i,card_type in enumerate(card_types):
        # id, card type
        f.write(f'{i}, {card_type}')
        f.write("\n")

#Lưu trữ data về thẻ
card_info['Bank name'] = card_info['Bank name'].apply(lambda x: bank_names.index(x))
card_info['Card type'] = card_info['Card type'].apply(lambda x: card_types.index(x))
with open(r'.\data\card_info.txt', 'w', encoding='utf-8') as f:
    for i, row in card_info.iterrows():
        #id, Bank name, Card type, Card name, Lower limit, Upper limit, Income, img_url
        f.write(f'{i},{row["Bank name"]},{row["Card type"]},{row["Card name"]},{row["Lower limit"]},{row["Upper limit"]},{row["Income"]},{row["img_url"]}')
        f.write("\n")

