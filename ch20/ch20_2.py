# 參閱20-7頁

from langchain_ollama import OllamaEmbeddings
import numpy as np

model=OllamaEmbeddings(model="nomic-embed-text")

def cos_similarity(a, b):  # 計算餘弦相似度
    ans = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return ans

data = [  # 資料字串
  "我替她感到欣慰",
  "水槽的碗裡有一隻魚",
  "A red pen on the desk."
 ]

embed_data = model.embed_documents(data) # 把字串列表轉成詞向量
txt = "我很快樂"  # 要跟資料字串比較的文字
embed_txt = model.embed_query(txt)       # 把字串轉換成詞向量

print(f"跟「{txt}」比較：")
for i, em in enumerate(embed_data):
    # 計算餘弦相似度
    print(f"{data[i]}：相似度{ cos_similarity(embed_txt, em)}")