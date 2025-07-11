from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, class_mapper

url_pg_krd = "postgresql://acsuser:SirvAmsnm@172.28.177.111/cash"
engine_krd = create_engine(url_pg_krd, echo=True)
session_krd = sessionmaker(engine_krd)

url_pg_rnd = "postgresql://acsuser:SirvAmsnm@172.172.181.174/century"
engine_rnd = create_engine(url_pg_rnd, echo=True)
session_rnd = sessionmaker(engine_rnd)

# url_pg_vlg = "postgresql://sync_goods_1c:S%3f4kM%3d@172.172.180.151/cash"
url_pg_vlg = "postgresql://acsuser:SirvAmsnm@172.172.181.174/century"
engine_vlg = create_engine(url_pg_vlg, echo=False)
session_vlg = sessionmaker(engine_vlg)


class Base(DeclarativeBase):
    __abstract__ = True

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}
