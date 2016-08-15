
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import create_engine, Column, Integer, String
class Test(Base):
	__tablename__ = 'testando_sql_alchemy'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	password = Column(String)

	def __repr__(self):
		return "<test dummy obj>"



engine = create_engine('postgresql://hpborges:290600@localhost:5432/hpborges')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

ed_user = Test(name='ed', fullname='jojonis', password='pass')
session.add(ed_user)
session.commit()