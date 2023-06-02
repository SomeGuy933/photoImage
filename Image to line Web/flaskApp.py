from flask import Flask, render_template, request
from PIL import Image
import main

app = Flask(__name__)
app.static_folder = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']
        if file.filename == '':
            return 'No file selected'

        file.save("uploads/img.jpeg")

        thiCCness = int(request.form.get('thickness'))
        threshold1 = int(request.form.get('threshold1'))
        threshold2 = int(request.form.get('threshold2'))
        drawColor = 'color' in request.form
        gif = 'gif' in request.form

        if not (1 <= thiCCness <= 5):
            return 'Invalid thiCCness value'

        if not (1 <= threshold1 <= 255):
            return 'Invalid line threshold one value'

        if not (1 <= threshold2 <= 255):
            return 'Invalid line threshold two value'
        rez = 25
        if drawColor:
            rez = int(request.form.get('rez'))
            if not (1 <= rez <= 100):
                return 'Invalid distance of average color value'
        fps = 5
        if gif:
            fps = int(request.form.get('fps'))
            if not (5 <= fps <= 100):
                return 'Invalid updates per frame value'
        main.doIt("uploads/img.jpeg", thiCCness=thiCCness, gif=gif, rez=rez, drawColor=drawColor, fps=fps,save="uploads/img.jpeg", threshold1=threshold1, threshold2=threshold2)

        return render_template('result.html')

    return render_template('upload.html')


@app.route('/uploads/img.jpeg')
def get_uploaded_image():
    return app.send_static_file('img.jpeg')


@app.route('/get_image_dimensions')
def get_image_dimensions():
    image_path = app.static_folder + '/img.jpeg'
    with Image.open(image_path) as img:
        width, height = img.size
    return {'width': width, 'height': height}


if __name__ == '__main__':
    app.run(debug=True)
