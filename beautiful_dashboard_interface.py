"""
Beautiful Dashboard Interface with Enhanced AI Integration
Complete production-ready system with stunning visuals
"""

from flask import Flask, render_template_string, request, jsonify
import threading
import time
import logging
from datetime import datetime
import json
import os
import sys

# Import your existing components
# Uncomment these when integrating with your actual system
# from enhanced_human_ai_assistant import EnhancedHumanAIAssistant
# from robust_dgr_excel_reader import RobustDGRExcelReader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'beautiful_dgr_dashboard_2024'

# Global system state
excel_reader = None
enhanced_ai = None
system_status = {
    'initialized': False,
    'plants_loaded': 0,
    'last_update': None,
    'error_message': None,
    'initialization_time': None,
    'ai_ready': False
}

# Dashboard data cache
dashboard_data = {
    'portfolio_metrics': {},
    'plant_summaries': [],
    'system_alerts': [],
    'last_updated': None,
    'data_quality': {}
}

def initialize_beautiful_system():
    """Initialize the complete beautiful KPI system"""
    global excel_reader, enhanced_ai, system_status
    
    try:
        logger.info("🎨 Initializing Beautiful DGR KPI System...")
        start_time = datetime.now()
        
        # Initialize Excel Reader
        logger.info("📊 Creating Excel Reader...")
        # Uncomment when integrating:
        # excel_reader = RobustDGRExcelReader("Files")
        # data = excel_reader.load_all_data()
        
        # For demo purposes, using sample data
        data = create_sample_data()
        
        if not data:
            raise Exception("No data could be loaded from Excel files")
        
        # Initialize Enhanced AI Assistant
        logger.info("🤖 Creating Enhanced AI Assistant...")
        # Uncomment when integrating:
        # enhanced_ai = EnhancedHumanAIAssistant(excel_reader)
        
        # For demo purposes, create mock AI
        enhanced_ai = MockEnhancedAI()
        
        # Update system status
        system_status.update({
            'initialized': True,
            'plants_loaded': len(data),
            'last_update': datetime.now(),
            'error_message': None,
            'initialization_time': (datetime.now() - start_time).total_seconds(),
            'ai_ready': True
        })
        
        logger.info(f"✅ Beautiful system initialized successfully!")
        logger.info(f"🏭 Loaded {len(data)} plants in {system_status['initialization_time']:.1f}s")
        
        # Generate initial dashboard data
        update_beautiful_dashboard_data()
        
        return True
        
    except Exception as e:
        error_msg = f"Beautiful system initialization failed: {str(e)}"
        logger.error(f"❌ {error_msg}")
        system_status.update({
            'initialized': False,
            'error_message': error_msg,
            'last_update': datetime.now(),
            'ai_ready': False
        })
        return False

def create_sample_data():
    """Create sample data for demo purposes"""
    return {
        '7MW': {'daily_kpi': True},
        '8MW': {'daily_kpi': True},
        'NTPC': {'daily_kpi': True},
        'ESP': {'daily_kpi': True},
        'ESS': {'daily_kpi': True},
        'AXPPL': {'daily_kpi': True},
        'JPPL_50MW': {'daily_kpi': True},
        'JPPL_70MW': {'daily_kpi': True},
        'Ghatodi': {'daily_kpi': True},
        'CEPPL_Solar': {'daily_kpi': True},
        'CEPPL_Wind': {'daily_kpi': True},
        'CSPPL': {'daily_kpi': True},
        'ESE': {'daily_kpi': True},
        'Motala_Solar': {'daily_kpi': True},
        'PSEGPL': {'daily_kpi': True},
        'PWEGPL': {'daily_kpi': True},
        'PWEPL': {'daily_kpi': True},
        'TQGPXIIPL': {'daily_kpi': True}
    }

class MockEnhancedAI:
    """Mock AI assistant for demo purposes"""
    
    def process_query(self, user_input: str) -> str:
        query = user_input.lower().strip()
        
        if 'help' in query:
            return """🤖 **Beautiful DGR AI Assistant Help**

**🚀 What I Can Do:**
• **Real-time Analysis**: "What's the status of all plants today?"
• **Performance Comparisons**: "Compare 7MW vs NTPC this week"
• **Diagnostic Support**: "Why is ESP underperforming?"
• **Financial Insights**: "Show me revenue analysis for this month"
• **Historical Data**: "What was performance on June 12th?" (with data availability checking)

**💡 Smart Features:**
• I learn from our conversations and remember context
• I adapt responses based on your role (Operations/Technical/Executive)
• I handle missing data gracefully and explain what's available
• I provide follow-up suggestions based on your interests

**⌨️ Keyboard Shortcuts:**
• Ctrl + / : Show this help
• Ctrl + Enter : Quick portfolio summary

**🎯 Sample Queries to Try:**
• "portfolio summary"
• "any plants down today?"
• "compare 7MW vs 8MW performance"
• "financial performance this month"
• "what was performance on June 12th?"

Just ask me naturally - I understand workplace language! 🚀"""

        elif 'portfolio' in query or 'summary' in query:
            return """📊 **Executive Portfolio Summary**

**🏭 Portfolio Overview (Last 30 Days):**
• **Total Energy Export**: 2,847,591 kWh
• **Portfolio Availability**: 94.2% (Above 95% target ⚠️)
• **Performance Ratio**: 87.8% (Good performance ✅)
• **Operational Status**: 16/18 plants online (89% operational rate)

**🏆 Top Performers:**
1. **7MW Plant**: 245,679 kWh (96.8% availability)
2. **JPPL_70MW**: 198,456 kWh (95.2% availability)
3. **AXPPL**: 187,321 kWh (94.7% availability)

**⚠️ Attention Required:**
• **ESP Plant**: Low availability (87.3%) - maintenance recommended
• **NTPC**: Below availability target (92.1%) - monitor closely
• **Ghatodi**: Data quality issues (89.1% complete)

**💰 Financial Impact:**
• **Estimated Revenue**: ₹99,66,569 (@ ₹3.50/kWh avg)
• **Daily Average**: ₹3,32,219
• **Monthly Target**: 95% achieved ✅

**💡 Executive Insight**: Portfolio performing well with strong energy output. Focus on ESP plant optimization could improve overall metrics by 2-3%.

**🔮 You might also ask:**
• "Why is ESP plant underperforming?"
• "Compare this month vs last month"
• "Maintenance recommendations"
• "ROI analysis by plant"
"""

        elif 'june 12' in query or 'june' in query:
            return """📅 **Data Availability Notice**

I see you're asking about June 12th data. Here's what I can tell you:

**📊 Data Status:**
• **Latest Available Data**: June 12, 2024 ✅
• **Requested Date**: June 12, 2024 ✅
• **Data Completeness**: 98.5% complete

**🏭 Performance Summary for June 12, 2024:**
• **Total Energy Export**: 94,567 kWh
• **Portfolio Availability**: 95.3%
• **Performance Ratio**: 88.1%
• **Operational Plants**: 17/18

**📈 Top Performers on June 12:**
1. **7MW**: 8,234 kWh (97.2% availability)
2. **NTPC**: 7,891 kWh (96.8% availability)  
3. **JPPL_70MW**: 7,456 kWh (95.4% availability)

**⚠️ Issues on June 12:**
• **ESP Plant**: Offline for maintenance (0% availability)
• **Minor grid curtailment**: 14:30-15:15 (affected 3 plants)

**💡 Context**: June 12th was a good solar day with high irradiation levels. The ESP maintenance was planned and didn't significantly impact portfolio performance.

**🔮 You might also ask:**
• "Compare June 12 vs June 11"
• "Why was ESP offline on June 12?"
• "Weather impact on June 12 performance"
"""

        elif 'today' in query or 'current' in query or 'now' in query:
            return """📅 **Current Data Status**

**⏰ Data Availability Notice:**
I don't have real-time data for today (June 17, 2024) yet. My latest data is from **June 12, 2024** (5 days ago).

**📊 Latest Available Performance (June 12, 2024):**
• **Total Energy Export**: 94,567 kWh
• **Portfolio Availability**: 95.3%
• **Performance Ratio**: 88.1%
• **Operational Plants**: 17/18 online

**🔄 What I Can Show You Instead:**
• **Latest available performance** (June 12th)
• **Weekly trends** leading up to June 12th
• **Performance patterns** for this time of year
• **Maintenance schedules** and planned activities

**📈 Recent Trend (June 6-12):**
• **Average Daily Energy**: 92,340 kWh
• **Availability Trend**: Stable around 94-96%
• **Performance Trend**: Consistent 87-89%

**💡 Recommendation**: For real-time monitoring, please check your SCADA system or contact the control room for live plant status.

**🔮 You might also ask:**
• "Show me performance for June 12th"
• "Weekly trends ending June 12"
• "Which plants typically perform best at this time?"
"""

        elif 'compare' in query:
            return """⚖️ **Plant Performance Comparison**

**📊 Comparative Analysis (Last 30 Days - May 13 to June 12):**

| Rank | Plant | Type | Energy (kWh) | Availability | Performance | Score |
|------|-------|------|--------------|--------------|-------------|-------|
| 1 | **7MW** | Solar | 245,679 | 96.8% | 89.2% | 93.0 |
| 2 | **JPPL_70MW** | Solar | 198,456 | 95.2% | 88.7% | 91.9 |
| 3 | **AXPPL** | Solar | 187,321 | 94.7% | 87.8% | 91.2 |
| 4 | **NTPC** | Solar | 165,432 | 92.1% | 86.5% | 89.3 |
| 5 | **CEPPL_Wind** | Wind | 156,789 | 91.8% | 85.9% | 88.8 |
| 6 | **ESP** | Solar | 142,567 | 87.3% | 84.2% | 85.7 |

**🏆 Key Insights:**
• **Best Overall**: 7MW Plant (Score: 93.0) - Excellent across all metrics
• **Highest Energy**: 7MW Plant (245,679 kWh) - 25% above average
• **Best Availability**: 7MW Plant (96.8%) - Industry-leading uptime
• **Most Improved**: AXPPL (+3.2% vs previous month)

**📈 Technology Comparison:**
• **Solar Average**: 91.2% availability, 87.1% performance
• **Wind Average**: 89.5% availability, 84.8% performance
• **Solar** outperforming **Wind** by 2.3% overall

**⚠️ Focus Areas:**
• **ESP Plant**: Needs maintenance attention (87.3% availability)
• **CEPPL_Wind**: Below wind industry average
• **Data Quality**: 3 plants below 95% data completeness

**💡 Strategic Recommendation**: 7MW plant operational practices should be replicated across portfolio. ESP plant requires immediate intervention.

**🔮 You might also ask:**
• "Why is 7MW performing so well?"
• "ESP plant diagnostic analysis"
• "Best practices from top performers"
"""

        elif any(word in query for word in ['why', 'problem', 'issue', 'down', 'low']):
            return """🔧 **Diagnostic Analysis**

**🎯 Performance Issue Analysis:**

Based on your query, I'm analyzing potential performance issues across the portfolio.

**⚠️ Current Issues Identified:**

**1. ESP Plant - Critical**
• **Issue**: Low availability (87.3% vs 95% target)
• **Impact**: 15,000 kWh daily energy loss
• **Root Cause**: Recurring inverter faults + scheduled maintenance
• **Action**: Immediate inverter replacement recommended

**2. NTPC Plant - Warning**
• **Issue**: Availability below target (92.1% vs 95%)
• **Impact**: 8,000 kWh daily energy loss
• **Root Cause**: Grid connectivity issues during peak hours
• **Action**: Coordinate with grid operator for stability improvement

**3. Data Quality Issues**
• **Issue**: 3 plants with <95% data completeness
• **Impact**: Reduced monitoring effectiveness
• **Root Cause**: Communication system intermittency
• **Action**: Upgrade SCADA communication infrastructure

**📊 Performance Impact:**
• **Daily Revenue Loss**: ₹80,500 (₹3.50/kWh)
• **Monthly Impact**: ₹24,15,000
• **Availability Gap**: 2.8% below industry benchmark

**🔧 Immediate Actions Required:**
1. **ESP Plant**: Schedule emergency maintenance this weekend
2. **NTPC**: Grid stability meeting with state utility
3. **All Plants**: SCADA system health check
4. **Monitoring**: Implement real-time alert system

**💡 Technical Insight**: Most issues are related to aging infrastructure and grid stability. A ₹50 lakh investment in modern inverters and communication systems could recover ₹2.4 crores annually.

**🔮 You might also ask:**
• "ESP plant maintenance schedule"
• "Grid issues affecting NTPC"
• "Investment plan for infrastructure upgrade"
"""

        elif 'financial' in query or 'revenue' in query or 'money' in query:
            return """💰 **Financial Performance Analysis**

**📈 Revenue Summary (Last 30 Days):**
• **Total Energy Sold**: 2,847,591 kWh
• **Estimated Revenue**: ₹99,66,569
• **Average Tariff**: ₹3.50 per kWh
• **Daily Average Revenue**: ₹3,32,219

**🏭 Plant-wise Financial Performance:**

| Plant | Energy (kWh) | Revenue (₹) | Tariff (₹/kWh) | PLF (%) |
|-------|--------------|-------------|----------------|---------|
| **7MW** | 245,679 | ₹8,59,877 | 3.50 | 24.5% |
| **JPPL_70MW** | 198,456 | ₹6,94,596 | 3.50 | 19.8% |
| **AXPPL** | 187,321 | ₹6,55,624 | 3.50 | 18.7% |
| **NTPC** | 165,432 | ₹5,79,012 | 3.50 | 16.5% |
| **CEPPL_Wind** | 156,789 | ₹5,51,762 | 3.52 | 15.7% |

**💼 Key Financial Metrics:**
• **Revenue per MW**: ₹5,53,698 per MW per month
• **Capacity Utilization**: 89% across portfolio
• **Energy Yield**: 1,424 kWh per kW per month
• **O&M Cost Ratio**: 2.1% of revenue (industry avg: 2.5%)

**📊 Performance vs Budget:**
• **Energy Target**: 95% achieved ✅
• **Revenue Target**: 97% achieved ✅
• **PLF Target**: 92% achieved ⚠️
• **Availability Target**: 89% achieved ⚠️

**💰 Revenue Optimization Opportunities:**
• **ESP Plant Recovery**: +₹5,25,000/month (if availability improved to 95%)
• **Grid Curtailment Reduction**: +₹2,80,000/month
• **Performance Optimization**: +₹1,90,000/month

**🎯 Financial Recommendations:**
1. **Immediate**: Focus on ESP plant recovery (₹5.25L monthly impact)
2. **Short-term**: Negotiate grid stability improvements
3. **Long-term**: Technology upgrade for 3-5% performance improvement

**📈 ROI Analysis:**
• **Current Portfolio LCOE**: ₹2.85 per kWh
• **Profit Margin**: 18.6% (₹0.65 per kWh)
• **Payback Period**: Original 8.2 years (6.1 years remaining)

**🔮 You might also ask:**
• "ROI analysis for individual plants"
• "Energy banking and drawl strategy"
• "Tariff renegotiation opportunities"
"""

        else:
            return f"""🤖 **AI Assistant Response**

I understand you're asking about: "{user_input}"

**🔍 Current Analysis:**
I'm analyzing your DGR plant data to provide the most accurate response. Based on your query, I can help with performance data, availability metrics, and operational insights across your renewable energy portfolio.

**📊 Quick Portfolio Status:**
• **Active Plants**: 18 DGR facilities
• **Data Available**: Up to June 12, 2024
• **System Status**: All monitoring systems operational

**💡 To get more specific help, try asking:**
• **"portfolio summary"** - Complete performance overview
• **"any plants down today?"** - Current operational status
• **"compare 7MW vs NTPC"** - Plant performance comparison
• **"financial performance"** - Revenue and ROI analysis
• **"help"** - Complete list of capabilities

**📅 Data Availability Note:**
My latest data is from June 12, 2024. For queries about recent dates, I'll explain what information is available and offer alternatives.

**🎯 Popular Workplace Queries:**
• Executive: "Show me board meeting summary"
• Operations: "Which plants need attention today?"
• Technical: "Why is performance ratio low?"
• Financial: "What's our monthly revenue?"

How can I help you dive deeper into your specific analysis needs? 🚀"""

def update_beautiful_dashboard_data():
    """Update dashboard data with beautiful formatting"""
    global dashboard_data
    
    if not system_status['initialized']:
        return
    
    try:
        logger.info("🎨 Updating beautiful dashboard data...")
        
        # Sample data for demo - replace with actual data integration
        dashboard_data.update({
            'portfolio_metrics': {
                'total_energy': 2847591,
                'avg_availability': 94.2,
                'avg_performance': 87.8,
                'operational_plants': 16,
                'total_plants': 18,
                'revenue_estimate': 9966569,
                'daily_average': 94920
            },
            'plant_summaries': [
                {
                    'name': '7MW',
                    'status': 'operational',
                    'energy': 245679,
                    'availability': 96.8,
                    'performance': 89.2,
                    'data_quality': 98.5,
                    'trend': 'up',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'JPPL_70MW',
                    'status': 'operational',
                    'energy': 198456,
                    'availability': 95.2,
                    'performance': 88.7,
                    'data_quality': 97.1,
                    'trend': 'stable',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'AXPPL',
                    'status': 'operational',
                    'energy': 187321,
                    'availability': 94.7,
                    'performance': 87.8,
                    'data_quality': 96.3,
                    'trend': 'up',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'NTPC',
                    'status': 'warning',
                    'energy': 165432,
                    'availability': 92.1,
                    'performance': 86.5,
                    'data_quality': 95.8,
                    'trend': 'down',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'CEPPL_Wind',
                    'status': 'operational',
                    'energy': 156789,
                    'availability': 91.8,
                    'performance': 85.9,
                    'data_quality': 94.2,
                    'trend': 'stable',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'ESP',
                    'status': 'critical',
                    'energy': 142567,
                    'availability': 87.3,
                    'performance': 84.2,
                    'data_quality': 93.1,
                    'trend': 'down',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'ESS',
                    'status': 'operational',
                    'energy': 134892,
                    'availability': 93.4,
                    'performance': 86.7,
                    'data_quality': 95.9,
                    'trend': 'stable',
                    'last_update': '2024-06-12'
                },
                {
                    'name': 'Ghatodi',
                    'status': 'warning',
                    'energy': 128456,
                    'availability': 89.7,
                    'performance': 83.2,
                    'data_quality': 89.1,
                    'trend': 'down',
                    'last_update': '2024-06-12'
                }
            ],
            'system_alerts': [
                '🚨 ESP: Critical availability (87.3%) - Immediate maintenance required',
                '⚠️ NTPC: Below availability target (92.1%) - Grid issues suspected',
                '📊 Ghatodi: Poor data quality (89.1% complete) - Communication issues',
                '⚡ CEPPL_Wind: Performance below wind benchmark (85.9%)',
                'ℹ️ 7MW: Excellent performance - Use as benchmark for other plants',
                '🔧 Portfolio: 2 plants need immediate attention',
                '📈 Revenue: 97% of monthly target achieved'
            ],
            'data_quality': {
                'overall_completeness': 94.8,
                'real_time_connectivity': 89,
                'data_freshness': 'June 12, 2024',
                'monitoring_health': 'Good'
            },
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        logger.info("✅ Beautiful dashboard data updated successfully")
        
    except Exception as e:
        logger.error(f"❌ Error updating beautiful dashboard data: {str(e)}")

def background_beautiful_updater():
    """Background thread for beautiful dashboard updates"""
    while True:
        if system_status['initialized']:
            try:
                update_beautiful_dashboard_data()
                time.sleep(300)  # Update every 5 minutes
            except Exception as e:
                logger.error(f"Beautiful background update error: {str(e)}")
                time.sleep(60)  # Retry in 1 minute
        else:
            time.sleep(10)  # Wait for initialization

# Beautiful HTML Template with Complete CSS
BEAUTIFUL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DGR KPI Intelligence Dashboard</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            --danger-gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-primary: #2c3e50;
            --text-secondary: #7f8c8d;
            --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.37);
            --shadow-hover: 0 12px 40px rgba(31, 38, 135, 0.5);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--primary-gradient);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }

        /* Animated Background Particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
            50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
        }

        /* Main Dashboard Container */
        .dashboard {
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Section */
        .header {
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-soft);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .header h1 {
            font-size: 2.8em;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--success-gradient);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: 600;
            margin-left: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .status-indicator.error {
            background: var(--danger-gradient);
        }

        .status-indicator i {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1em;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            box-shadow: var(--shadow-soft);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--success-gradient);
            border-radius: 20px 20px 0 0;
        }

        .metric-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--success-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            color: white;
            font-size: 1.5em;
        }

        .metric-title {
            font-size: 1em;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 15px;
            font-weight: 500;
        }

        .metric-value {
            font-size: 2.5em;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        .metric-unit {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
            font-weight: 500;
        }

        .metric-trend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            color: white;
        }

        .trend-up { color: #4CAF50; }
        .trend-down { color: #F44336; }

        /* Main Content Layout */
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }

        .content-section {
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            box-shadow: var(--shadow-soft);
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }

        .section-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--success-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .section-title {
            font-size: 1.4em;
            font-weight: 600;
            color: white;
        }

        /* Plant Performance Cards */
        .plant-grid {
            display: grid;
            gap: 15px;
        }

        .plant-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }

        .plant-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }

        .plant-status-indicator {
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            border-radius: 15px 0 0 15px;
        }

        .plant-card.operational .plant-status-indicator { background: #4CAF50; }
        .plant-card.warning .plant-status-indicator { background: #FF9800; }
        .plant-card.critical .plant-status-indicator { background: #F44336; }
        .plant-card.no_data .plant-status-indicator { background: #9E9E9E; }

        .plant-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .plant-name {
            font-size: 1.1em;
            font-weight: 600;
            color: white;
        }

        .plant-status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }

        .plant-status-badge.operational { background: rgba(76, 175, 80, 0.2); color: #4CAF50; }
        .plant-status-badge.warning { background: rgba(255, 152, 0, 0.2); color: #FF9800; }
        .plant-status-badge.critical { background: rgba(244, 67, 54, 0.2); color: #F44336; }

        .plant-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            font-size: 0.9em;
        }

        .plant-metric {
            text-align: center;
        }

        .plant-metric-value {
            font-size: 1.2em;
            font-weight: 600;
            color: white;
            margin-bottom: 5px;
        }

        .plant-metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.8em;
        }

        /* Alert System */
        .alerts-container {
            max-height: 400px;
            overflow-y: auto;
        }

        .alert-item {
            background: rgba(255, 255, 255, 0.05);
            border-left: 4px solid;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }

        .alert-item:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .alert-item.critical { border-left-color: #F44336; }
        .alert-item.warning { border-left-color: #FF9800; }
        .alert-item.info { border-left-color: #2196F3; }

        .alert-content {
            color: white;
            line-height: 1.4;
        }

        .alert-time {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8em;
            margin-top: 5px;
        }

        /* AI Chat Section */
        .chat-section {
            grid-column: 1 / -1;
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            box-shadow: var(--shadow-soft);
            height: 600px;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }

        .ai-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--success-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5em;
        }

        .chat-title {
            flex: 1;
        }

        .chat-title h3 {
            color: white;
            font-size: 1.3em;
            margin-bottom: 5px;
        }

        .chat-subtitle {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
        }

        /* Quick Action Suggestions */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }

        .quick-action {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quick-action:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        /* Chat Messages */
        .chat-messages {
            flex: 1;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            overflow-y: auto;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .message {
            margin-bottom: 20px;
            padding: 15px 20px;
            border-radius: 20px;
            max-width: 85%;
            line-height: 1.5;
            position: relative;
            animation: messageSlide 0.3s ease-out;
        }

        @keyframes messageSlide {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message.user {
            background: var(--success-gradient);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }

        .message.ai {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-bottom-left-radius: 5px;
            white-space: pre-wrap;
        }

        .message-time {
            font-size: 0.7em;
            opacity: 0.7;
            margin-top: 5px;
        }

        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            color: rgba(255, 255, 255, 0.7);
        }

        .typing-dots {
            display: flex;
            gap: 3px;
        }

        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            animation: typingDot 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typingDot {
            0%, 60%, 100% { opacity: 0.3; transform: scale(0.8); }
            30% { opacity: 1; transform: scale(1); }
        }

        /* Chat Input */
        .chat-input {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .chat-input-field {
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            padding: 15px 20px;
            color: white;
            font-size: 1em;
            outline: none;
            transition: all 0.3s ease;
        }

        .chat-input-field:focus {
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.15);
        }

        .chat-input-field::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }

        .send-button {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--success-gradient);
            border: none;
            color: white;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .send-button:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        .send-button:disabled {
            background: rgba(255, 255, 255, 0.2);
            cursor: not-allowed;
            transform: none;
        }

        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 1024px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            }
        }

        @media (max-width: 768px) {
            .dashboard {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2.2em;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .metric-card {
                padding: 20px;
            }
            
            .quick-actions {
                flex-direction: column;
            }
            
            .quick-action {
                text-align: center;
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <!-- Animated Background Particles -->
    <div class="particles" id="particles"></div>

    <div class="dashboard">
        <!-- Header Section -->
        <div class="header">
            <h1>
                <i class="fas fa-solar-panel"></i>
                DGR KPI Intelligence
                <span class="status-indicator" id="statusIndicator">
                    <i class="fas fa-circle"></i>
                    <span id="statusText">Initializing...</span>
                </span>
            </h1>
            <div class="subtitle">
                <span>Intelligent Analytics • Real-time Monitoring • Predictive Insights</span>
                <span id="lastUpdate">System starting...</span>
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="metrics-grid" id="metricsGrid">
            <div class="metric-card">
                <div class="metric-icon"><i class="fas fa-bolt"></i></div>
                <div class="metric-title">System Status</div>
                <div class="metric-value">Loading...</div>
                <div class="metric-unit">Initializing components</div>
                <div class="metric-trend">⚡ Starting</div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Plant Performance Section -->
            <div class="content-section">
                <div class="section-header">
                    <div class="section-icon">
                        <i class="fas fa-industry"></i>
                    </div>
                    <div>
                        <div class="section-title">Plant Performance</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9em;">Real-time monitoring across all facilities</div>
                    </div>
                </div>
                <div class="plant-grid" id="plantsContainer">
                    <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 40px;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 2em; margin-bottom: 15px;"></i>
                        <div>Loading plant performance data...</div>
                    </div>
                </div>
            </div>

            <!-- Alerts Section -->
            <div class="content-section">
                <div class="section-header">
                    <div class="section-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div>
                        <div class="section-title">Smart Alerts</div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.9em;">AI-powered notifications</div>
                    </div>
                </div>
                <div class="alerts-container" id="alertsContainer">
                    <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 20px;">
                        <i class="fas fa-search" style="font-size: 1.5em; margin-bottom: 10px;"></i>
                        <div>Analyzing system for alerts...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- AI Chat Section -->
        <div class="chat-section">
            <div class="chat-header">
                <div class="ai-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="chat-title">
                    <h3>AI Assistant</h3>
                    <div class="chat-subtitle">Your intelligent DGR operations companion</div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="quick-actions">
                <div class="quick-action" onclick="sendQuickQuery('portfolio summary')">
                    <i class="fas fa-chart-line"></i> Portfolio Summary
                </div>
                <div class="quick-action" onclick="sendQuickQuery('yesterday performance')">
                    <i class="fas fa-calendar-day"></i> Yesterday's Performance
                </div>
                <div class="quick-action" onclick="sendQuickQuery('any plants down today?')">
                    <i class="fas fa-exclamation-circle"></i> Plant Status
                </div>
                <div class="quick-action" onclick="sendQuickQuery('compare best vs worst plants')">
                    <i class="fas fa-balance-scale"></i> Plant Comparison
                </div>
                <div class="quick-action" onclick="sendQuickQuery('financial performance this month')">
                    <i class="fas fa-money-bill-wave"></i> Financial Analysis
                </div>
                <div class="quick-action" onclick="sendQuickQuery('help')">
                    <i class="fas fa-question-circle"></i> Help
                </div>
            </div>

            <!-- Chat Messages -->
            <div class="chat-messages" id="chatMessages">
                <div class="message ai">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <i class="fas fa-robot" style="color: #4CAF50;"></i>
                        <strong>Your AI Assistant is Ready!</strong>
                    </div>
                    
                    I'm your intelligent DGR operations companion, designed to understand your workplace needs and provide human-like responses. Here's what makes me special:

                    <div style="margin: 15px 0;">
                        <strong>🧠 Smart Features:</strong><br>
                        • I learn from our conversations and adapt to your preferences<br>
                        • I understand context and remember what we've discussed<br>
                        • I handle missing data gracefully and explain availability<br>
                        • I adjust my responses based on your role (Operations, Technical, Executive)<br>
                    </div>

                    <div style="margin: 15px 0;">
                        <strong>💼 Real Workplace Scenarios I Handle:</strong><br>
                        • "Any plants down today?" - Morning operations check<br>
                        • "Why is 7MW underperforming?" - Diagnostic analysis<br>
                        • "Show me executive summary for board meeting" - Management reports<br>
                        • "What was performance on June 12th?" - Historical data (with availability checking)<br>
                        • "Compare solar vs wind portfolio" - Comparative analysis<br>
                    </div>

                    <strong>Ask me anything about your DGR plants - I'm here to help! 🚀</strong>
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                </div>
            </div>

            <!-- Chat Input -->
            <div class="chat-input">
                <input type="text" class="chat-input-field" id="chatInput" 
                       placeholder="Ask me about plant performance, alerts, comparisons, financial analysis...">
                <button class="send-button" id="sendButton" onclick="sendMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let isProcessing = false;
        let particlesInitialized = false;

        // Initialize particles animation
        function initParticles() {
            if (particlesInitialized) return;
            
            const particlesContainer = document.getElementById('particles');
            const particleCount = 15;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                const size = Math.random() * 4 + 2;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
                
                particlesContainer.appendChild(particle);
            }
            
            particlesInitialized = true;
        }

        // Update dashboard data
        function updateDashboard() {
            fetch('/api/dashboard')
                .then(response => response.json())
                .then(data => {
                    updateMetrics(data.portfolio_metrics || {});
                    updatePlants(data.plant_summaries || []);
                    updateAlerts(data.system_alerts || []);
                    updateSystemStatus(data.system_status || {});
                    updateTimestamp(data.last_updated);
                })
                .catch(error => {
                    console.error('Dashboard update error:', error);
                    updateSystemStatus({ initialized: false, error_message: 'Connection failed' });
                });
        }

        function updateMetrics(metrics) {
            const grid = document.getElementById('metricsGrid');
            grid.innerHTML = `
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-bolt"></i></div>
                    <div class="metric-title">Total Energy Export</div>
                    <div class="metric-value">${formatNumber(metrics.total_energy || 0)}</div>
                    <div class="metric-unit">kWh (Portfolio Total)</div>
                    <div class="metric-trend trend-up"><i class="fas fa-arrow-up"></i> Active</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-percentage"></i></div>
                    <div class="metric-title">Portfolio Availability</div>
                    <div class="metric-value">${(metrics.avg_availability || 0).toFixed(1)}%</div>
                    <div class="metric-unit">Average Uptime</div>
                    <div class="metric-trend ${metrics.avg_availability >= 95 ? 'trend-up' : 'trend-down'}">
                        <i class="fas fa-${metrics.avg_availability >= 95 ? 'arrow-up' : 'arrow-down'}"></i> 
                        ${metrics.avg_availability >= 95 ? 'Excellent' : 'Needs Attention'}
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-tachometer-alt"></i></div>
                    <div class="metric-title">Performance Ratio</div>
                    <div class="metric-value">${(metrics.avg_performance || 0).toFixed(1)}%</div>
                    <div class="metric-unit">System Efficiency</div>
                    <div class="metric-trend ${metrics.avg_performance >= 80 ? 'trend-up' : 'trend-down'}">
                        <i class="fas fa-${metrics.avg_performance >= 80 ? 'arrow-up' : 'arrow-down'}"></i> 
                        ${metrics.avg_performance >= 80 ? 'Optimal' : 'Below Target'}
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon"><i class="fas fa-industry"></i></div>
                    <div class="metric-title">Plant Status</div>
                    <div class="metric-value">${metrics.operational_plants || 0}/${metrics.total_plants || 0}</div>
                    <div class="metric-unit">Operational Plants</div>
                    <div class="metric-trend trend-up">
                        <i class="fas fa-check-circle"></i> 
                        ${((metrics.operational_plants || 0) / (metrics.total_plants || 1) * 100).toFixed(0)}% Online
                    </div>
                </div>
            `;
        }

        function updatePlants(plants) {
            const container = document.getElementById('plantsContainer');
            if (plants.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 40px;">
                        <i class="fas fa-spinner fa-spin" style="font-size: 2em; margin-bottom: 15px;"></i>
                        <div>Loading plant performance data...</div>
                    </div>
                `;
                return;
            }

            container.innerHTML = plants.map(plant => `
                <div class="plant-card ${plant.status}" onclick="queryPlant('${plant.name}')">
                    <div class="plant-status-indicator"></div>
                    <div class="plant-header">
                        <div class="plant-name">
                            <i class="fas fa-solar-panel"></i> ${plant.name}
                        </div>
                        <div class="plant-status-badge ${plant.status}">
                            ${getStatusText(plant.status)}
                        </div>
                    </div>
                    <div class="plant-metrics">
                        <div class="plant-metric">
                            <div class="plant-metric-value">${plant.availability}%</div>
                            <div class="plant-metric-label">Availability</div>
                        </div>
                        <div class="plant-metric">
                            <div class="plant-metric-value">${plant.performance}%</div>
                            <div class="plant-metric-label">Performance</div>
                        </div>
                        <div class="plant-metric">
                            <div class="plant-metric-value">${formatNumber(plant.energy)}</div>
                            <div class="plant-metric-label">Energy (kWh)</div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function updateAlerts(alerts) {
            const container = document.getElementById('alertsContainer');
            if (alerts.length === 0) {
                container.innerHTML = `
                    <div class="alert-item info">
                        <div class="alert-content">
                            <i class="fas fa-check-circle" style="color: #4CAF50; margin-right: 10px;"></i>
                            <strong>All Systems Operational</strong><br>
                            No critical alerts detected. All plants operating within normal parameters.
                        </div>
                        <div class="alert-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
                return;
            }

            container.innerHTML = alerts.map(alert => {
                const alertType = alert.includes('🚨') ? 'critical' : 
                                alert.includes('⚠️') ? 'warning' : 'info';
                
                return `
                    <div class="alert-item ${alertType}">
                        <div class="alert-content">${alert}</div>
                        <div class="alert-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
            }).join('');
        }

        function updateSystemStatus(status) {
            const indicator = document.getElementById('statusIndicator');
            const statusText = document.getElementById('statusText');
            
            if (status.initialized) {
                indicator.className = 'status-indicator';
                statusText.textContent = `Online (${status.plants_loaded || 0} plants)`;
            } else {
                indicator.className = 'status-indicator error';
                statusText.textContent = status.error_message || 'System Error';
            }
        }

        function updateTimestamp(timestamp) {
            if (timestamp) {
                document.getElementById('lastUpdate').textContent = `Last updated: ${timestamp}`;
            }
        }

        function getStatusText(status) {
            const statusMap = {
                'operational': '🟢 Online',
                'warning': '🟡 Warning', 
                'critical': '🔴 Critical',
                'no_data': '⚫ No Data'
            };
            return statusMap[status] || status;
        }

        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toLocaleString();
        }

        // Chat functionality
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const button = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message || isProcessing) return;
            
            isProcessing = true;
            const chatMessages = document.getElementById('chatMessages');
            
            // Add user message
            addMessage('user', message);
            
            // Add typing indicator
            addTypingIndicator();
            
            input.value = '';
            button.disabled = true;
            button.innerHTML = '<div class="loading-spinner"></div>';
            
            // Send to AI
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                addMessage('ai', data.response);
            })
            .catch(error => {
                removeTypingIndicator();
                addMessage('ai', '❌ I apologize, but I encountered an error processing your request. Please try again.');
            })
            .finally(() => {
                isProcessing = false;
                button.disabled = false;
                button.innerHTML = '<i class="fas fa-paper-plane"></i>';
                input.focus();
            });
        }

        function sendQuickQuery(query) {
            document.getElementById('chatInput').value = query;
            sendMessage();
        }

        function queryPlant(plantName) {
            const queries = [
                `Tell me about ${plantName} performance`,
                `Detailed analysis for ${plantName}`,
                `What's the status of ${plantName}?`,
                `How is ${plantName} performing today?`
            ];
            const randomQuery = queries[Math.floor(Math.random() * queries.length)];
            document.getElementById('chatInput').value = randomQuery;
            sendMessage();
        }

        function addMessage(type, content) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            if (type === 'ai') {
                messageDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <i class="fas fa-robot" style="color: #4CAF50;"></i>
                        <strong>AI Assistant</strong>
                    </div>
                    ${content}
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                `;
            } else {
                messageDiv.innerHTML = `
                    ${content}
                    <div class="message-time">${new Date().toLocaleTimeString()}</div>
                `;
            }
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function addTypingIndicator() {
            const chatMessages = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message ai';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `
                <div class="typing-indicator">
                    <i class="fas fa-robot" style="color: #4CAF50; margin-right: 8px;"></i>
                    <span>AI is thinking</span>
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            `;
            
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function removeTypingIndicator() {
            const typingIndicator = document.getElementById('typingIndicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
        }

        // Keyboard event handlers
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !isProcessing) {
                sendMessage();
            }
        });

        // Auto-resize chat input
        document.getElementById('chatInput').addEventListener('input', function(e) {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Initialize dashboard
        function initializeDashboard() {
            console.log('🚀 Initializing Beautiful DGR Dashboard');
            
            // Initialize particles
            initParticles();
            
            // Initial dashboard update
            updateDashboard();
            
            // Set up periodic updates
            setInterval(updateDashboard, 60000); // Update every minute
            
            // Focus on chat input
            setTimeout(() => {
                document.getElementById('chatInput').focus();
            }, 1000);
            
            console.log('✅ Dashboard initialized successfully');
        }

        // Start dashboard when page loads
        document.addEventListener('DOMContentLoaded', initializeDashboard);

        // Add some interactive effects
        document.addEventListener('mousemove', function(e) {
            const particles = document.querySelectorAll('.particle');
            particles.forEach((particle, index) => {
                const speed = (index + 1) * 0.01;
                const x = (e.clientX * speed) / 50;
                const y = (e.clientY * speed) / 50;
                particle.style.transform = `translate(${x}px, ${y}px)`;
            });
        });

        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + / for help
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                sendQuickQuery('help');
            }
            
            // Ctrl/Cmd + Enter for portfolio summary
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                sendQuickQuery('portfolio summary');
            }
        });

        // Add smooth scroll behavior for messages
        function smoothScrollToBottom(element) {
            element.scrollTo({
                top: element.scrollHeight,
                behavior: 'smooth'
            });
        }

        // Enhance visual feedback
        document.querySelectorAll('.quick-action, .plant-card, .metric-card').forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.02)';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>
"""

# Flask Routes for Beautiful Dashboard
@app.route('/')
def beautiful_dashboard():
    """Serve the beautiful dashboard"""
    return BEAUTIFUL_HTML_TEMPLATE

@app.route('/api/dashboard')
def api_dashboard_enhanced():
    """Enhanced dashboard API with beautiful data formatting"""
    try:
        return jsonify({
            'portfolio_metrics': dashboard_data['portfolio_metrics'],
            'plant_summaries': dashboard_data['plant_summaries'],
            'system_alerts': dashboard_data['system_alerts'],
            'data_quality': dashboard_data['data_quality'],
            'system_status': system_status,
            'last_updated': dashboard_data['last_updated']
        })
        
    except Exception as e:
        logger.error(f"Beautiful dashboard API error: {str(e)}")
        return jsonify({
            'error': str(e),
            'system_status': {'initialized': False, 'error_message': str(e)}
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat_enhanced():
    """Enhanced chat API with beautiful AI responses"""
    try:
        if not system_status['ai_ready']:
            return jsonify({
                'response': '🤖 AI Assistant is still initializing. Please wait a moment and try again.',
                'error': True
            })
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'response': 'I didn\'t receive your message properly. Could you please try again?',
                'error': True
            })
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'response': 'I\'m here to help! Please ask me anything about your DGR plants.',
                'error': True
            })
        
        logger.info(f"Processing beautiful AI query: {user_message[:100]}...")
        
        # Process with Enhanced AI Assistant
        response = enhanced_ai.process_query(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': False,
            'ai_version': 'Enhanced Beautiful AI v2.0'
        })
        
    except Exception as e:
        logger.error(f"Beautiful chat API error: {str(e)}")
        return jsonify({
            'response': f'I encountered a technical issue: {str(e)}. Please try rephrasing your question, and I\'ll do my best to help!',
            'error': True
        })

@app.route('/api/status')
def api_status():
    """Beautiful system status API"""
    try:
        return jsonify({
            'system_status': system_status,
            'dashboard_health': 'Beautiful dashboard operational',
            'ai_status': 'Enhanced AI ready' if system_status['ai_ready'] else 'AI initializing',
            'version': 'Beautiful DGR Dashboard v2.0',
            'features': [
                'Glassmorphism Design',
                'Animated Particles',
                'Enhanced AI Assistant',
                'Real-time Monitoring',
                'Smart Alerts',
                'Mobile Responsive'
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plant/<plant_name>')
def api_plant_details(plant_name):
    """Get detailed plant information"""
    try:
        # Find plant in dashboard data
        plant_info = None
        for plant in dashboard_data['plant_summaries']:
            if plant['name'].lower() == plant_name.lower():
                plant_info = plant
                break
        
        if not plant_info:
            return jsonify({'error': f'Plant {plant_name} not found'}), 404
        
        # Enhanced plant details
        detailed_info = {
            'basic_info': plant_info,
            'performance_history': {
                'last_7_days': [94.2, 95.1, 93.8, 96.2, 94.7, 95.5, plant_info['availability']],
                'trend': plant_info['trend'],
                'best_day': '2024-06-10',
                'worst_day': '2024-06-08'
            },
            'alerts': [
                alert for alert in dashboard_data['system_alerts'] 
                if plant_name.lower() in alert.lower()
            ],
            'recommendations': [
                'Monitor performance trends closely',
                'Schedule preventive maintenance',
                'Optimize based on weather patterns'
            ]
        }
        
        return jsonify(detailed_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main function to start the beautiful dashboard"""
    print("🎨 Beautiful DGR KPI Intelligence Dashboard")
    print("=" * 60)
    print("✨ Features:")
    print("  • Stunning glassmorphism design with animated particles")
    print("  • Enhanced AI with human-like responses (100+ scenarios)")
    print("  • Real-time data visualization with smooth animations")
    print("  • Mobile-responsive interface with touch gestures")
    print("  • Interactive chat with context awareness")
    print("  • Smart alerts and beautiful notifications")
    print("  • Executive, Technical, and Operations modes")
    print("")
    print("🌐 Dashboard URL: http://localhost:5008")
    print("🤖 AI Assistant ready for workplace scenarios")
    print("⌨️  Keyboard shortcuts: Ctrl+/ (help), Ctrl+Enter (summary)")
    print("")
    print("🚀 Integration Instructions:")
    print("  1. Uncomment the import lines for your actual modules")
    print("  2. Replace MockEnhancedAI with your EnhancedHumanAIAssistant")
    print("  3. Replace create_sample_data() with actual data loading")
    print("  4. Update dashboard_data with real plant information")
    print("")
    print("📁 File Structure:")
    print("  ├── beautiful_dashboard_interface.py (this file)")
    print("  ├── enhanced_human_ai_assistant.py (enhanced AI)")
    print("  ├── robust_dgr_excel_reader.py (your data reader)")
    print("  └── Files/ (your Excel files directory)")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Initialize system in background thread
    def background_init():
        if initialize_beautiful_system():
            # Start background updater
            updater_thread = threading.Thread(target=background_beautiful_updater, daemon=True)
            updater_thread.start()
            logger.info("✅ Beautiful background services started")
        else:
            logger.error("❌ Beautiful system initialization failed")
    
    init_thread = threading.Thread(target=background_init, daemon=True)
    init_thread.start()
    
    try:
        app.run(host='0.0.0.0', port=5008, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Beautiful dashboard stopped by user")
        logger.info("Beautiful dashboard shutdown completed")
    except Exception as e:
        logger.error(f"Beautiful server error: {str(e)}")
        print(f"\n❌ Server error: {str(e)}")

# Additional utility functions for integration

def integrate_with_existing_system(excel_reader_instance, ai_assistant_instance):
    """
    Integration function to connect with your existing system
    Call this function to replace the mock components with real ones
    """
    global excel_reader, enhanced_ai
    
    excel_reader = excel_reader_instance
    enhanced_ai = ai_assistant_instance
    
    # Update system status
    system_status.update({
        'initialized': True,
        'ai_ready': True,
        'integration_complete': True
    })
    
    logger.info("✅ Beautiful dashboard integrated with existing system")

def create_custom_plant_widget(plant_name, metrics):
    """
    Create a custom widget for specific plant monitoring
    Returns HTML for embedding in custom dashboards
    """
    widget_html = f"""
    <div class="custom-plant-widget" style="
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    ">
        <h3 style="margin: 0 0 15px 0; color: #4CAF50;">
            <i class="fas fa-solar-panel"></i> {plant_name}
        </h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{metrics.get('availability', 0):.1f}%</div>
                <div style="font-size: 0.8em; opacity: 0.7;">Availability</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{metrics.get('performance', 0):.1f}%</div>
                <div style="font-size: 0.8em; opacity: 0.7;">Performance</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.5em; font-weight: bold;">{metrics.get('energy', 0):,.0f}</div>
                <div style="font-size: 0.8em; opacity: 0.7;">kWh</div>
            </div>
        </div>
    </div>
    """
    return widget_html

def export_dashboard_config():
    """
    Export current dashboard configuration for backup/sharing
    """
    config = {
        'system_status': system_status,
        'dashboard_data': dashboard_data,
        'timestamp': datetime.now().isoformat(),
        'version': 'Beautiful DGR Dashboard v2.0'
    }
    
    try:
        with open('dashboard_config_backup.json', 'w') as f:
            json.dump(config, f, indent=2, default=str)
        logger.info("✅ Dashboard configuration exported")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to export config: {str(e)}")
        return False

# Health check endpoint
@app.route('/health')
def health_check():
    """System health check"""
    return jsonify({
        'status': 'healthy' if system_status['initialized'] else 'initializing',
        'version': 'Beautiful DGR Dashboard v2.0',
        'uptime': (datetime.now() - system_status.get('start_time', datetime.now())).total_seconds(),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == "__main__":
    # Initialize start time
    system_status['start_time'] = datetime.now()
    
    # Start the beautiful dashboard
    main()