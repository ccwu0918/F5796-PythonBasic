# 參閱6-26頁

from os import path
import platform

def pyTube_folder():
    sys = platform.system()
    home = path.expanduser('~')  # 使用者家目錄

    if sys == 'Darwin':  # macOS系統
        folder=path.join(home,'Movies','PyTube')
    else:  # 其他作業系統（Windows和Linux）
        folder=path.join(home,'Videos','PyTube')

    os.makedirs(folder, exist_ok=True)  # 新增資料夾

    return folder  # 傳回資料夾路徑