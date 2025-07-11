# app/services/hierarchy_service.py - MLM Hierarchy Management Service

from database.models import (
    db, Reseller, Organization, MonthlySales, 
    CommissionCalculation, MonthlySummary
)
from services.commission_engine import CommissionEngine
from decimal import Decimal
from typing import Dict, List, Optional
import logging

class HierarchyService:
    """
    Service for managing MLM hierarchy structure and related operations
    """
    
    def __init__(self):
        self.commission_engine = CommissionEngine()
        self.logger = logging.getLogger(__name__)
    
    def get_complete_hierarchy(self) -> List[Dict]:
        """
        Get complete hierarchy starting from root resellers (no sponsors)
        Returns nested structure with all downlines
        """
        try:
            # Get root resellers (those without sponsors)
            root_resellers = Reseller.query.filter_by(sponsor_id=None).all()
            
            hierarchy = []
            for root in root_resellers:
                hierarchy.append(self._build_reseller_tree(root))
            
            return hierarchy
            
        except Exception as e:
            self.logger.error(f"Error building hierarchy: {str(e)}")
            raise
    
    def _build_reseller_tree(self, reseller: Reseller) -> Dict:
        """
        Recursively build reseller tree with all downlines
        """
        # Get basic reseller data
        reseller_data = reseller.to_dict()
        
        # Add organization info
        if reseller.organization:
            reseller_data['organization'] = reseller.organization.to_dict()
        
        # Get direct downlines
        downlines = Reseller.query.filter_by(sponsor_id=reseller.id).all()
        reseller_data['children'] = []
        
        for downline in downlines:
            reseller_data['children'].append(self._build_reseller_tree(downline))
        
        return reseller_data
    
    def get_reseller_details(self, reseller_id: int) -> Dict:
        """
        Get detailed information for a specific reseller including
        sales history, commission totals, and downline summary
        """
        reseller = Reseller.query.get(reseller_id)
        if not reseller:
            raise ValueError(f"Reseller {reseller_id} not found")
        
        try:
            # Basic reseller info
            details = reseller.to_dict()
            
            # Organization info
            if reseller.organization:
                details['organization'] = reseller.organization.to_dict()
            
            # Sales history (last 6 months)
            sales_history = self._get_sales_history(reseller_id, months=6)
            details['sales_history'] = sales_history
            
            # Commission history
            commission_history = self._get_commission_history(reseller_id, months=6)
            details['commission_history'] = commission_history
            
            # Downline summary
            downline_summary = self._get_downline_summary(reseller_id)
            details['downline_summary'] = downline_summary
            
            # Current month performance
            current_month = "2024-07"  # For demo purposes
            current_performance = self.commission_engine.calculate_monthly_commissions(
                reseller_id, current_month
            )
            details['current_performance'] = current_performance
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error getting reseller details for {reseller_id}: {str(e)}")
            raise
    
    def _get_sales_history(self, reseller_id: int, months: int = 6) -> List[Dict]:
        """Get sales history for the specified number of months"""
        sales_records = db.session.query(MonthlySales).filter(
            MonthlySales.reseller_id == reseller_id
        ).order_by(MonthlySales.month.desc()).limit(months).all()
        
        return [record.to_dict() for record in sales_records]
    
    def _get_commission_history(self, reseller_id: int, months: int = 6) -> List[Dict]:
        """Get commission history for the specified number of months"""
        # Get unique months from commission calculations
        commission_months = db.session.query(
            CommissionCalculation.month,
            db.func.sum(CommissionCalculation.commission_amount).label('total')
        ).filter(
            CommissionCalculation.reseller_id == reseller_id
        ).group_by(
            CommissionCalculation.month
        ).order_by(
            CommissionCalculation.month.desc()
        ).limit(months).all()
        
        history = []
        for month, total in commission_months:
            # Get detailed breakdown for this month
            month_commissions = CommissionCalculation.query.filter_by(
                reseller_id=reseller_id,
                month=month
            ).all()
            
            breakdown = {}
            for comm in month_commissions:
                if comm.commission_type not in breakdown:
                    breakdown[comm.commission_type] = 0
                breakdown[comm.commission_type] += float(comm.commission_amount)
            
            history.append({
                'month': month,
                'total_commission': float(total),
                'breakdown': breakdown
            })
        
        return history
    
    def _get_downline_summary(self, reseller_id: int) -> Dict:
        """Get summary of all downlines including counts by level"""
        # Count direct downlines by level
        direct_counts = db.session.query(
            Reseller.level,
            db.func.count(Reseller.id).label('count')
        ).filter(
            Reseller.sponsor_id == reseller_id
        ).group_by(Reseller.level).all()
        
        direct_summary = {level: count for level, count in direct_counts}
        
        # Count total downlines (recursive)
        total_downlines = self._count_total_downlines(reseller_id)
        
        # Get active downlines for current month
        current_month = "2024-07"
        active_downlines = self._count_active_downlines(reseller_id, current_month)
        
        return {
            'direct_downlines': direct_summary,
            'total_downlines': total_downlines,
            'active_downlines': active_downlines,
            'total_count': sum(direct_summary.values())
        }
    
    def _count_total_downlines(self, reseller_id: int, visited=None) -> int:
        """Recursively count all downlines"""
        if visited is None:
            visited = set()
        
        if reseller_id in visited:
            return 0
        
        visited.add(reseller_id)
        
        # Get direct downlines
        direct_downlines = Reseller.query.filter_by(sponsor_id=reseller_id).all()
        count = len(direct_downlines)
        
        # Add counts from each downline's tree
        for downline in direct_downlines:
            count += self._count_total_downlines(downline.id, visited.copy())
        
        return count
    
    def _count_active_downlines(self, reseller_id: int, month: str) -> Dict:
        """Count active downlines by level for a specific month"""
        from config import Config
        
        active_counts = {'BP': 0, 'IBO': 0, 'BD': 0}
        
        # Get all downlines recursively
        all_downlines = self._get_all_downlines(reseller_id)
        
        for downline in all_downlines:
            # Get sales for the month
            sales = MonthlySales.query.filter_by(
                reseller_id=downline.id,
                month=month
            ).first()
            
            gppis = sales.gppis if sales else Decimal('0')
            
            # Check if active based on level requirements
            threshold = Config.COMMISSION_RULES['active_thresholds'][downline.level]
            if gppis >= threshold:
                active_counts[downline.level] += 1
        
        return active_counts
    
    def _get_all_downlines(self, reseller_id: int, visited=None) -> List[Reseller]:
        """Get all downlines recursively"""
        if visited is None:
            visited = set()
        
        if reseller_id in visited:
            return []
        
        visited.add(reseller_id)
        
        all_downlines = []
        direct_downlines = Reseller.query.filter_by(sponsor_id=reseller_id).all()
        
        for downline in direct_downlines:
            all_downlines.append(downline)
            all_downlines.extend(self._get_all_downlines(downline.id, visited.copy()))
        
        return all_downlines
    
    def update_monthly_sales(self, reseller_id: int, month: str, amount: float) -> bool:
        """
        Update monthly sales for a reseller
        Creates new record if doesn't exist, updates if it does
        """
        try:
            # Find existing record
            sales_record = MonthlySales.query.filter_by(
                reseller_id=reseller_id,
                month=month
            ).first()
            
            if sales_record:
                # Update existing record
                sales_record.gppis = Decimal(str(amount))
                # Update product breakdown (simplified for demo)
                sales_record.premium_sales = Decimal(str(amount * 0.4))
                sales_record.standard_sales = Decimal(str(amount * 0.4))
                sales_record.basic_sales = Decimal(str(amount * 0.2))
            else:
                # Create new record
                sales_record = MonthlySales(
                    reseller_id=reseller_id,
                    month=month,
                    gppis=Decimal(str(amount)),
                    premium_sales=Decimal(str(amount * 0.4)),
                    standard_sales=Decimal(str(amount * 0.4)),
                    basic_sales=Decimal(str(amount * 0.2))
                )
                db.session.add(sales_record)
            
            db.session.commit()
            
            self.logger.info(f"Updated sales for reseller {reseller_id}, month {month}: ₱{amount:,.2f}")
            return True
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error updating sales: {str(e)}")
            return False
    
    def get_dashboard_stats(self, month: str) -> Dict:
        """
        Get dashboard statistics for a specific month
        """
        try:
            # Total sales for the month
            total_sales = db.session.query(
                db.func.sum(MonthlySales.gppis)
            ).filter(MonthlySales.month == month).scalar() or Decimal('0')
            
            # Count resellers by level
            level_counts = db.session.query(
                Reseller.level,
                db.func.count(Reseller.id).label('count')
            ).group_by(Reseller.level).all()
            
            reseller_counts = {level: count for level, count in level_counts}
            
            # Count active resellers by level
            from config import Config
            active_counts = {'BP': 0, 'IBO': 0, 'BD': 0}
            
            for level in ['BP', 'IBO', 'BD']:
                threshold = Config.COMMISSION_RULES['active_thresholds'][level]
                
                # Count active resellers for this level
                active_count = db.session.query(
                    db.func.count(MonthlySales.reseller_id)
                ).join(Reseller).filter(
                    Reseller.level == level,
                    MonthlySales.month == month,
                    MonthlySales.gppis >= threshold
                ).scalar() or 0
                
                active_counts[level] = active_count
            
            # Calculate total commissions (estimated)
            estimated_commissions = float(total_sales) * 0.15  # Average 15% commission rate
            
            # Top performers
            top_performers = db.session.query(
                Reseller.id,
                Reseller.first_name,
                Reseller.last_name,
                Reseller.level,
                MonthlySales.gppis
            ).join(MonthlySales).filter(
                MonthlySales.month == month
            ).order_by(
                MonthlySales.gppis.desc()
            ).limit(5).all()
            
            top_performers_list = [
                {
                    'id': id,
                    'name': f"{first_name} {last_name}",
                    'level': level,
                    'sales': float(gppis)
                }
                for id, first_name, last_name, level, gppis in top_performers
            ]
            
            return {
                'total_sales': float(total_sales),
                'estimated_commissions': estimated_commissions,
                'total_resellers': sum(reseller_counts.values()),
                'reseller_counts': reseller_counts,
                'active_counts': active_counts,
                'top_performers': top_performers_list,
                'month': month
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard stats: {str(e)}")
            raise
    
    def get_reseller_by_code(self, employee_code: str) -> Optional[Reseller]:
        """Get reseller by employee code"""
        return Reseller.query.filter_by(employee_code=employee_code).first()
    
    def search_resellers(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search resellers by name, email, or employee code
        """
        search_pattern = f"%{query}%"
        
        resellers = Reseller.query.filter(
            db.or_(
                Reseller.first_name.ilike(search_pattern),
                Reseller.last_name.ilike(search_pattern),
                Reseller.email.ilike(search_pattern),
                Reseller.employee_code.ilike(search_pattern)
            )
        ).limit(limit).all()
        
        return [reseller.to_dict() for reseller in resellers]