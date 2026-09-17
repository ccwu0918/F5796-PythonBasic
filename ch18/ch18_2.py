# 參閱18-20頁

import requests as req
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
payload = {
    "model": "gemma3:1b",
    "prompt": "星際大戰黑武士是反派嗎？",
    "stream": True  # 串流模式
}

resp = req.post(OLLAMA_URL, json=payload, stream=True) # 接收串流

if resp.status_code == 200:
    print ("AI回應：")
    for line in resp.iter_lines(): # 逐行讀取回應
        if line: # 若有內容（亦即，非''空字串）
            utf8_line = line.decode("utf-8") # 解析 bytes
            result = json.loads(utf8_line)   # 把 JSON 轉成字典
            msg = result.get("response", "") # 取得 "response" 鍵值
            print(msg, end="", flush=True)   # 清除緩衝、立即輸出
else:
    # 顯示 HTTP 狀態碼和原因
    print("出錯了：", resp.status_code, resp.text)