import React, { useState, useEffect } from 'react';
import { 
  Users, 
  TrendingUp, 
  DollarSign, 
  Award, 
  Settings, 
  BarChart3, 
  UserPlus, 
  Target,
  ChevronDown,
  ChevronRight,
  Star,
  Calendar,
  PlusCircle,
  Edit,
  Eye,
  Crown,
  Diamond,
  Medal
} from 'lucide-react';

// SUNX MLM Commission Rules based on the provided documents
const commissionRules = {
  BP: {
    outright_discount: [0.15, 0.20, 0.25], // 15%, 20%, 25% based on product
    group_override: null,
    lifetime_incentive: null,
    min_gppis_active: 2000, // ₱2K for active status
    promotion_threshold: 50000, // ₱50K GPPIS in 2 months
    promotion_bond: 25000 // ₱25K security bond option
  },
  IBO: {
    outright_discount: [0.28, 0.35, 0.40], // 28%, 35%, 40%
    group_override: {
      silver: { min_active_bps: 3, min_ggpis: 50000, rate: 0.05 },
      gold: { min_active_bps: 5, min_ggpis: 100000, rate: 0.06 },
      diamond: { min_active_bps: 8, min_ggpis: 180000, rate: 0.08 }
    },
    lifetime_incentive: {
      rate: 0.02, // 2% of downline IBOs GPPIS
      min_gppis_self: 10000, // ₱10K GPPIS
      min_gppis_downline: 10000 // ₱10K GPPIS for downline IBO
    },
    min_gppis_active: 2000, // ₱2K for basic active status
    min_gppis_bd_active: 10000 // ₱10K for BD service fee counting
  },
  BD: {
    outright_discount: [0.28, 0.35, 0.40], // Inherits IBO level
    group_service_fee: {
      tier1: { min_ggpis: 1000000, rate: 0.05 }, // ₱1M → 5%
      tier2: { min_ggpis: 2500000, rate: 0.06 }, // ₱2.5M → 6%
      tier3: { min_ggpis: 4000000, rate: 0.07 }  // ₱4M → 7%
    },
    bd_override: {
      rate: 0.01, // 1% on 1st-level BD downlines GGPIS
      min_ggpis_both: 1000000 // Both BDs need ≥₱1M GGPIS
    },
    min_active_ibos: 15, // Must maintain 15 Active IBOs
    min_gppis_active: 10000 // ₱10K for BD active status
  }
};

// Product-specific discount rates
const productDiscountRates = {
  "SUNX-PREMIUM": { BP: 0.25, IBO: 0.40, BD: 0.40 },
  "SUNX-STANDARD": { BP: 0.20, IBO: 0.35, BD: 0.35 },
  "SUNX-BASIC": { BP: 0.15, IBO: 0.28, BD: 0.28 }
};

// Sample hierarchy data with Philippine peso amounts
const initialHierarchy = {
  "user1": {
    id: "user1",
    name: "Maria Santos",
    level: "BD",
    parentId: null,
    gppis: 125000, // ₱125K
    ggpis: 4500000, // ₱4.5M
    active: true,
    joinDate: "2023-01-15",
    children: ["user2", "user3"],
    promotionDate: null // For tracking promotion timeline
  },
  "user2": {
    id: "user2",
    name: "Juan Dela Cruz",
    level: "IBO",
    parentId: "user1",
    gppis: 85000, // ₱85K
    ggpis: 220000, // ₱220K
    active: true,
    joinDate: "2023-03-20",
    children: ["user4", "user5", "user6"],
    promotionDate: "2023-05-20" // Promoted to IBO
  },
  "user3": {
    id: "user3",
    name: "Rosa Mendoza",
    level: "IBO",
    parentId: "user1",
    gppis: 78000, // ₱78K
    ggpis: 185000, // ₱185K
    active: true,
    joinDate: "2023-02-10",
    children: ["user7", "user8"],
    promotionDate: "2023-04-10" // Promoted to IBO
  },
  "user4": {
    id: "user4",
    name: "Carlos Reyes",
    level: "BP",
    parentId: "user2",
    gppis: 12000, // ₱12K
    ggpis: 12000,
    active: true,
    joinDate: "2023-05-12",
    children: [],
    promotionDate: null // Still BP, tracking for promotion
  },
  "user5": {
    id: "user5",
    name: "Ana Garcia",
    level: "BP",
    parentId: "user2",
    gppis: 8000, // ₱8K
    ggpis: 8000,
    active: true,
    joinDate: "2023-06-08",
    children: [],
    promotionDate: null
  },
  "user6": {
    id: "user6",
    name: "Pedro Morales",
    level: "IBO",
    parentId: "user2",
    gppis: 25000, // ₱25K
    ggpis: 25000,
    active: true,
    joinDate: "2023-04-15",
    children: [],
    promotionDate: "2023-06-15" // Promoted to IBO
  },
  "user7": {
    id: "user7",
    name: "Carmen Lopez",
    level: "BP",
    parentId: "user3",
    gppis: 15000, // ₱15K
    ggpis: 15000,
    active: true,
    joinDate: "2023-07-22",
    children: [],
    promotionDate: null
  },
  "user8": {
    id: "user8",
    name: "Rico Hernandez",
    level: "BP",
    parentId: "user3",
    gppis: 5000, // ₱5K
    ggpis: 5000,
    active: true,
    joinDate: "2023-08-10",
    children: [],
    promotionDate: null
  }
};

const sampleSales = [
  { id: 1, resellerId: "user4", amount: 12000, date: "2024-07-01", type: "POS", status: "confirmed", product: "SUNX-BASIC" },
  { id: 2, resellerId: "user5", amount: 28000, date: "2024-07-02", type: "Sale Order", status: "confirmed", product: "SUNX-STANDARD" },
  { id: 3, resellerId: "user7", amount: 15000, date: "2024-07-03", type: "POS", status: "confirmed", product: "SUNX-PREMIUM" },
  { id: 4, resellerId: "user2", amount: 35000, date: "2024-07-04", type: "Sale Order", status: "confirmed", product: "SUNX-STANDARD" },
  { id: 5, resellerId: "user3", amount: 18000, date: "2024-07-05", type: "POS", status: "pending", product: "SUNX-PREMIUM" }
];

// Enhanced commission calculation engine for SUNX MLM
const calculateCommissions = (sale, hierarchy, rules) => {
  const reseller = hierarchy[sale.resellerId];
  if (!reseller || !reseller.active) return [];

  const commissions = [];

  // 1. Outright Discount for the reseller (product-specific rates)
  const discountRate = productDiscountRates[sale.product]?.[reseller.level] || 0;
  
  commissions.push({
    userId: reseller.id,
    userName: reseller.name,
    type: "outright_discount",
    rate: discountRate,
    amount: sale.amount * discountRate,
    saleId: sale.id,
    product: sale.product
  });

  // 2. Group Override (IBO only)
  if (reseller.level === 'IBO') {
    const overrideTier = calculateGroupOverrideTier(reseller, hierarchy);
    if (overrideTier) {
      commissions.push({
        userId: reseller.id,
        userName: reseller.name,
        type: "group_override",
        rate: overrideTier.rate,
        amount: sale.amount * overrideTier.rate,
        saleId: sale.id,
        tier: overrideTier.name
      });
    }
  }

  // 3. Lifetime Incentive (IBO on 1st-level IBO downlines only)
  let current = reseller;
  while (current.parentId) {
    current = hierarchy[current.parentId];
    if (current && current.level === 'IBO' && reseller.level === 'IBO') {
      const lifetimeRule = rules.IBO.lifetime_incentive;
      // Check if both IBO and downline IBO meet ₱10K GPPIS requirement
      if (current.gppis >= lifetimeRule.min_gppis_self && 
          reseller.gppis >= lifetimeRule.min_gppis_downline) {
        // Apply to ALL 1st-level IBO downlines' GPPIS
        const firstLevelIBOs = current.children
          .map(childId => hierarchy[childId])
          .filter(child => child && child.level === 'IBO' && child.gppis >= lifetimeRule.min_gppis_downline);
        
        firstLevelIBOs.forEach(iboDownline => {
          commissions.push({
            userId: current.id,
            userName: current.name,
            type: "lifetime_incentive",
            rate: lifetimeRule.rate,
            amount: iboDownline.gppis * lifetimeRule.rate,
            saleId: sale.id,
            source: iboDownline.name
          });
        });
      }
      break; // Only apply to immediate upline IBO
    }
  }

  // 4. BD Group Service Fee
  current = reseller;
  while (current.parentId) {
    current = hierarchy[current.parentId];
    if (current && current.level === 'BD') {
      const serviceFee = calculateBDServiceFee(current, hierarchy);
      if (serviceFee) {
        commissions.push({
          userId: current.id,
          userName: current.name,
          type: "bd_service_fee",
          rate: serviceFee.rate,
          amount: sale.amount * serviceFee.rate,
          saleId: sale.id,
          tier: serviceFee.tier
        });
      }
    }
  }

  // 5. BD Override (BD on 1st-level BD downlines)
  if (reseller.level === 'BD') {
    let current = reseller;
    while (current.parentId) {
      current = hierarchy[current.parentId];
      if (current && current.level === 'BD') {
        const bdOverrideRule = rules.BD.bd_override;
        // Both BDs must have ≥₱1M GGPIS
        if (current.ggpis >= bdOverrideRule.min_ggpis_both && 
            reseller.ggpis >= bdOverrideRule.min_ggpis_both) {
          commissions.push({
            userId: current.id,
            userName: current.name,
            type: "bd_override",
            rate: bdOverrideRule.rate,
            amount: reseller.ggpis * bdOverrideRule.rate,
            saleId: sale.id,
            source: reseller.name
          });
        }
        break; // Only apply to immediate upline BD
      }
    }
  }

  return commissions;
};

// Calculate IBO Group Override Tier (only qualifying BPs count)
const calculateGroupOverrideTier = (ibo, hierarchy) => {
  const rule = commissionRules.IBO.group_override;
  
  // Count active BPs in 1st level (≥₱2K GPPIS each)
  const activeBPs = ibo.children
    .map(childId => hierarchy[childId])
    .filter(child => child && child.level === 'BP' && child.gppis >= commissionRules.BP.min_gppis_active)
    .length;

    // Check tier eligibility - only need the required number of active BPs
  if (activeBPs >= rule.diamond.min_active_bps && ibo.ggpis >= rule.diamond.min_ggpis) {
    return { name: 'Diamond', rate: rule.diamond.rate };
  } else if (activeBPs >= rule.gold.min_active_bps && ibo.ggpis >= rule.gold.min_ggpis) {
    return { name: 'Gold', rate: rule.gold.rate };
  } else if (activeBPs >= rule.silver.min_active_bps && ibo.ggpis >= rule.silver.min_ggpis) {
    return { name: 'Silver', rate: rule.silver.rate };
  }
  
  return null;
};

// Check BP promotion eligibility (2 consecutive months with month-end cutoffs)
const checkPromotionEligibility = (user, currentDate = "2024-07-31") => {
  if (user.level !== 'BP') return null;
  
  const joinDate = new Date(user.joinDate);
  const current = new Date(currentDate);
  
  // Calculate months since joining
  const monthsSinceJoin = (current.getFullYear() - joinDate.getFullYear()) * 12 + 
                         (current.getMonth() - joinDate.getMonth());
  
  // For demonstration, assume they need ₱50K GPPIS within 2 consecutive months
  const progress = (user.gppis / commissionRules.BP.promotion_threshold) * 100;
  
  return {
    eligible: progress >= 100,
    progress: Math.min(progress, 100),
    monthsTracked: Math.min(monthsSinceJoin + 1, 2),
    monthsRemaining: Math.max(2 - monthsSinceJoin - 1, 0),
    volumeNeeded: Math.max(commissionRules.BP.promotion_threshold - user.gppis, 0)
  };
};

// Calculate BD Service Fee Tier (count all downline IBOs at all levels)
const calculateBDServiceFee = (bd, hierarchy) => {
  const rule = commissionRules.BD.group_service_fee;
  
  // Check if BD is active (≥₱10K GPPIS)
  if (bd.gppis < commissionRules.BD.min_gppis_active) return null;
  
  // Count active IBOs in entire downline tree (≥₱10K GPPIS each)
  const countActiveIBOs = (userId, visited = new Set()) => {
    if (visited.has(userId)) return 0;
    visited.add(userId);
    
    const user = hierarchy[userId];
    if (!user) return 0;
    
    let count = 0;
    // Count this user if they're an IBO with ≥₱10K GPPIS
    if (user.level === 'IBO' && user.gppis >= commissionRules.IBO.min_gppis_bd_active) {
      count = 1;
    }
    
    // Recursively count in all children
    user.children.forEach(childId => {
      count += countActiveIBOs(childId, visited);
    });
    
    return count;
  };
  
  const activeIBOs = countActiveIBOs(bd.id);
  
  // Must maintain 15+ Active IBOs across entire downline
  if (activeIBOs < commissionRules.BD.min_active_ibos) return null;
  
  // Determine tier based on GGPIS
  if (bd.ggpis >= rule.tier3.min_ggpis) {
    return { tier: 'Tier 3', rate: rule.tier3.rate };
  } else if (bd.ggpis >= rule.tier2.min_ggpis) {
    return { tier: 'Tier 2', rate: rule.tier2.rate };
  } else if (bd.ggpis >= rule.tier1.min_ggpis) {
    return { tier: 'Tier 1', rate: rule.tier1.rate };
  }
  
  return null;
};

// Main App Component
const MLMCommissionApp = () => {
  const [hierarchy, setHierarchy] = useState(initialHierarchy);
  const [sales, setSales] = useState(sampleSales);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [expandedNodes, setExpandedNodes] = useState(new Set(['user1', 'user2', 'user3']));
  const [selectedUser, setSelectedUser] = useState(null);

  // Calculate all commissions
  const allCommissions = sales.filter(sale => sale.status === 'confirmed')
    .flatMap(sale => calculateCommissions(sale, hierarchy, commissionRules));

  // Aggregate commissions by user
  const userCommissions = allCommissions.reduce((acc, comm) => {
    if (!acc[comm.userId]) {
      acc[comm.userId] = { total: 0, commissions: [] };
    }
    acc[comm.userId].total += comm.amount;
    acc[comm.userId].commissions.push(comm);
    return acc;
  }, {});

  // Format Philippine Peso
  const formatPHP = (amount) => {
    return new Intl.NumberFormat('en-PH', {
      style: 'currency',
      currency: 'PHP',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  // Dashboard Component
  const Dashboard = () => {
    const totalSales = sales.filter(s => s.status === 'confirmed').reduce((sum, sale) => sum + sale.amount, 0);
    const totalCommissions = Object.values(userCommissions).reduce((sum, user) => sum + user.total, 0);
    const activeResellers = Object.values(hierarchy).filter(u => u.active).length;

    // Count by level
    const levelCounts = Object.values(hierarchy).reduce((acc, user) => {
      acc[user.level] = (acc[user.level] || 0) + 1;
      return acc;
    }, {});

    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Sales</p>
                <p className="text-2xl font-bold text-gray-900">{formatPHP(totalSales)}</p>
              </div>
              <DollarSign className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Commissions</p>
                <p className="text-2xl font-bold text-gray-900">{formatPHP(totalCommissions)}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Resellers</p>
                <p className="text-2xl font-bold text-gray-900">{activeResellers}</p>
              </div>
              <Users className="h-8 w-8 text-purple-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Commission Rate</p>
                <p className="text-2xl font-bold text-gray-900">{((totalCommissions / totalSales) * 100).toFixed(1)}%</p>
              </div>
              <Award className="h-8 w-8 text-orange-500" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Level Distribution</h3>
            <div className="space-y-3">
              {[
                { level: 'BD', color: 'bg-red-500', icon: Crown },
                { level: 'IBO', color: 'bg-blue-500', icon: Diamond },
                { level: 'BP', color: 'bg-green-500', icon: Medal }
              ].map(({ level, color, icon: Icon }) => (
                <div key={level} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-8 h-8 ${color} rounded-lg flex items-center justify-center`}>
                      <Icon className="h-4 w-4 text-white" />
                    </div>
                    <span className="font-medium text-gray-900">{level}</span>
                  </div>
                  <span className="text-lg font-bold text-gray-900">{levelCounts[level] || 0}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Earners</h3>
            <div className="space-y-3">
              {Object.entries(userCommissions)
                .sort(([,a], [,b]) => b.total - a.total)
                .slice(0, 5)
                .map(([userId, data]) => {
                  const user = hierarchy[userId];
                  return (
                    <div key={userId} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`w-3 h-3 rounded-full ${
                          user.level === 'BD' ? 'bg-red-500' : 
                          user.level === 'IBO' ? 'bg-blue-500' : 'bg-green-500'
                        }`}></div>
                        <div>
                          <p className="font-medium text-gray-900">{user.name}</p>
                          <p className="text-sm text-gray-500">{user.level}</p>
                        </div>
                      </div>
                      <p className="font-semibold text-gray-900">{formatPHP(data.total)}</p>
                    </div>
                  );
                })}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Sales</h3>
            <div className="space-y-3">
              {sales.slice(0, 5).map(sale => {
                const reseller = hierarchy[sale.resellerId];
                return (
                  <div key={sale.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{reseller?.name}</p>
                      <p className="text-sm text-gray-500">{sale.date} • {sale.type}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">{formatPHP(sale.amount)}</p>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        sale.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {sale.status}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Hierarchy Tree Component
  const HierarchyNode = ({ userId, level = 0 }) => {
    const user = hierarchy[userId];
    const isExpanded = expandedNodes.has(userId);
    const hasChildren = user.children && user.children.length > 0;
    const userEarnings = userCommissions[userId]?.total || 0;

    // Get override tier for IBOs
    const overrideTier = user.level === 'IBO' ? calculateGroupOverrideTier(user, hierarchy) : null;
    
    // Get service fee tier for BDs
    const serviceFee = user.level === 'BD' ? calculateBDServiceFee(user, hierarchy) : null;

    const toggleExpand = () => {
      const newExpanded = new Set(expandedNodes);
      if (isExpanded) {
        newExpanded.delete(userId);
      } else {
        newExpanded.add(userId);
      }
      setExpandedNodes(newExpanded);
    };

    const getLevelColor = (level) => {
      switch(level) {
        case 'BD': return 'bg-red-500 text-white';
        case 'IBO': return 'bg-blue-500 text-white';
        case 'BP': return 'bg-green-500 text-white';
        default: return 'bg-gray-500 text-white';
      }
    };

    const getLevelIcon = (level) => {
      switch(level) {
        case 'BD': return Crown;
        case 'IBO': return Diamond;
        case 'BP': return Medal;
        default: return Users;
      }
    };

    const LevelIcon = getLevelIcon(user.level);

    return (
      <div className="ml-4">
        <div className="flex items-center space-x-3 p-3 bg-white rounded-lg shadow-sm border border-gray-200 mb-2">
          {hasChildren && (
            <button onClick={toggleExpand} className="text-gray-400 hover:text-gray-600">
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          )}
          
          <div className={`px-2 py-1 rounded text-xs font-semibold flex items-center space-x-1 ${getLevelColor(user.level)}`}>
            <LevelIcon size={12} />
            <span>{user.level}</span>
          </div>
          
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <p className="font-medium text-gray-900">{user.name}</p>
              {overrideTier && (
                <span className={`px-2 py-1 text-xs rounded-full ${
                  overrideTier.name === 'Diamond' ? 'bg-purple-100 text-purple-800' :
                  overrideTier.name === 'Gold' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {overrideTier.name}
                </span>
              )}
              {serviceFee && (
                <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
                  {serviceFee.tier}
                </span>
              )}
            </div>
            <p className="text-sm text-gray-500">
              GPPIS: {formatPHP(user.gppis)} | GGPIS: {formatPHP(user.ggpis)}
            </p>
          </div>
          
          <div className="text-right">
            <p className="font-semibold text-green-600">{formatPHP(userEarnings)}</p>
            <p className="text-xs text-gray-500">Earned</p>
          </div>
          
          <button 
            onClick={() => setSelectedUser(user)}
            className="text-blue-500 hover:text-blue-700"
          >
            <Eye size={16} />
          </button>
        </div>
        
        {isExpanded && hasChildren && (
          <div className="ml-4 border-l-2 border-gray-200 pl-4">
            {user.children.map(childId => (
              <HierarchyNode key={childId} userId={childId} level={level + 1} />
            ))}
          </div>
        )}
      </div>
    );
  };

  // Hierarchy Component
  const Hierarchy = () => {
    const rootUsers = Object.values(hierarchy).filter(user => !user.parentId);

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">SUNX MLM Hierarchy</h3>
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center space-x-2">
              <UserPlus size={16} />
              <span>Add Reseller</span>
            </button>
          </div>
          
          <div className="space-y-2">
            {rootUsers.map(user => (
              <HierarchyNode key={user.id} userId={user.id} />
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Commission Rules Component (Updated for SUNX)
  const CommissionRules = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">SUNX Commission Rules Configuration</h3>
          
          {/* Outright Discount Rules by Product */}
          <div className="mb-8">
            <h4 className="font-semibold text-gray-900 mb-4">Outright Discount by Level & Product</h4>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-200 rounded-lg">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left font-semibold text-gray-900">Product</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-900">BP Rate</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-900">IBO Rate</th>
                    <th className="px-4 py-3 text-left font-semibold text-gray-900">BD Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(productDiscountRates).map(([product, rates]) => (
                    <tr key={product} className="border-t border-gray-200">
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          product === 'SUNX-PREMIUM' ? 'bg-purple-100 text-purple-800' :
                          product === 'SUNX-STANDARD' ? 'bg-blue-100 text-blue-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {product}
                        </span>
                      </td>
                      <td className="px-4 py-3 font-medium">{(rates.BP * 100).toFixed(0)}%</td>
                      <td className="px-4 py-3 font-medium">{(rates.IBO * 100).toFixed(0)}%</td>
                      <td className="px-4 py-3 font-medium">{(rates.BD * 100).toFixed(0)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Active Status Thresholds */}
          <div className="mb-8">
            <h4 className="font-semibold text-gray-900 mb-4">Active Status Requirements</h4>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">General Active (BPs)</h5>
                <p className="text-2xl font-bold text-green-600">{formatPHP(2000)}</p>
                <p className="text-sm text-gray-600">GPPIS per month</p>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">BD Calculation Active (IBOs)</h5>
                <p className="text-2xl font-bold text-blue-600">{formatPHP(10000)}</p>
                <p className="text-sm text-gray-600">GPPIS per month</p>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">BD Active Status</h5>
                <p className="text-2xl font-bold text-red-600">{formatPHP(10000)}</p>
                <p className="text-sm text-gray-600">GPPIS per month</p>
              </div>
            </div>
          </div>

          {/* IBO Group Override Rules */}
          <div className="mb-8">
            <h4 className="font-semibold text-gray-900 mb-4">IBO Group Override Tiers</h4>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {Object.entries(commissionRules.IBO.group_override).map(([tier, rules]) => (
                <div key={tier} className="border border-gray-200 rounded-lg p-4">
                  <h5 className="font-semibold text-gray-900 capitalize mb-3">{tier}</h5>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Min Active BPs:</span>
                      <span className="font-medium">{rules.min_active_bps}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Min GGPIS:</span>
                      <span className="font-medium">{formatPHP(rules.min_ggpis)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Override Rate:</span>
                      <span className="font-medium">{(rules.rate * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* BD Service Fee Rules */}
          <div className="mb-8">
            <h4 className="font-semibold text-gray-900 mb-4">BD Group Service Fee Tiers</h4>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {Object.entries(commissionRules.BD.group_service_fee).map(([tier, rules]) => (
                <div key={tier} className="border border-gray-200 rounded-lg p-4">
                  <h5 className="font-semibold text-gray-900 capitalize mb-3">{tier.replace('tier', 'Tier ')}</h5>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Min GGPIS:</span>
                      <span className="font-medium">{formatPHP(rules.min_ggpis)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Service Fee:</span>
                      <span className="font-medium">{(rules.rate * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-600 mt-2">
              * Requires 15+ Active IBOs (≥₱10K GPPIS each) and BD must be Active (≥₱10K GPPIS)
            </p>
          </div>

          {/* Promotion Pathways */}
          <div>
            <h4 className="font-semibold text-gray-900 mb-4">BP to IBO Promotion Pathways</h4>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">Volume-Based</h5>
                <p className="text-sm text-gray-600">
                  Achieve {formatPHP(commissionRules.BP.promotion_threshold)} GPPIS within 2 months
                </p>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">Certificate</h5>
                <p className="text-sm text-gray-600">
                  Present Certificate of Volume from another direct-selling org (≥{formatPHP(50000)})
                </p>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <h5 className="font-semibold text-gray-900 mb-3">Security Bond</h5>
                <p className="text-sm text-gray-600">
                  Post {formatPHP(commissionRules.BP.promotion_bond)} Security Bond for instant IBO status
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Sales Tracking Component
  const SalesTracking = () => {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Sales & Commission Tracking</h3>
            <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center space-x-2">
              <PlusCircle size={16} />
              <span>Record Sale</span>
            </button>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Sale ID</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Reseller</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Amount</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Date</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Type</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Product</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
                  <th className="text-left py-3 px-4 font-semibold text-gray-900">Commission</th>
                </tr>
              </thead>
              <tbody>
                {sales.map(sale => {
                  const reseller = hierarchy[sale.resellerId];
                  const saleCommissions = allCommissions.filter(c => c.saleId === sale.id);
                  const totalCommission = saleCommissions.reduce((sum, c) => sum + c.amount, 0);
                  
                  return (
                    <tr key={sale.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">#{sale.id}</td>
                      <td className="py-3 px-4">
                        <div>
                          <p className="font-medium">{reseller?.name}</p>
                          <p className="text-sm text-gray-500">{reseller?.level}</p>
                        </div>
                      </td>
                      <td className="py-3 px-4 font-semibold">{formatPHP(sale.amount)}</td>
                      <td className="py-3 px-4">{sale.date}</td>
                      <td className="py-3 px-4">{sale.type}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          sale.product === 'SUNX-PREMIUM' ? 'bg-purple-100 text-purple-800' :
                          sale.product === 'SUNX-STANDARD' ? 'bg-blue-100 text-blue-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {sale.product}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          sale.status === 'confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {sale.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-semibold text-green-600">
                        {formatPHP(totalCommission)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  // Reports Component
  const Reports = () => {
    // Get promotion candidates using the eligibility checker
    const promotionCandidates = Object.values(hierarchy)
      .filter(user => user.level === 'BP')
      .map(user => ({
        ...user,
        eligibility: checkPromotionEligibility(user)
      }))
      .filter(user => user.eligibility && user.eligibility.progress > 50); // Show those with >50% progress

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">SUNX Commission Reports & Analytics</h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-4">Commission by Type</h4>
              <div className="space-y-3">
                {[
                  'outright_discount',
                  'group_override', 
                  'lifetime_incentive',
                  'bd_service_fee',
                  'bd_override'
                ].map(type => {
                  const typeCommissions = allCommissions.filter(c => c.type === type);
                  const total = typeCommissions.reduce((sum, c) => sum + c.amount, 0);
                  
                  return (
                    <div key={type} className="flex justify-between items-center">
                      <span className="text-gray-600 capitalize">{type.replace('_', ' ')}</span>
                      <span className="font-semibold">{formatPHP(total)}</span>
                    </div>
                  );
                })}
              </div>
            </div>
            
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-4">BP Promotion Tracking (2-Month Window)</h4>
              <div className="space-y-3">
                {promotionCandidates.map(user => {
                  const elig = user.eligibility;
                  
                  return (
                    <div key={user.id} className="p-2 bg-gray-50 rounded">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium">{user.name}</span>
                        <span className={`text-xs px-2 py-1 rounded ${
                          elig.eligible ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-600'
                        }`}>
                          {elig.eligible ? 'Eligible' : `${elig.progress.toFixed(0)}%`}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        GPPIS: {formatPHP(user.gppis)} / {formatPHP(commissionRules.BP.promotion_threshold)}
                      </div>
                      <div className="text-xs text-gray-500">
                        Month {elig.monthsTracked}/2 • Need: {formatPHP(elig.volumeNeeded)}
                      </div>
                    </div>
                  );
                })}
                {promotionCandidates.length === 0 && (
                  <p className="text-gray-500 text-sm">No active promotion candidates</p>
                )}
              </div>
            </div>
          </div>

          {/* Additional Analytics */}
          <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">IBO Override Qualifications</h4>
              <div className="space-y-2">
                {Object.values(hierarchy)
                  .filter(user => user.level === 'IBO')
                  .map(user => {
                    const tier = calculateGroupOverrideTier(user, hierarchy);
                    const activeBPs = user.children
                      .map(id => hierarchy[id])
                      .filter(child => child && child.level === 'BP' && child.gppis >= 2000)
                      .length;
                    
                    return (
                      <div key={user.id} className="text-sm">
                        <div className="font-medium">{user.name}</div>
                        <div className="text-gray-500">
                          {activeBPs} Active BPs • {tier ? tier.name : 'No Override'}
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">BD Service Fee Status</h4>
              <div className="space-y-2">
                {Object.values(hierarchy)
                  .filter(user => user.level === 'BD')
                  .map(user => {
                    const serviceFee = calculateBDServiceFee(user, hierarchy);
                    
                    // Count total IBOs in downline
                    const countDownlineIBOs = (userId, visited = new Set()) => {
                      if (visited.has(userId)) return 0;
                      visited.add(userId);
                      const u = hierarchy[userId];
                      if (!u) return 0;
                      let count = u.level === 'IBO' && u.gppis >= 10000 ? 1 : 0;
                      u.children.forEach(childId => {
                        count += countDownlineIBOs(childId, visited);
                      });
                      return count;
                    };
                    
                    const activeIBOs = countDownlineIBOs(user.id);
                    
                    return (
                      <div key={user.id} className="text-sm">
                        <div className="font-medium">{user.name}</div>
                        <div className="text-gray-500">
                          {activeIBOs}/15 IBOs • {serviceFee ? serviceFee.tier : 'Not Qualified'}
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Product Performance</h4>
              <div className="space-y-2">
                {Object.keys(productDiscountRates).map(product => {
                  const productSales = sales.filter(s => s.product === product && s.status === 'confirmed');
                  const totalSales = productSales.reduce((sum, s) => sum + s.amount, 0);
                  
                  return (
                    <div key={product} className="text-sm">
                      <div className="font-medium">{product}</div>
                      <div className="text-gray-500">
                        {productSales.length} sales • {formatPHP(totalSales)}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // User Detail Modal
  const UserDetailModal = () => {
    if (!selectedUser) return null;
    
    const userEarnings = userCommissions[selectedUser.id];
    const downlineUsers = selectedUser.children?.map(id => hierarchy[id]) || [];
    const overrideTier = selectedUser.level === 'IBO' ? calculateGroupOverrideTier(selectedUser, hierarchy) : null;
    const serviceFee = selectedUser.level === 'BD' ? calculateBDServiceFee(selectedUser, hierarchy) : null;
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-6 max-w-2xl w-full mx-4 max-h-screen overflow-y-auto">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-gray-900">{selectedUser.name} - Details</h3>
            <button 
              onClick={() => setSelectedUser(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <p className="text-sm text-gray-600">Level</p>
              <p className="font-semibold">{selectedUser.level}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <p className="font-semibold text-green-600">{selectedUser.active ? 'Active' : 'Inactive'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">GPPIS</p>
              <p className="font-semibold">{formatPHP(selectedUser.gppis)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">GGPIS</p>
              <p className="font-semibold">{formatPHP(selectedUser.ggpis)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Join Date</p>
              <p className="font-semibold">{selectedUser.joinDate}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Earnings</p>
              <p className="font-semibold text-green-600">{formatPHP(userEarnings?.total || 0)}</p>
            </div>
          </div>

          {/* Special Qualifications */}
          {(overrideTier || serviceFee) && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold mb-2">Special Qualifications</h4>
              {overrideTier && (
                <p className="text-sm text-blue-700">
                  Group Override: {overrideTier.name} ({(overrideTier.rate * 100).toFixed(0)}%)
                </p>
              )}
              {serviceFee && (
                <p className="text-sm text-blue-700">
                  BD Service Fee: {serviceFee.tier} ({(serviceFee.rate * 100).toFixed(0)}%)
                </p>
              )}
            </div>
          )}
          
          {downlineUsers.length > 0 && (
            <div>
              <h4 className="font-semibold mb-3">Direct Downline ({downlineUsers.length})</h4>
              <div className="space-y-2">
                {downlineUsers.map(user => (
                  <div key={user.id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                    <div>
                      <span className="font-medium">{user.name}</span>
                      <span className="text-sm text-gray-600 ml-2">({user.level})</span>
                    </div>
                    <span className="text-sm text-gray-600">{formatPHP(user.gppis)} GPPIS</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Commission Breakdown */}
          {userEarnings && (
            <div className="mt-6 p-4 bg-green-50 rounded-lg">
              <h4 className="font-semibold mb-2">Commission Breakdown</h4>
              <div className="space-y-1">
                {userEarnings.commissions.map((comm, index) => (
                  <div key={index} className="flex justify-between text-sm">
                    <span className="text-green-700 capitalize">
                      {comm.type.replace('_', ' ')} 
                      {comm.tier && ` (${comm.tier})`}
                      {comm.source && ` from ${comm.source}`}
                    </span>
                    <span className="font-medium">{formatPHP(comm.amount)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'hierarchy', label: 'Hierarchy', icon: Users },
    { id: 'rules', label: 'Commission Rules', icon: Settings },
    { id: 'sales', label: 'Sales Tracking', icon: DollarSign },
    { id: 'reports', label: 'Reports', icon: TrendingUp }
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="bg-orange-600 p-2 rounded-lg">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">SUNX MLM Commission System</h1>
                <p className="text-sm text-gray-500">Multi-Level Marketing Commission Management (Philippines)</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-5 w-5 text-gray-400" />
              <span className="text-sm text-gray-600">July 2025</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex space-x-8">
          {/* Sidebar Navigation */}
          <div className="w-64 flex-shrink-0">
            <nav className="space-y-2">
              {tabs.map(tab => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                      activeTab === tab.id
                        ? 'bg-orange-100 text-orange-700 border-orange-200'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon size={20} />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {activeTab === 'dashboard' && <Dashboard />}
            {activeTab === 'hierarchy' && <Hierarchy />}
            {activeTab === 'rules' && <CommissionRules />}
            {activeTab === 'sales' && <SalesTracking />}
            {activeTab === 'reports' && <Reports />}
          </div>
        </div>
      </div>

      {/* User Detail Modal */}
      <UserDetailModal />
    </div>
  );
};

export default MLMCommissionApp;