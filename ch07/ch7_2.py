# 參閱7-19頁

import subprocess

result = subprocess.run(["ping", "google.com"])
print("ping指令執行完畢，回傳碼：", result.returncode)