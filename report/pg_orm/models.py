from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from report.pg_orm.database import Base


class Agent(Base):
    __tablename__ = "agent"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False, index=True)
    program_id: Mapped[int]
    item_name: Mapped[str]
    level_id: Mapped[int]
    is_active: Mapped[bool]
    comment: Mapped[Optional[str]]
    date_create: Mapped[Optional[datetime]]
    date_update: Mapped[Optional[datetime]]
    group_id: Mapped[int]
    region_id: Mapped[int]
    contact_phone: Mapped[Optional[str]]
    contact_face: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    agent_dovoz_id: Mapped[int] = mapped_column(ForeignKey("agent.id"))
    agent_id: Mapped[int]
    ex_id: Mapped[Optional[str]]
    dovoz = relationship(
        "Agent",
        # "Node",
        uselist=False,
        remote_side=[id],
        backref=backref("next", uselist=False),
        lazy="joined",
        join_depth=2,
    )


class Invoice(Base):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    program_id: Mapped[int] = mapped_column()
    db_id: Mapped[int]
    acs_number: Mapped[int]
    is_active: Mapped[bool]
    date_doc: Mapped[Optional[datetime]]
    is_entry: Mapped[bool]
    invoice_type_id: Mapped[int]
    from_id: Mapped[int] = mapped_column(ForeignKey(Agent.id))
    to_id: Mapped[int] = mapped_column(ForeignKey(Agent.id))
    agent_id: Mapped[int] = mapped_column(ForeignKey(Agent.id))
    date_create: Mapped[Optional[datetime]]
    date_update: Mapped[Optional[datetime]]
    comment: Mapped[Optional[str]]
    user_create: Mapped[Optional[str]]
    user_update: Mapped[Optional[str]]
    delivery: Mapped[bool]
    uid: Mapped[int]
    original_uid: Mapped[int]
    order_number: Mapped[Optional[str]]

    invoices_body: Mapped[list["InvoiceBody"]] = relationship(
        "InvoiceBody",
        # back_populates="invoice_id_by",
        primaryjoin="and_(Invoice.id==InvoiceBody.invoice_id, "
        "InvoiceBody.program_id==Invoice.program_id)",
        lazy="joined",
    )
    agent: Mapped[Agent] = relationship(
        lazy="joined",
        uselist=False,
        foreign_keys=[agent_id],
    )
    from_ids: Mapped[Agent] = relationship(
        lazy="joined",
        foreign_keys=[from_id],
    )
    to_ids: Mapped[Agent] = relationship(
        lazy="joined",
        uselist=False,
        foreign_keys=[to_id],
    )


class Goods(Base):
    __tablename__ = "goods_all"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    marking_goods: Mapped[int] = mapped_column(index=True)
    item_name: Mapped[str]
    group_id: Mapped[int]
    is_active: Mapped[bool]
    shelf_life: Mapped[int]
    pieces_pkge: Mapped[int]
    amount_inblock: Mapped[int]
    amount_inbox: Mapped[int]
    amount_inpallet: Mapped[int]
    user_create: Mapped[Optional[str]]
    date_create: Mapped[Optional[datetime]]
    user_update: Mapped[Optional[str]]
    date_update: Mapped[Optional[datetime]]
    weight: Mapped[float]
    weight_netto: Mapped[float]
    length_box: Mapped[float]
    width_box: Mapped[float]
    height_box: Mapped[float]
    barcode_block: Mapped[Optional[str]]
    barcode_box: Mapped[Optional[str]]
    barcode_pkge: Mapped[Optional[str]]

    invoices_body: Mapped["InvoiceBody"] = relationship(
        back_populates="goods",
    )


class InvoiceBody(Base):
    __tablename__ = "invoice_body"
    line_id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[float]
    is_active: Mapped[bool]
    invoice_id: Mapped[int] = mapped_column(ForeignKey(Invoice.id), primary_key=True)
    goods_id: Mapped[int] = mapped_column(ForeignKey(Goods.id))

    goods: Mapped[Goods] = relationship(
        back_populates="invoices_body",
        lazy="joined",
        primaryjoin="and_(Goods.id==InvoiceBody.goods_id)",
    )
