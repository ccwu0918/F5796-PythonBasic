# 參閱7-19頁

import subprocess

result = subprocess.run( ["ping", "google.com"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True )

print("STDOUT（標準輸出）：")
print(result.stdout)
print("STDERR（標準錯誤）：")
print(result.stderr)