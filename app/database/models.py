# app/database/models.py - SQLAlchemy Database Models

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import JSON
from decimal import Decimal

db = SQLAlchemy()

class Organization(db.Model):
    """Organization/Company model"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    organization_type = db.Column(db.String(50), nullable=False)  # 'corporate', 'individual', 'franchise'
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    territory = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resellers = db.relationship('Reseller', backref='organization', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization_type': self.organization_type,
            'address': self.address,
            'city': self.city,
            'province': self.province,
            'phone': self.phone,
            'email': self.email,
            'territory': self.territory
        }

class Reseller(db.Model):
    """Reseller (MLM participant) model"""
    __tablename__ = 'resellers'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # 'BP', 'IBO', 'BD'
    position = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    
    # MLM-specific fields
    sponsor_id = db.Column(db.Integer, db.ForeignKey('resellers.id'), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    promotion_date = db.Column(db.Date, nullable=True)
    active_status = db.Column(db.Boolean, default=True)
    territory = db.Column(db.String(100))
    
    # Avatar/initials for display
    avatar_initials = db.Column(db.String(5))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sponsor = db.relationship('Reseller', remote_side=[id], backref='downlines')
    monthly_sales = db.relationship('MonthlySales', backref='reseller', lazy=True, cascade='all, delete-orphan')
    commissions_earned = db.relationship('CommissionCalculation', 
                                       foreign_keys='CommissionCalculation.reseller_id',
                                       backref='earner', lazy=True)
    commissions_from = db.relationship('CommissionCalculation',
                                     foreign_keys='CommissionCalculation.source_reseller_id',
                                     backref='source', lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def direct_downlines(self):
        """Get direct downlines (children)"""
        return Reseller.query.filter_by(sponsor_id=self.id).all()
    
    def get_monthly_sales(self, month):
        """Get sales for a specific month"""
        sales_record = MonthlySales.query.filter_by(
            reseller_id=self.id,
            month=month
        ).first()
        return sales_record.gppis if sales_record else 0
    
    def to_dict(self, include_downlines=False):
        result = {
            'id': self.id,
            'employee_code': self.employee_code,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'level': self.level,
            'position': self.position,
            'email': self.email,
            'phone': self.phone,
            'sponsor_id': self.sponsor_id,
            'organization_id': self.organization_id,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'promotion_date': self.promotion_date.isoformat() if self.promotion_date else None,
            'active_status': self.active_status,
            'territory': self.territory,
            'avatar_initials': self.avatar_initials
        }
        
        if include_downlines:
            result['children'] = [d.to_dict() for d in self.direct_downlines]
        else:
            result['children'] = [d.id for d in self.direct_downlines]
        
        return result

class MonthlySales(db.Model):
    """Monthly sales records for each reseller"""
    __tablename__ = 'monthly_sales'
    
    id = db.Column(db.Integer, primary_key=True)
    reseller_id = db.Column(db.Integer, db.ForeignKey('resellers.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: 'YYYY-MM'
    gppis = db.Column(db.Numeric(12, 2), default=0)  # Gross Personal Paid-In Sales
    
    # Product breakdown (optional for detailed analysis)
    premium_sales = db.Column(db.Numeric(12, 2), default=0)
    standard_sales = db.Column(db.Numeric(12, 2), default=0)
    basic_sales = db.Column(db.Numeric(12, 2), default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('reseller_id', 'month', name='_reseller_month_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'reseller_id': self.reseller_id,
            'month': self.month,
            'gppis': float(self.gppis),
            'premium_sales': float(self.premium_sales),
            'standard_sales': float(self.standard_sales),
            'basic_sales': float(self.basic_sales)
        }

class CommissionRule(db.Model):
    """Commission rules configuration"""
    __tablename__ = 'commission_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # 'outright', 'group_override', etc.
    level = db.Column(db.String(10))  # 'BP', 'IBO', 'BD', or NULL for all
    product_category = db.Column(db.String(50))  # 'SUNX-PREMIUM', etc.
    
    # Rule parameters (stored as JSON for flexibility)
    parameters = db.Column(JSON)
    
    active = db.Column(db.Boolean, default=True)
    effective_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rule_type': self.rule_type,
            'level': self.level,
            'product_category': self.product_category,
            'parameters': self.parameters,
            'active': self.active,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None
        }

class CommissionCalculation(db.Model):
    """Commission calculation records"""
    __tablename__ = 'commission_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    reseller_id = db.Column(db.Integer, db.ForeignKey('resellers.id'), nullable=False)
    source_reseller_id = db.Column(db.Integer, db.ForeignKey('resellers.id'), nullable=True)
    
    commission_type = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: 'YYYY-MM'
    
    # Commission details
    base_amount = db.Column(db.Numeric(12, 2), nullable=False)
    commission_rate = db.Column(db.Numeric(5, 4), nullable=False)  # Percentage as decimal
    commission_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    # Additional context
    tier_name = db.Column(db.String(50))  # 'Silver', 'Gold', 'Diamond', etc.
    notes = db.Column(db.Text)
    
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'reseller_id': self.reseller_id,
            'source_reseller_id': self.source_reseller_id,
            'commission_type': self.commission_type,
            'month': self.month,
            'base_amount': float(self.base_amount),
            'commission_rate': float(self.commission_rate),
            'commission_amount': float(self.commission_amount),
            'tier_name': self.tier_name,
            'notes': self.notes,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None
        }

class MonthlySummary(db.Model):
    """Monthly performance summary for each reseller"""
    __tablename__ = 'monthly_summaries'
    
    id = db.Column(db.Integer, primary_key=True)
    reseller_id = db.Column(db.Integer, db.ForeignKey('resellers.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Format: 'YYYY-MM'
    
    # Sales metrics
    gppis = db.Column(db.Numeric(12, 2), default=0)
    ggpis = db.Column(db.Numeric(12, 2), default=0)  # Calculated group sales
    
    # Commission totals
    total_commissions = db.Column(db.Numeric(12, 2), default=0)
    outright_commissions = db.Column(db.Numeric(12, 2), default=0)
    override_commissions = db.Column(db.Numeric(12, 2), default=0)
    incentive_commissions = db.Column(db.Numeric(12, 2), default=0)
    
    # Status and qualifications
    active_status = db.Column(db.Boolean, default=False)
    group_override_tier = db.Column(db.String(50))
    active_downlines_count = db.Column(db.Integer, default=0)
    promotion_eligible = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('reseller_id', 'month', name='_summary_reseller_month_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'reseller_id': self.reseller_id,
            'month': self.month,
            'gppis': float(self.gppis),
            'ggpis': float(self.ggpis),
            'total_commissions': float(self.total_commissions),
            'outright_commissions': float(self.outright_commissions),
            'override_commissions': float(self.override_commissions),
            'incentive_commissions': float(self.incentive_commissions),
            'active_status': self.active_status,
            'group_override_tier': self.group_override_tier,
            'active_downlines_count': self.active_downlines_count,
            'promotion_eligible': self.promotion_eligible
        }

def init_db():
    """Initialize the database with all tables"""
    db.create_all()
    print("✅ Database tables created successfully!")

def drop_db():
    """Drop all database tables (use with caution!)"""
    db.drop_all()
    print("🗑️ Database tables dropped!")

def reset_db():
    """Reset the database (drop and recreate all tables)"""
    drop_db()
    init_db()