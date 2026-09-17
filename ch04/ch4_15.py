# 參閱4-21頁


def rect_area(w, h=None):
    if h is None:
        return w * w
    else:
        return w * h


area = rect_area(8, 3)
# area = rect_area(8)
print(area)
