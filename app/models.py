from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    hostname = Column(String, index=True, nullable=False)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    id = Column(String, primary_key=True)  # CVE-YYYY-NNNN
    title = Column(String)
    cvss_base = Column(Float, default=0)
    epss = Column(Float, default=0)        # likelihood (0..1)
    known_exploited = Column(Boolean, default=False)
    refs = Column(JSON, default={})

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
