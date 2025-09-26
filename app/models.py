from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    hostname = Column(String, index=True, nullable=False)
    ip = Column(String, index=True)
    os_name = Column(String)
    os_version = Column(String)
    owner_team = Column(String)
    business_criticality = Column(Integer, default=1)  # 1..5
    tags = Column(JSON, default={})

    softwares = relationship("Software", back_populates="asset", cascade="all,delete")
    findings = relationship("Finding", back_populates="asset", cascade="all,delete")

class Software(Base):
    __tablename__ = "softwares"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    name = Column(String, index=True)
    version = Column(String)
    vendor = Column(String)
    cpe = Column(String, index=True)
    evidence = Column(JSON, default={})
    asset = relationship("Asset", back_populates="softwares")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    id = Column(String, primary_key=True)  # CVE-YYYY-NNNN
    title = Column(String)
    cvss_base = Column(Float, default=0.0)
    epss = Column(Float, default=0.0)             # 0..1
    known_exploited = Column(Boolean, default=False)
    refs = Column(JSON, default={})

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    cve_id = Column(String, ForeignKey("vulnerabilities.id"))
    detected_at = Column(DateTime, default=datetime.utcnow)
    evidence = Column(JSON, default={})
    severity = Column(String, default="medium")
    risk_score = Column(Float, default=0.0)
    status = Column(String, default="open")  # open/in-progress/accepted/false-positive/closed
    due_at = Column(DateTime, nullable=True)
    ticket_ref = Column(String, nullable=True)

    asset = relationship("Asset", back_populates="findings")
