# app/database/sample_data.py - Create realistic sample data for demo

from database.models import (
    db, Organization, Reseller, MonthlySales, 
    CommissionRule, CommissionCalculation, MonthlySummary
)
from datetime import date
from decimal import Decimal

def create_sample_data():
    """Create comprehensive sample data for the MLM system"""
    
    # Check if data already exists
    if Reseller.query.first():
        print("📊 Sample data already exists. Skipping creation.")
        return
    
    print("🏢 Creating organizations...")
    create_organizations()
    
    print("👥 Creating resellers...")
    create_resellers()
    
    print("💰 Creating monthly sales...")
    create_monthly_sales()
    
    print("📋 Creating commission rules...")
    create_commission_rules()
    
    print("✅ Sample data creation completed!")

def create_organizations():
    """Create sample organizations"""
    organizations = [
        Organization(
            name="Santos Marketing Corporation",
            organization_type="corporate",
            address="123 Ayala Avenue, Makati Business District",
            city="Makati",
            province="Metro Manila",
            postal_code="1226",
            phone="+63 2 8123 4567",
            email="info@santosmarketing.ph",
            territory="Metro Manila North"
        ),
        Organization(
            name="Dela Cruz Sales Network",
            organization_type="individual",
            address="456 Quezon Avenue, Quezon City",
            city="Quezon City",
            province="Metro Manila",
            postal_code="1104",
            phone="+63 2 8234 5678",
            email="sales@delacruznetwork.ph",
            territory="Metro Manila East"
        ),
        Organization(
            name="Mendoza Family Business",
            organization_type="individual",
            address="789 Rizal Street, Pasig City",
            city="Pasig",
            province="Metro Manila",
            postal_code="1600",
            phone="+63 2 8345 6789",
            email="contact@mendozafamily.ph",
            territory="Metro Manila Central"
        ),
        Organization(
            name="Morales Direct Sales",
            organization_type="franchise",
            address="321 Bonifacio Street, Manila",
            city="Manila",
            province="Metro Manila",
            postal_code="1000",
            phone="+63 2 8456 7890",
            email="info@moralesdirect.ph",
            territory="Metro Manila South"
        ),
        Organization(
            name="Reyes Retail Outlet",
            organization_type="individual",
            address="654 Taft Avenue, Pasay City",
            city="Pasay",
            province="Metro Manila",
            postal_code="1300",
            phone="+63 2 8567 8901",
            email="reyes@retail.ph",
            territory="Metro Manila West"
        )
    ]
    
    for org in organizations:
        db.session.add(org)
    
    db.session.commit()
    print(f"   Created {len(organizations)} organizations")

def create_resellers():
    """Create sample resellers with hierarchy"""
    resellers_data = [
        # BD Level (Top)
        {
            'employee_code': 'BD001',
            'first_name': 'Maria Isabel',
            'last_name': 'Santos',
            'level': 'BD',
            'position': 'Business Distributor',
            'email': 'maria.santos@sunx.ph',
            'phone': '+63 917 123 4567',
            'sponsor_id': None,
            'organization_id': 1,
            'join_date': date(2022, 1, 15),
            'promotion_date': date(2022, 6, 15),
            'avatar_initials': 'MS',
            'territory': 'Metro Manila North'
        },
        
        # IBO Level (Second tier)
        {
            'employee_code': 'IBO001',
            'first_name': 'Juan Carlos',
            'last_name': 'Dela Cruz',
            'level': 'IBO',
            'position': 'Independent Business Owner',
            'email': 'juan.delacruz@sunx.ph',
            'phone': '+63 917 234 5678',
            'sponsor_id': 1,  # Under Maria Santos
            'organization_id': 2,
            'join_date': date(2022, 3, 20),
            'promotion_date': date(2022, 8, 20),
            'avatar_initials': 'JD',
            'territory': 'Metro Manila East'
        },
        {
            'employee_code': 'IBO002',
            'first_name': 'Rosa Maria',
            'last_name': 'Mendoza',
            'level': 'IBO',
            'position': 'Independent Business Owner',
            'email': 'rosa.mendoza@sunx.ph',
            'phone': '+63 917 345 6789',
            'sponsor_id': 1,  # Under Maria Santos
            'organization_id': 3,
            'join_date': date(2022, 2, 10),
            'promotion_date': date(2022, 7, 10),
            'avatar_initials': 'RM',
            'territory': 'Metro Manila Central'
        },
        {
            'employee_code': 'IBO003',
            'first_name': 'Pedro Alfonso',
            'last_name': 'Morales',
            'level': 'IBO',
            'position': 'Independent Business Owner',
            'email': 'pedro.morales@sunx.ph',
            'phone': '+63 917 456 7890',
            'sponsor_id': 2,  # Under Juan Dela Cruz
            'organization_id': 4,
            'join_date': date(2023, 4, 15),
            'promotion_date': date(2023, 9, 15),
            'avatar_initials': 'PM',
            'territory': 'Metro Manila South'
        },
        
        # BP Level (Third tier)
        {
            'employee_code': 'BP001',
            'first_name': 'Carlos Miguel',
            'last_name': 'Reyes',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'carlos.reyes@sunx.ph',
            'phone': '+63 917 567 8901',
            'sponsor_id': 2,  # Under Juan Dela Cruz
            'organization_id': 5,
            'join_date': date(2023, 5, 12),
            'avatar_initials': 'CR',
            'territory': 'Metro Manila West'
        },
        {
            'employee_code': 'BP002',
            'first_name': 'Ana Patricia',
            'last_name': 'Garcia',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'ana.garcia@sunx.ph',
            'phone': '+63 917 678 9012',
            'sponsor_id': 2,  # Under Juan Dela Cruz
            'organization_id': 2,
            'join_date': date(2023, 6, 8),
            'avatar_initials': 'AG',
            'territory': 'Quezon City North'
        },
        {
            'employee_code': 'BP003',
            'first_name': 'Carmen Teresa',
            'last_name': 'Lopez',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'carmen.lopez@sunx.ph',
            'phone': '+63 917 789 0123',
            'sponsor_id': 3,  # Under Rosa Mendoza
            'organization_id': 3,
            'join_date': date(2023, 7, 22),
            'avatar_initials': 'CL',
            'territory': 'Pasig North'
        },
        {
            'employee_code': 'BP004',
            'first_name': 'Rico Emmanuel',
            'last_name': 'Hernandez',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'rico.hernandez@sunx.ph',
            'phone': '+63 917 890 1234',
            'sponsor_id': 3,  # Under Rosa Mendoza
            'organization_id': 3,
            'join_date': date(2023, 8, 10),
            'avatar_initials': 'RH',
            'territory': 'Pasig South'
        },
        {
            'employee_code': 'BP005',
            'first_name': 'Sofia Isabella',
            'last_name': 'Ramos',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'sofia.ramos@sunx.ph',
            'phone': '+63 917 901 2345',
            'sponsor_id': 3,  # Under Rosa Mendoza
            'organization_id': 3,
            'join_date': date(2023, 9, 15),
            'avatar_initials': 'SR',
            'territory': 'Marikina'
        },
        {
            'employee_code': 'BP006',
            'first_name': 'Miguel Antonio',
            'last_name': 'Villanueva',
            'level': 'BP',
            'position': 'Business Partner',
            'email': 'miguel.villanueva@sunx.ph',
            'phone': '+63 917 012 3456',
            'sponsor_id': 4,  # Under Pedro Morales
            'organization_id': 4,
            'join_date': date(2023, 10, 20),
            'avatar_initials': 'MV',
            'territory': 'Manila East'
        }
    ]
    
    for reseller_data in resellers_data:
        reseller = Reseller(**reseller_data)
        db.session.add(reseller)
    
    db.session.commit()
    print(f"   Created {len(resellers_data)} resellers")

def create_monthly_sales():
    """Create monthly sales data for the last 3 months"""
    months = ['2024-05', '2024-06', '2024-07']
    
    # Sales data for each reseller by month
    sales_data = {
        1: {'2024-05': 142000, '2024-06': 118000, '2024-07': 125000},  # Maria Santos (BD)
        2: {'2024-05': 92000, '2024-06': 78000, '2024-07': 85000},    # Juan Dela Cruz (IBO)
        3: {'2024-05': 72000, '2024-06': 85000, '2024-07': 78000},    # Rosa Mendoza (IBO)
        4: {'2024-05': 28000, '2024-06': 32000, '2024-07': 25000},    # Pedro Morales (IBO)
        5: {'2024-05': 8000, '2024-06': 15000, '2024-07': 12000},     # Carlos Reyes (BP)
        6: {'2024-05': 16000, '2024-06': 22000, '2024-07': 18000},    # Ana Garcia (BP)
        7: {'2024-05': 12000, '2024-06': 18000, '2024-07': 15000},    # Carmen Lopez (BP)
        8: {'2024-05': 6000, '2024-06': 12000, '2024-07': 8000},      # Rico Hernandez (BP)
        9: {'2024-05': 25000, '2024-06': 28000, '2024-07': 22000},    # Sofia Ramos (BP)
        10: {'2024-05': 11000, '2024-06': 16000, '2024-07': 14000}    # Miguel Villanueva (BP)
    }
    
    for reseller_id, monthly_data in sales_data.items():
        for month, gppis in monthly_data.items():
            # Create basic sales breakdown (for demonstration)
            premium_pct = 0.4 if reseller_id <= 4 else 0.2  # Higher levels sell more premium
            standard_pct = 0.4
            basic_pct = 1 - premium_pct - standard_pct
            
            sales_record = MonthlySales(
                reseller_id=reseller_id,
                month=month,
                gppis=Decimal(str(gppis)),
                premium_sales=Decimal(str(gppis * premium_pct)),
                standard_sales=Decimal(str(gppis * standard_pct)),
                basic_sales=Decimal(str(gppis * basic_pct))
            )
            db.session.add(sales_record)
    
    db.session.commit()
    print(f"   Created sales data for {len(months)} months")

def create_commission_rules():
    """Create commission rules in the database"""
    rules = [
        # Outright Discount Rules
        CommissionRule(
            name="BP Outright - SUNX Premium",
            rule_type="outright_discount",
            level="BP",
            product_category="SUNX-PREMIUM",
            parameters={"rate": 0.25}
        ),
        CommissionRule(
            name="BP Outright - SUNX Standard",
            rule_type="outright_discount",
            level="BP",
            product_category="SUNX-STANDARD",
            parameters={"rate": 0.20}
        ),
        CommissionRule(
            name="BP Outright - SUNX Basic",
            rule_type="outright_discount",
            level="BP",
            product_category="SUNX-BASIC",
            parameters={"rate": 0.15}
        ),
        
        # IBO Rules
        CommissionRule(
            name="IBO Outright - SUNX Premium",
            rule_type="outright_discount",
            level="IBO",
            product_category="SUNX-PREMIUM",
            parameters={"rate": 0.40}
        ),
        CommissionRule(
            name="IBO Outright - SUNX Standard",
            rule_type="outright_discount",
            level="IBO",
            product_category="SUNX-STANDARD",
            parameters={"rate": 0.35}
        ),
        CommissionRule(
            name="IBO Outright - SUNX Basic",
            rule_type="outright_discount",
            level="IBO",
            product_category="SUNX-BASIC",
            parameters={"rate": 0.28}
        ),
        
        # Group Override Rules
        CommissionRule(
            name="IBO Group Override - Silver",
            rule_type="group_override",
            level="IBO",
            parameters={
                "tier": "silver",
                "min_active_bps": 3,
                "min_ggpis": 50000,
                "rate": 0.05
            }
        ),
        CommissionRule(
            name="IBO Group Override - Gold",
            rule_type="group_override",
            level="IBO",
            parameters={
                "tier": "gold",
                "min_active_bps": 5,
                "min_ggpis": 100000,
                "rate": 0.06
            }
        ),
        CommissionRule(
            name="IBO Group Override - Diamond",
            rule_type="group_override",
            level="IBO",
            parameters={
                "tier": "diamond",
                "min_active_bps": 8,
                "min_ggpis": 180000,
                "rate": 0.08
            }
        ),
        
        # BD Service Fee Rules
        CommissionRule(
            name="BD Service Fee - Tier 1",
            rule_type="bd_service_fee",
            level="BD",
            parameters={
                "tier": 1,
                "min_ggpis": 1000000,
                "rate": 0.05,
                "min_active_ibos": 15
            }
        ),
        CommissionRule(
            name="BD Service Fee - Tier 2",
            rule_type="bd_service_fee",
            level="BD",
            parameters={
                "tier": 2,
                "min_ggpis": 2500000,
                "rate": 0.06,
                "min_active_ibos": 15
            }
        ),
        CommissionRule(
            name="BD Service Fee - Tier 3",
            rule_type="bd_service_fee",
            level="BD",
            parameters={
                "tier": 3,
                "min_ggpis": 4000000,
                "rate": 0.07,
                "min_active_ibos": 15
            }
        ),
        
        # Lifetime Incentive
        CommissionRule(
            name="IBO Lifetime Incentive",
            rule_type="lifetime_incentive",
            level="IBO",
            parameters={
                "rate": 0.02,
                "min_gppis_both": 10000
            }
        )
    ]
    
    for rule in rules:
        db.session.add(rule)
    
    db.session.commit()
    print(f"   Created {len(rules)} commission rules")

def get_sample_reseller_data():
    """Get sample reseller data for quick reference"""
    return {
        'hierarchy': {
            'BD001': {
                'name': 'Maria Isabel Santos',
                'level': 'BD',
                'downlines': ['IBO001', 'IBO002']
            },
            'IBO001': {
                'name': 'Juan Carlos Dela Cruz',
                'level': 'IBO',
                'downlines': ['IBO003', 'BP001', 'BP002']
            },
            'IBO002': {
                'name': 'Rosa Maria Mendoza',
                'level': 'IBO',
                'downlines': ['BP003', 'BP004', 'BP005']
            },
            'IBO003': {
                'name': 'Pedro Alfonso Morales',
                'level': 'IBO',
                'downlines': ['BP006']
            }
        },
        'total_resellers': 10,
        'levels': {'BD': 1, 'IBO': 3, 'BP': 6}
    }