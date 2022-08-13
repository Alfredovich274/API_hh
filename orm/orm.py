from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Структура данных:
Основная таблица
    id
    author - id author
    name - уникальное значение
    year - id year
    rating - id rating
    description - уникальное значение, text
    text - уникальное значение, text
    link - уникальное значение
    link doc - уникальное значение
    link fb2 - уникальное значение
    link pdf - уникальное значение
Таблица author
    id
    name - уникальное значение
Таблица year
    id
    name - уникальное значение
Таблица rating
    id
    name - уникальное значение
"""
engine = create_engine('sqlite:///db_orm.sqlite', echo=True)
Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.name} {self.id}'


class Year(Base):
    __tablename__ = 'year'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.name} {self.id}'


class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.name} {self.id}'


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('author.id'))
    name = Column(String, unique=True)
    year = Column(Integer, ForeignKey('year.id'))
    rating = Column(Integer, ForeignKey('rating.id'))
    description = Column(Text, unique=True)
    text = Column(Text, unique=True)
    link = Column(Text, unique=True)
    link_doc = Column(Text, unique=True)
    link_fb2 = Column(Text, unique=True)
    link_pdf = Column(Text, unique=True)

    def __init__(self, name, author, year, rating, description, text, link):
        super().__init__()
        self.name = name
        self.author = author
        self.year = year
        self.rating = rating
        self.description = description
        self.text = text
        self.link = link

    def __str__(self):
        return f'{self.id} - {self.author} {self.name} {self.year}' \
               f' {self.rating} {self.link}'


def add_foreign(data, name):
    print(data, name)
    Session = sessionmaker(bind=engine)
    session = Session()
    if name == 'year':
        try:
            year_id = session.query(Year).filter(Year.name == data).first().id
        except AttributeError:
            new_entry = Year(data)
            session.add(new_entry)
            session.commit()
            year_id = session.query(Year).filter(Year.name == data).first().id
        return year_id
    if name == 'rating':
        try:
            rating_id = session.query(Rating).filter(Rating.name == data).first().id
        except AttributeError:
            new_entry = Rating(data)
            session.add(new_entry)
            session.commit()
            rating_id = session.query(Rating).filter(Rating.name == data).first().id
        return rating_id
    if name == 'author':  # Можно было сделать через one_or_none()
        try:
            author_id = session.query(Author).filter(Author.name == data).first().id
        except AttributeError:
            new_entry = Author(data)
            session.add(new_entry)
            session.commit()
            author_id = session.query(Author).filter(Author.name == data).first().id
        return author_id


def add_line(data):
    """
    Переносим строку данных в базу данных, если нужно по связанным таблицам.
    :param data: Строка dict, где перечислены ключ значения одной строки данных.
    :return: В идеале возвращаем True если все прошло удачно и False если
    наоборот, но нет времени делать проверку данных, по этому пока ни чего
    не возвращаем
    """
    # Заполняем таблицы
    Session = sessionmaker(bind=engine)
    session = Session()
    author = add_foreign(data['author'], 'author') if data.get('author') else 0
    year = add_foreign(data['year'], 'year') if data.get('year') else 0
    rating = add_foreign(data['rating'], 'rating') if data.get('rating') else 0
    name = data['title'] if data.get('title') else 0
    description = data['description'] if data.get('description') else 0
    text = data['citation'] if data.get('citation') else 0
    link = data['link'] if data.get('link') else 0

    session.add(Book(name=name, author=author, year=year, rating=rating,
                     description=description, text=text, link=link))
    session.commit()


def get_base():
    Session = sessionmaker(bind=engine)
    session = Session()
    book = session.query(Book)
    author = session.query(Author)
    year = session.query(Year)
    rating = session.query(Rating)
    return book, year, author, rating
    # return session.query(Author.name, Book.name, Year.name, Rating.name,
    #                      Book.text, Book.link).filter(Book.author == Author.id
    #                                                   and Book.year == Year.id
    #                                                   and Book.rating == Rating.id)


if __name__ in '__main__':
    # Создаем таблицы
    Base.metadata.create_all(engine)

