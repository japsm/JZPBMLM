# app/services/commission_engine.py - MLM Commission Calculation Engine

from database.models import (
    db, Reseller, MonthlySales, CommissionCalculation, 
    MonthlySummary, CommissionRule
)
from config import Config
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import logging

class CommissionEngine:
    """
    Core commission calculation engine for SUNX MLM system
    Handles all commission types according to business rules
    """
    
    def __init__(self):
        self.rules = Config.COMMISSION_RULES
        self.logger = logging.getLogger(__name__)
    
    def calculate_monthly_commissions(self, reseller_id: int, month: str) -> Dict:
        """
        Calculate all commissions for a specific reseller and month
        Returns complete commission breakdown
        """
        reseller = Reseller.query.get(reseller_id)
        if not reseller:
            raise ValueError(f"Reseller {reseller_id} not found")
        
        # Get GPPIS and GGPIS
        gppis = self._get_gppis(reseller_id, month)
        ggpis = self._calculate_ggpis(reseller_id, month)
        
        # Initialize commission structure
        commissions = {
            'reseller_id': reseller_id,
            'reseller_name': reseller.full_name,
            'level': reseller.level,
            'month': month,
            'gppis': float(gppis),
            'ggpis': float(ggpis),
            'active_status': self._check_active_status(reseller, gppis),
            'commissions': [],
            'total_commission': 0,
            'qualifications': {}
        }
        
        try:
            # Calculate different commission types based on level
            if reseller.level in ['BP', 'IBO', 'BD']:
                self._calculate_outright_discount(commissions, reseller, month, gppis)
            
            if reseller.level == 'IBO':
                self._calculate_group_override(commissions, reseller, month, ggpis)
                self._calculate_lifetime_incentive(commissions, reseller, month, gppis)
            
            if reseller.level == 'BD':
                self._calculate_bd_service_fee(commissions, reseller, month, gppis, ggpis)
                self._calculate_bd_override(commissions, reseller, month, ggpis)
            
            # Calculate promotion eligibility for BPs
            if reseller.level == 'BP':
                commissions['qualifications']['promotion'] = self._check_promotion_eligibility(
                    reseller, month, gppis
                )
            
            # Calculate total
            commissions['total_commission'] = sum(
                c['amount'] for c in commissions['commissions']
            )
            
            self.logger.info(f"Calculated commissions for {reseller.full_name}: ₱{commissions['total_commission']:,.2f}")
            
        except Exception as e:
            self.logger.error(f"Error calculating commissions for {reseller.full_name}: {str(e)}")
            raise
        
        return commissions
    
    def _get_gppis(self, reseller_id: int, month: str) -> Decimal:
        """Get Gross Personal Paid-In Sales for reseller and month"""
        sales = MonthlySales.query.filter_by(
            reseller_id=reseller_id,
            month=month
        ).first()
        return sales.gppis if sales else Decimal('0')
    
    def _calculate_ggpis(self, reseller_id: int, month: str, visited=None) -> Decimal:
        """
        Calculate Gross Group Paid-In Sales (including all downline sales)
        Uses recursive traversal with cycle detection
        """
        if visited is None:
            visited = set()
        
        if reseller_id in visited:
            return Decimal('0')  # Prevent infinite loops
        
        visited.add(reseller_id)
        
        # Start with personal sales
        personal_sales = self._get_gppis(reseller_id, month)
        group_sales = personal_sales
        
        # Add all downline sales recursively
        downlines = Reseller.query.filter_by(sponsor_id=reseller_id).all()
        for downline in downlines:
            downline_ggpis = self._calculate_ggpis(downline.id, month, visited.copy())
            group_sales += downline_ggpis
        
        return group_sales
    
    def _check_active_status(self, reseller: Reseller, gppis: Decimal) -> bool:
        """Check if reseller meets active status requirements"""
        threshold = self.rules['active_thresholds'][reseller.level]
        return gppis >= threshold
    
    def _calculate_outright_discount(self, commissions: Dict, reseller: Reseller, 
                                   month: str, gppis: Decimal):
        """Calculate outright discount commissions based on product sales"""
        if gppis <= 0:
            return
        
        # For demo purposes, assume even distribution across product categories
        sales_breakdown = {
            'SUNX-PREMIUM': gppis * Decimal('0.4'),
            'SUNX-STANDARD': gppis * Decimal('0.4'),
            'SUNX-BASIC': gppis * Decimal('0.2')
        }
        
        for product, sales_amount in sales_breakdown.items():
            if sales_amount > 0:
                rate = Decimal(str(self.rules['outright_discount'][product][reseller.level]))
                commission_amount = sales_amount * rate
                
                commissions['commissions'].append({
                    'type': 'outright_discount',
                    'product': product,
                    'base_amount': float(sales_amount),
                    'rate': float(rate),
                    'amount': float(commission_amount),
                    'description': f'{reseller.level} Outright Discount - {product}'
                })
    
    def _calculate_group_override(self, commissions: Dict, reseller: Reseller,
                                month: str, ggpis: Decimal):
        """Calculate IBO group override commissions"""
        # Count active BPs in first level
        direct_bps = Reseller.query.filter_by(
            sponsor_id=reseller.id,
            level='BP'
        ).all()
        
        active_bps = []
        for bp in direct_bps:
            bp_gppis = self._get_gppis(bp.id, month)
            if bp_gppis >= self.rules['active_thresholds']['BP']:
                active_bps.append(bp)
        
        active_bp_count = len(active_bps)
        
        # Determine override tier
        override_tier = None
        rules = self.rules['group_override']
        
        if (active_bp_count >= rules['diamond']['min_active_bps'] and 
            ggpis >= rules['diamond']['min_ggpis']):
            override_tier = 'diamond'
        elif (active_bp_count >= rules['gold']['min_active_bps'] and 
              ggpis >= rules['gold']['min_ggpis']):
            override_tier = 'gold'
        elif (active_bp_count >= rules['silver']['min_active_bps'] and 
              ggpis >= rules['silver']['min_ggpis']):
            override_tier = 'silver'
        
        if override_tier:
            rate = Decimal(str(rules[override_tier]['rate']))
            commission_amount = ggpis * rate
            
            commissions['commissions'].append({
                'type': 'group_override',
                'tier': override_tier.title(),
                'active_bps': active_bp_count,
                'base_amount': float(ggpis),
                'rate': float(rate),
                'amount': float(commission_amount),
                'description': f'Group Override - {override_tier.title()} ({active_bp_count} Active BPs)'
            })
            
            commissions['qualifications']['group_override'] = {
                'tier': override_tier.title(),
                'active_bps': active_bp_count,
                'rate': float(rate)
            }
    
    def _calculate_lifetime_incentive(self, commissions: Dict, reseller: Reseller,
                                    month: str, gppis: Decimal):
        """Calculate lifetime incentive for IBO on downline IBOs"""
        min_gppis = self.rules['lifetime_incentive']['min_gppis']
        
        # Check if reseller qualifies (≥₱10K GPPIS)
        if gppis < min_gppis:
            return
        
        # Find direct IBO downlines with ≥₱10K GPPIS
        direct_ibos = Reseller.query.filter_by(
            sponsor_id=reseller.id,
            level='IBO'
        ).all()
        
        qualifying_ibos = []
        total_qualifying_gppis = Decimal('0')
        
        for ibo in direct_ibos:
            ibo_gppis = self._get_gppis(ibo.id, month)
            if ibo_gppis >= min_gppis:
                qualifying_ibos.append({
                    'name': ibo.full_name,
                    'gppis': float(ibo_gppis)
                })
                total_qualifying_gppis += ibo_gppis
        
        if qualifying_ibos:
            rate = Decimal(str(self.rules['lifetime_incentive']['rate']))
            commission_amount = total_qualifying_gppis * rate
            
            commissions['commissions'].append({
                'type': 'lifetime_incentive',
                'qualifying_ibos': len(qualifying_ibos),
                'base_amount': float(total_qualifying_gppis),
                'rate': float(rate),
                'amount': float(commission_amount),
                'description': f'Lifetime Incentive ({len(qualifying_ibos)} Qualifying IBOs)',
                'details': qualifying_ibos
            })
    
    def _calculate_bd_service_fee(self, commissions: Dict, reseller: Reseller,
                                month: str, gppis: Decimal, ggpis: Decimal):
        """Calculate BD service fee commissions"""
        # Check if BD is active (≥₱10K GPPIS)
        if gppis < self.rules['active_thresholds']['BD']:
            return
        
        # Count active IBOs in entire downline
        active_ibos_count = self._count_active_ibos_downline(reseller.id, month)
        
        # Check minimum IBO requirement
        if active_ibos_count < self.rules['bd_service_fee']['min_active_ibos']:
            return
        
        # Determine service fee tier
        rules = self.rules['bd_service_fee']
        tier = None
        
        if ggpis >= rules['tier3']['min_ggpis']:
            tier = 'tier3'
        elif ggpis >= rules['tier2']['min_ggpis']:
            tier = 'tier2'
        elif ggpis >= rules['tier1']['min_ggpis']:
            tier = 'tier1'
        
        if tier:
            rate = Decimal(str(rules[tier]['rate']))
            commission_amount = ggpis * rate
            tier_name = f"Tier {tier[-1]}"
            
            commissions['commissions'].append({
                'type': 'bd_service_fee',
                'tier': tier_name,
                'active_ibos': active_ibos_count,
                'base_amount': float(ggpis),
                'rate': float(rate),
                'amount': float(commission_amount),
                'description': f'BD Service Fee - {tier_name} ({active_ibos_count} Active IBOs)'
            })
            
            commissions['qualifications']['bd_service_fee'] = {
                'tier': tier_name,
                'active_ibos': active_ibos_count,
                'rate': float(rate)
            }
    
    def _count_active_ibos_downline(self, reseller_id: int, month: str, visited=None) -> int:
        """Count all active IBOs in entire downline tree"""
        if visited is None:
            visited = set()
        
        if reseller_id in visited:
            return 0
        
        visited.add(reseller_id)
        
        count = 0
        downlines = Reseller.query.filter_by(sponsor_id=reseller_id).all()
        
        for downline in downlines:
            # Count if this downline is an active IBO
            if downline.level == 'IBO':
                downline_gppis = self._get_gppis(downline.id, month)
                if downline_gppis >= self.rules['active_thresholds']['IBO_BD_CALC']:
                    count += 1
            
            # Recursively count in their downlines
            count += self._count_active_ibos_downline(downline.id, month, visited.copy())
        
        return count
    
    def _calculate_bd_override(self, commissions: Dict, reseller: Reseller,
                             month: str, ggpis: Decimal):
        """Calculate BD override on direct BD downlines"""
        min_ggpis = self.rules['bd_override']['min_ggpis_both']
        
        # Check if this BD qualifies (≥₱1M GGPIS)
        if ggpis < min_ggpis:
            return
        
        # Find direct BD downlines
        direct_bds = Reseller.query.filter_by(
            sponsor_id=reseller.id,
            level='BD'
        ).all()
        
        qualifying_bds = []
        total_qualifying_ggpis = Decimal('0')
        
        for bd in direct_bds:
            bd_ggpis = self._calculate_ggpis(bd.id, month)
            if bd_ggpis >= min_ggpis:
                qualifying_bds.append({
                    'name': bd.full_name,
                    'ggpis': float(bd_ggpis)
                })
                total_qualifying_ggpis += bd_ggpis
        
        if qualifying_bds:
            rate = Decimal(str(self.rules['bd_override']['rate']))
            commission_amount = total_qualifying_ggpis * rate
            
            commissions['commissions'].append({
                'type': 'bd_override',
                'qualifying_bds': len(qualifying_bds),
                'base_amount': float(total_qualifying_ggpis),
                'rate': float(rate),
                'amount': float(commission_amount),
                'description': f'BD Override ({len(qualifying_bds)} Qualifying BDs)',
                'details': qualifying_bds
            })
    
    def _check_promotion_eligibility(self, reseller: Reseller, month: str, 
                                   gppis: Decimal) -> Dict:
        """Check BP promotion eligibility to IBO"""
        threshold = self.rules['promotion']['bp_to_ibo_threshold']
        progress = (gppis / threshold) * 100
        
        # Get previous month GPPIS for 2-month requirement
        prev_month = self._get_previous_month(month)
        prev_gppis = self._get_gppis(reseller.id, prev_month)
        
        consecutive_qualified = (gppis >= threshold and prev_gppis >= threshold)
        
        return {
            'current_gppis': float(gppis),
            'required_gppis': float(threshold),
            'progress_percentage': min(float(progress), 100.0),
            'eligible': gppis >= threshold,
            'consecutive_months_qualified': consecutive_qualified,
            'amount_needed': max(float(threshold - gppis), 0),
            'previous_month_gppis': float(prev_gppis)
        }
    
    def _get_previous_month(self, month: str) -> str:
        """Get previous month string (YYYY-MM format)"""
        year, month_num = map(int, month.split('-'))
        if month_num == 1:
            return f"{year-1}-12"
        else:
            return f"{year}-{month_num-1:02d}"
    
    def get_promotion_candidates(self, month: str) -> List[Dict]:
        """Get all BP promotion candidates for a specific month"""
        bps = Reseller.query.filter_by(level='BP').all()
        candidates = []
        
        for bp in bps:
            gppis = self._get_gppis(bp.id, month)
            eligibility = self._check_promotion_eligibility(bp, month, gppis)
            
            # Include candidates with >50% progress
            if eligibility['progress_percentage'] > 50:
                candidates.append({
                    'reseller_id': bp.id,
                    'name': bp.full_name,
                    'employee_code': bp.employee_code,
                    'organization': bp.organization.name if bp.organization else '',
                    'eligibility': eligibility
                })
        
        # Sort by progress percentage
        candidates.sort(key=lambda x: x['eligibility']['progress_percentage'], reverse=True)
        
        return candidates