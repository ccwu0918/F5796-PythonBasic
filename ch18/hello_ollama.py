# 參閱18-19頁

import requests as req

OLLAMA_URL = "http://localhost:11434/api/generate" # 請求的資源網址

payload = {  # 定義請求的本體
  "model": "gemma3:1b",            # 模型名稱  
  "prompt": "星際大戰黑武士是反派嗎？", # 提示詞
  "stream": False     # 是否串流：否               
}

print("連接Ollama…")
resp = req.post(OLLAMA_URL, json=payload)  # 發出 POST 請求
print(resp.json()["response"])             # 顯示 JSON 格式回應中的 "response" 內容