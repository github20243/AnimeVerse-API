import os

# Создаем директории
dirs = ['static', 'static/css', 'static/js']
for dir in dirs:
    os.makedirs(dir, exist_ok=True)
