from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.orm import relationship

class Minerio(Base):
	__tablename__ = 'Minerio'

	minerio = Column(String(128), primary_key = True)

class Chapa(Base):
	__tablename__ = 'Chapa'

	id = Column(Integer, primary_key = True)
	minerio = Column(String(128), ForeignKey('Minerio.minerio'))
	lamina = Column(String(32))
	codigo = Column(String(32))
	textura = Column(String(32))
	#Responsavel
	aumento = Column(Integer)
	cor = Column(String(32))
	tamanho = Column(String(32))
	posicao_x = Column(Float)
	posicao_y = Column(Float)
	relevo = Column(String(128))
	formato_cristal = Column(String(128))
	clivagem = Column(Boolean)
	fratura = Column(Boolean)
	minerios_contato = Column(String(128))
	extincao = Column(String(64))
	comentario = Column(String(512))

class Foto(Base):
	__tablename__ = 'Foto'

	id = Column(Integer, primary_key = True)
	chapa = Column(Integer, ForeignKey('Chapa.id'))
	imagem = image_attachment('Imagem')
	angulo = Column(Float)
	luz = Column(Boolean)

class Imagem(Base, Image):
	__tablename__ = 'Imagem'

	foto_id = Column(Integer, ForeignKey('Foto.id'))
	foto = relationship('Foto')