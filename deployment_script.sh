#!/bin/bash

# SUNX MLM Prototype - Quick Deployment Script
# This script sets up the complete project structure for client demonstration

echo "🚀 Setting up SUNX MLM Commission Engine Prototype..."
echo "=================================================="

# Create project directory
PROJECT_NAME="sunx-mlm-prototype"
echo "📁 Creating project directory: $PROJECT_NAME"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Initialize Git repository
echo "🔧 Initializing Git repository..."
git init
echo "node_modules/" > .gitignore
echo ".DS_Store" >> .gitignore
echo "*.log" >> .gitignore
echo ".env" >> .gitignore

# Create package.json
echo "📦 Creating package.json..."
cat > package.json << 'EOF'
{
  "name": "sunx-mlm-prototype",
  "version": "1.0.0",
  "description": "SUNX MLM Commission Engine - Client Demonstration Prototype",
  "main": "index.html",
  "scripts": {
    "start": "npx http-server . -p 3000 -o",
    "dev": "npx live-server --port=3000 --open=/index.html",
    "build": "echo 'Static build complete - ready for deployment'",
    "deploy": "gh-pages -d .",
    "demo": "echo 'Starting demo server...' && npm run start"
  },
  "keywords": ["MLM", "commission", "odoo", "erp", "sunx", "philippines"],
  "author": "Your Company Name",
  "license": "MIT",
  "devDependencies": {
    "http-server": "^14.1.1",
    "live-server": "^1.2.2",
    "gh-pages": "^4.0.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/sunx-mlm-prototype.git"
  }
}
EOF

# Create README.md
echo "📝 Creating documentation..."
cat > README.md << 'EOF'
# SUNX MLM Commission Engine - Client Demo

## 🎯 Quick Start
```bash
npm run demo
```
Then open: http://localhost:3000

## 🏢 What This Demonstrates
✅ Complete MLM hierarchy with 10 realistic resellers  
✅ Real-time commission calculations (6 types)  
✅ Interactive sales editing with live updates  
✅ Odoo ERP integration architecture  
✅ Philippine peso formatting and business rules  
✅ Professional client-ready interface  

## 🔧 Technical Features
- **GPPIS/GGPIS calculations** with downline aggregation
- **Group Override tiers** (Silver/Gold/Diamond)
- **BD Service Fee** with 15+ IBO requirement
- **Lifetime Incentive** for IBO downlines
- **Promotion tracking** with 2-month windows
- **Data persistence** across demo sessions

## 📊 Demo Script
1. **Overview**: Show dashboard statistics
2. **Hierarchy**: Navigate visual organization
3. **Real-time**: Edit sales figures and watch updates
4. **Details**: Click users for commission breakdowns
5. **Integration**: Highlight Odoo ERP concepts

## 🚀 Odoo Integration Ready
- Resellers as **hr.employee** records
- Organizations as **res.partner** companies  
- Sales from **sale.order** and **pos.order**
- Custom **mlm.commission** models
- Real-time calculation triggers

Built to prove we understand SUNX requirements completely.
EOF

# Create demo data documentation
echo "📋 Creating commission rules documentation..."
mkdir -p docs
cat > docs/commission-rules.md << 'EOF'
# SUNX MLM Commission Rules - Implementation

## Outright Discount by Product
| Product | BP | IBO | BD |
|---------|----|----|-----|
| SUNX-PREMIUM | 25% | 40% | 40% |
| SUNX-STANDARD | 20% | 35% | 35% |
| SUNX-BASIC | 15% | 28% | 28% |

## Group Override (IBO Only)
- **Silver**: 3+ Active BPs, ≥₱50K GGPIS → 5%
- **Gold**: 5+ Active BPs, ≥₱100K GGPIS → 6%  
- **Diamond**: 8+ Active BPs, ≥₱180K GGPIS → 8%

## BD Service Fee
- **Tier 1**: ≥₱1M GGPIS → 5%
- **Tier 2**: ≥₱2.5M GGPIS → 6%
- **Tier 3**: ≥₱4M GGPIS → 7%
- Requires: 15+ Active IBOs (≥₱10K GPPIS each)

## Lifetime Incentive
- 2% of 1st-level IBO downlines' GPPIS
- Both upline and downline must have ≥₱10K GPPIS

## Active Status Thresholds
- **BP**: ≥₱2K GPPIS/month
- **IBO**: ≥₱2K GPPIS/month (basic), ≥₱10K for BD calculations
- **BD**: ≥₱10K GPPIS/month

## Promotion: BP → IBO
1. **Volume**: ₱50K GPPIS in 2 consecutive months
2. **Certificate**: CV from other org ≥₱50K
3. **Bond**: ₱25K security bond (instant)
EOF

# Create the main HTML file (this would be copied from the artifact)
echo "🎨 Creating main prototype file..."
echo "<!-- Copy the HTML content from the artifact here -->" > index.html
echo "⚠️  IMPORTANT: Copy the complete HTML prototype from the Claude artifact into index.html"

# Create deployment instructions
cat > DEPLOYMENT.md << 'EOF'
# 🚀 Deployment Instructions

## Local Development
```bash
# Install dependencies (optional)
npm install

# Start demo server
npm run demo
# Opens automatically at http://localhost:3000
```

## GitHub Setup
```bash
# Set your GitHub repository
git remote add origin https://github.com/YOURUSERNAME/sunx-mlm-prototype.git

# Initial commit
git add .
git commit -m "feat: Complete SUNX MLM prototype for client demo"
git push -u origin main
```

## GitHub Pages Deployment
```bash
# Deploy to GitHub Pages
npm run deploy
# Accessible at https://YOURUSERNAME.github.io/sunx-mlm-prototype
```

## VSCode Integration
1. Open project in VSCode: `code .`
2. Install Live Server extension
3. Right-click index.html → "Open with Live Server"
4. Use Source Control panel for Git operations

## Client Demo Checklist
- [ ] Test all interactive features
- [ ] Verify commission calculations
- [ ] Check data persistence
- [ ] Prepare talking points
- [ ] Have backup plan (screenshots)

## Production Deployment
For actual Odoo integration:
1. Review `docs/odoo-integration-specs.md`
2. Implement custom Odoo modules
3. Set up staging environment
4. Migrate demo data structure
5. Configure API endpoints
EOF

# Create a simple launcher script
cat > launch-demo.sh << 'EOF'
#!/bin/bash
echo "🚀 Launching SUNX MLM Demo..."
echo "Opening http://localhost:3000"
echo "Press Ctrl+C to stop the server"
npm run start
EOF
chmod +x launch-demo.sh

# Create Windows batch file
cat > launch-demo.bat << 'EOF'
@echo off
echo 🚀 Launching SUNX MLM Demo...
echo Opening http://localhost:3000
echo Press Ctrl+C to stop the server
npm run start
pause
EOF

echo ""
echo "✅ Project setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Copy the HTML prototype content into index.html"
echo "2. Run: npm run demo"
echo "3. Open http://localhost:3000"
echo "4. Test all interactive features"
echo "5. Set up GitHub repository"
echo ""
echo "🎯 Client Demo Ready!"
echo "Your professional MLM prototype is ready for client presentation."
echo ""
echo "💡 Pro Tips:"
echo "- Edit sales figures to show real-time calculations"
echo "- Use month selector to show different periods"
echo "- Click user details to show commission breakdowns"
echo "- Highlight Odoo integration concepts"
echo ""
echo "🚀 Success! SUNX will be impressed with your technical depth."

# Make the script executable
chmod +x "$0"