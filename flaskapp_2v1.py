from flask import Flask, request, render_template
import os
from pathlib import Path
import shutil

def organize_files(map):
    if not os.path.exists(map):
        return f"De opgegeven map '{map}' bestaat niet."

    os.chdir(map)

    Path("images").mkdir(exist_ok=True)
    Path("else").mkdir(exist_ok=True)

    files = sorted(os.listdir())

    counterImages = 1
    counterElse = 1

    for file in files:
        if file in ["images", "else"]:
            continue
        name, ext = os.path.splitext(file)

        if ext.lower() in [".jpg", ".jpeg"]:
            newName = f"Picture {counterImages}{ext}"
            counterDoubleName = 1  # Reset de teller voor dubbele namen

            while os.path.exists(newName):
                newName = f"Picture {counterImages}_{counterDoubleName}{ext}"
                counterDoubleName += 1

            os.rename(file, newName)
            shutil.move(newName, "images")
            counterImages += 1
        else:
            newNameElse = f"Document {counterElse}{ext}"
            counterDoubleName = 1  # Reset de teller voor dubbele namen

            while os.path.exists(newNameElse):
                newNameElse = f"Document {counterElse}_{counterDoubleName}{ext}"
                counterDoubleName += 1

            os.rename(file, newNameElse)
            shutil.move(newNameElse, "else")
            counterElse += 1

    return "De bestanden zijn geordend!"


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def my_form():
    map_check = None
    result = None
    if request.method == 'POST':
        cwd_map = request.form['map_input']
        result = organize_files(cwd_map)
        map_check = cwd_map.lower()

    return render_template('flask_web.html', map_check=map_check, result=result)


if __name__ == '__main__':
    app.run(debug=True)
