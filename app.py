from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Note('{self.title}', '{self.created}')"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_title = request.form['title']
        note_content = request.form['content']

        if note_title.strip() and note_content.strip():
            new_note = Note(title=note_title, content=note_content)
            db.session.add(new_note)
            db.session.commit()

        return redirect(url_for('index'))

    notes = Note.query.order_by(Note.created.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)