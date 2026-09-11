from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Numeric,
    Date
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String(100), nullable=True)
    invoice_date = Column(Date, nullable=True)

    vendor = Column(String(255), nullable=True)
    customer = Column(String(255), nullable=True)

    po_number = Column(String(100), nullable=True)
    gstin = Column(String(20), nullable=True)
    currency = Column(String(10), nullable=True)

    subtotal = Column(Numeric(12, 2), nullable=True)
    tax = Column(Numeric(12, 2), nullable=True)
    total = Column(Numeric(12, 2), nullable=True)

    raw_text = Column(Text, nullable=True)

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    description = Column(String(500), nullable=True)
    hsn_code = Column(String(50), nullable=True)

    quantity = Column(Numeric(12, 2), nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=True)
    amount = Column(Numeric(12, 2), nullable=True)

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="queued"
    )

    error_message = Column(
        Text,
        nullable=True
    )
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice")

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default="user"
    )
