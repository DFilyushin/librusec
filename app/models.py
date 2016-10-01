from app import db

relationship_table = db.Table('link_ab',
                        db.Column('id_book', db.Integer, db.ForeignKey('books.id'), nullable=False),
                        db.Column('id_author', db.Integer, db.ForeignKey('authors.id'), nullable=False),
                        db.PrimaryKeyConstraint('id_book', 'id_author'))

class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    middle_name = db.Column(db.String)

    def __repr__(self):
        return "%s %s" % (self.last_name, self.first_name)


class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    size = db.Column(db.Integer, name='file_size')
    type = db.Column(db.String, name='file_type')
    lang = db.Column(db.String)
    genre = db.Column(db.Text)
    authors = db.relationship('Authors', secondary=relationship_table, backref=db.backref('books'))


class Genre(db.Model):
    __tablename__ = 'genre'
    id_genre = db.Column(db.String, primary_key=True)
    ru_genre = db.Column(db.String, nullable=False)
