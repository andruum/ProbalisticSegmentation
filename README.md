# ProbalisticSegmentation

Требования:

python3

cv2 (pip3 install opencv-python)

numpy(pip3 install numpy)

Запуск:

python3 main.py path-to-image max-num-regions

где:

path-to-image - путь к изображению

max-num-regions - максимальное количество регионов, на которые нужно разделить картинку. Параметр по умолчанию - 10 . Если результаты сегментации не удовлетворяют (некоторые регионы слились в один) стоит попробовать увеличить этот параметр. Или уменьшить.

Результаты появятся в ./results
