from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from faker import Faker

engine = create_engine('mysql://root:@localhost/flask')

faker = Faker()

with Session(bind=engine) as sessao:
    SQL = "INSERT INTO users (nome) VALUES (:nome)"

    for x in range(100):
        nome = faker.name()
        sessao.execute(text(SQL), {'nome':nome})

    sessao.rollback()
    sessao.commit()