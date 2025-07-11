# main.py - SUNX MLM Commission Engine
# Main application entry point

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from flask import Flask, render_template, request, jsonify
from database.models import db, init_db
from database.sample_data import create_sample_data
from services.commission_engine import CommissionEngine
from services.hierarchy_service import HierarchyService
from config import Config
import webbrowser
import threading
import time

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Services
    commission_engine = CommissionEngine()
    hierarchy_service = HierarchyService()
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return render_template('index.html')
    
    @app.route('/api/hierarchy')
    def get_hierarchy():
        """Get complete hierarchy data"""
        try:
            hierarchy_data = hierarchy_service.get_complete_hierarchy()
            return jsonify({
                'success': True,
                'data': hierarchy_data
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/reseller/<int:reseller_id>')
    def get_reseller_details(reseller_id):
        """Get detailed reseller information"""
        try:
            details = hierarchy_service.get_reseller_details(reseller_id)
            return jsonify({
                'success': True,
                'data': details
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/commissions/<int:reseller_id>/<string:month>')
    def get_commissions(reseller_id, month):
        """Get commission calculations for reseller and month"""
        try:
            commissions = commission_engine.calculate_monthly_commissions(reseller_id, month)
            return jsonify({
                'success': True,
                'data': commissions
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/sales/update', methods=['POST'])
    def update_sales():
        """Update monthly sales for a reseller"""
        try:
            data = request.get_json()
            reseller_id = data.get('reseller_id')
            month = data.get('month')
            amount = data.get('amount')
            
            success = hierarchy_service.update_monthly_sales(reseller_id, month, amount)
            
            if success:
                # Recalculate commissions
                updated_commissions = commission_engine.calculate_monthly_commissions(reseller_id, month)
                return jsonify({
                    'success': True,
                    'data': updated_commissions,
                    'message': 'Sales updated successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update sales'
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/dashboard/stats/<string:month>')
    def get_dashboard_stats(month):
        """Get dashboard statistics for a specific month"""
        try:
            stats = hierarchy_service.get_dashboard_stats(month)
            return jsonify({
                'success': True,
                'data': stats
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/promotion/candidates/<string:month>')
    def get_promotion_candidates(month):
        """Get BP promotion candidates for a specific month"""
        try:
            candidates = commission_engine.get_promotion_candidates(month)
            return jsonify({
                'success': True,
                'data': candidates
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return app

def open_browser():
    """Open the application in the default web browser"""
    time.sleep(1.5)  # Wait for Flask to start
    webbrowser.open('http://localhost:5000')

def main():
    """Main application entry point"""
    print("🚀 Starting SUNX MLM Commission Engine...")
    print("=" * 50)
    
    # Create Flask app
    app = create_app()
    
    # Initialize database and create sample data
    with app.app_context():
        print("📊 Initializing database...")
        init_db()
        print("🏢 Creating sample data...")
        create_sample_data()
        print("✅ Database setup complete!")
    
    print("\n🌐 Starting web server...")
    print("📱 Application will open in your browser at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask development server
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 SUNX MLM Commission Engine stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()