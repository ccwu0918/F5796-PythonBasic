import csv
import face_recognition
import pickle

pict_path = 'D:\\pict\\'                # 請自行修改路徑
csv_file = 'D:\\dataset\\staff.csv'     # 請自行修改路徑
pickle_file = 'D:\\dataset\\staff.dat'  # 請自行修改路徑

staff = {
    'name': [],
    'pict': [],
    'RFID': [],
    'encode': []
}

# 從CVS檔讀取個人資料
with open(csv_file, encoding='utf-8') as f:
    csv_data = csv.reader(f, delimiter=',')
    for row in csv_data:
        _key = row[0]
        _data = row[1:]

        if _key == 'RFID':
            staff[_key] = [int(i, base=16) for i in _data]
        else:
            staff[_key] = _data

for pic in staff['pict']:
    img = face_recognition.load_image_file(pict_path+pic)
    encoding = face_recognition.face_encodings(img)[0]
    print(encoding)
    staff['encode'].append(encoding)

with open(pickle_file, 'wb') as f:
    pickle.dump(staff, f)
