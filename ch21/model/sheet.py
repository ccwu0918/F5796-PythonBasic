# 類別功能：
# 指定工作表名稱和標題
# 新增工作表內容
import gspread

class GoogleSheet():
    '''
    建構式參數：
    file_name：試算表檔名
    ws_title：工作表名稱，預設None。
    '''

    def __init__(self, file_name, wks_title=None):
        try: # 嘗試讀取憑證檔
            client = gspread.service_account()
        except Exception as e:
            print('無法開啟憑證檔', e)
            exit()  # 關閉程式

        try: # 嘗試開啟Google試算表
            sh = client.open(file_name)
        except Exception as e:
            print('無法開啟Google試算表', e)
            exit()

        if wks_title is None:
            # 開啟「工作表1」
            self._wks = sh.sheet1
        else:
            try: # 嘗試開啟指定工作表
                self._wks = sh.worksheet(wks_title)
            except Exception as e:
                print('無法開啟工作表', e)
                exit()

    def append_row(self, data):
        self._wks.append_row(data)  # 插入新列

    def resize(self, n=1):
        self._wks.resize(n)

    def update_header(self, data, delete=True):
        if delete:
            self._wks.delete_row(1)
        
        self._wks.insert_row(data, 1)

    @property
    def headers(self):
        return self._wks.row_values(1)
    