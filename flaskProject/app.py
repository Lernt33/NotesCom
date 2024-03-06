from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Ваше начальное содержимое страницы
initial_content = {
    'title': 'Динамическая подгрузка контента с Flask и AJAX',
    'content': 'Нажмите кнопку, чтобы загрузить дополнительный контент.'
}

@app.route('/')
def index():
    return render_template('index.html', content=initial_content)

@app.route('/load_content')
def load_content():
    # Здесь может быть ваша логика для загрузки дополнительного контента
    additional_content = {
        'title': 'Дополнительный контент',
        'content': 'Это дополнительный контент, загруженный динамически.'
    }
    return jsonify(additional_content)

if __name__ == '__main__':
    app.run(debug=True)