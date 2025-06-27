#!/usr/bin/env python3
"""
Clean Formatted Chatbot - Demo Mode (No Pandas Required)
Perfect for initial deployment
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanChatbot:
    """
    Clean chatbot with demo mode for deployment
    """
    
    def __init__(self):
        self.is_initialized = False
        
        # Demo plant data for showcase
        self.demo_plants = {
            'CEPPL_WIND': {
                'name': 'CEPPL Wind Farm',
                'type': '🌪️ Wind Power',
                'total_generation': 24272985,
                'daily_average': 159691,
                'peak_output': 1072005,
                'availability': 96.5,
                'performance_ratio': 87.3,
                'capacity_factor': 28.5
            },
            'AXPPL_SOLAR': {
                'name': 'AXPPL Solar Plant',
                'type': '☀️ Solar Power',
                'total_generation': 18945672,
                'daily_average': 124387,
                'peak_output': 890234,
                'availability': 94.2,
                'performance_ratio': 91.7,
                'capacity_factor': 32.1
            },
            'PSEGPL_HYDRO': {
                'name': 'PSEGPL Hydroelectric',
                'type': '💧 Hydroelectric',
                'total_generation': 31567890,
                'daily_average': 207345,
                'peak_output': 1245678,
                'availability': 98.1,
                'performance_ratio': 89.4,
                'capacity_factor': 45.8
            },
            'CSPPL_THERMAL': {
                'name': 'CSPPL Thermal Plant',
                'type': '⚙️ Thermal Power',
                'total_generation': 42156789,
                'daily_average': 276234,
                'peak_output': 1567890,
                'availability': 92.8,
                'performance_ratio': 85.6,
                'capacity_factor': 67.3
            }
        }
        
        # Plant aliases for flexible matching
        self.plant_aliases = {
            'ceppl': 'CEPPL_WIND',
            'wind': 'CEPPL_WIND',
            'axppl': 'AXPPL_SOLAR',
            'solar': 'AXPPL_SOLAR',
            'psegpl': 'PSEGPL_HYDRO',
            'hydro': 'PSEGPL_HYDRO',
            'csppl': 'CSPPL_THERMAL',
            'thermal': 'CSPPL_THERMAL'
        }
        
        logger.info("Demo Chatbot initialized")
    
    def initialize_system(self):
        """Initialize demo system"""
        try:
            logger.info("Initializing demo chatbot...")
            self.is_initialized = True
            logger.info("Demo chatbot ready with sample data!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize: {str(e)}")
            return False
    
    def process_query(self, user_query: str) -> str:
        """Process query with demo data"""
        
        if not self.is_initialized:
            return "❌ System not initialized. Please restart the server."
        
        try:
            query = user_query.lower().strip()
            query = self._clean_query(query)
            mentioned_plants = self._find_plants_in_query(query)
            intent = self._detect_intent(query, mentioned_plants)
            
            return self._generate_demo_response(intent, query, mentioned_plants, user_query)
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "❌ Unable to process request. Please try rephrasing your query."
    
    def _clean_query(self, query: str) -> str:
        """Remove filler words"""
        filler_words = ['tell', 'me', 'about', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'what', 'how', 'can', 'you', 'please']
        words = query.split()
        cleaned_words = [word for word in words if word not in filler_words]
        return ' '.join(cleaned_words)
    
    def _find_plants_in_query(self, query: str) -> List[str]:
        """Find plant names in query using aliases"""
        found_plants = []
        
        for alias, plant_name in self.plant_aliases.items():
            if alias in query:
                if plant_name not in found_plants:
                    found_plants.append(plant_name)
        
        return found_plants
    
    def _detect_intent(self, query: str, plants: List[str]) -> str:
        """Detect user intent"""
        
        if plants and len(plants) == 1:
            if any(word in query for word in ['performance', 'doing', 'stats', 'information', 'data']):
                return 'plant_analysis'
        
        if len(plants) >= 2 or any(word in query for word in ['compare', 'vs', 'versus', 'difference', 'between']):
            return 'comparison'
        
        if any(word in query for word in ['best', 'worst', 'top', 'bottom', 'most', 'least', 'highest', 'lowest']):
            return 'ranking'
        
        if any(word in query for word in ['energy', 'power', 'generation', 'kwh']):
            return 'energy_query'
        
        if any(word in query for word in ['portfolio', 'all', 'total', 'overall']):
            return 'portfolio'
        
        if plants:
            return 'plant_analysis'
        
        return 'general'
    
    def _generate_demo_response(self, intent: str, query: str, plants: List[str], original_query: str) -> str:
        """Generate demo responses"""
        
        if intent == 'plant_analysis':
            return self._create_plant_analysis(plants[0] if plants else None)
        elif intent == 'comparison':
            return self._create_comparison_analysis(plants)
        elif intent == 'ranking':
            return self._create_ranking_analysis()
        elif intent == 'energy_query':
            return self._create_energy_analysis(plants)
        elif intent == 'portfolio':
            return self._create_portfolio_analysis()
        else:
            return self._create_help_message()
    
    def _create_plant_analysis(self, plant_name: str) -> str:
        """Create demo plant analysis"""
        
        if not plant_name or plant_name not in self.demo_plants:
            return """💡 Please specify which plant you would like to analyze.

Available demo plants:
• CEPPL (Wind Power)
• AXPPL (Solar Power) 
• PSEGPL (Hydroelectric)
• CSPPL (Thermal Power)

Example: 'Analyze CEPPL performance'"""
        
        plant = self.demo_plants[plant_name]
        
        response = f"🏭 PLANT ANALYSIS: {plant['name'].upper()}\n"
        response += "═" * 50 + "\n\n"
        
        response += f"📊 DATA OVERVIEW\n"
        response += f"• Plant Type: {plant['type']}\n"
        response += f"• Analysis Period: Demo Data (Last 12 months)\n\n"
        
        response += f"⚡ ENERGY PERFORMANCE\n"
        response += f"• Total Generation: {plant['total_generation']:,.0f} kWh\n"
        response += f"• Daily Average: {plant['daily_average']:,.0f} kWh\n"
        response += f"• Peak Daily Output: {plant['peak_output']:,.0f} kWh\n\n"
        
        response += f"📈 OPERATIONAL METRICS\n"
        response += f"• Plant Availability: {plant['availability']:.1f}%\n"
        
        if plant['availability'] > 95:
            status = "✅ EXCELLENT"
        elif plant['availability'] > 85:
            status = "⚠️ GOOD"
        else:
            status = "🔴 NEEDS ATTENTION"
        
        response += f"• Operational Status: {status}\n"
        response += f"• Performance Ratio: {plant['performance_ratio']:.1f}%\n"
        response += f"• Capacity Factor: {plant['capacity_factor']:.1f}%\n\n"
        
        response += f"💡 KEY INSIGHTS\n"
        response += f"• This is demo data showcasing dashboard capabilities\n"
        response += f"• Real plant data integration available with pandas\n"
        response += f"• Contact admin to connect live data sources\n"
        
        return response
    
    def _create_comparison_analysis(self, plants: List[str]) -> str:
        """Create demo comparison"""
        
        if len(plants) < 2:
            plants = ['CEPPL_WIND', 'AXPPL_SOLAR']  # Default comparison
        
        plant1_name, plant2_name = plants[0], plants[1]
        plant1 = self.demo_plants[plant1_name]
        plant2 = self.demo_plants[plant2_name]
        
        response = f"⚖️ PLANT COMPARISON\n"
        response += f"{plant1['name']} vs {plant2['name']}\n"
        response += "═" * 50 + "\n\n"
        
        response += f"⚡ ENERGY GENERATION\n"
        response += f"• {plant1['name']}: {plant1['total_generation']:,.0f} kWh\n"
        response += f"• {plant2['name']}: {plant2['total_generation']:,.0f} kWh\n\n"
        
        if plant1['total_generation'] > plant2['total_generation']:
            diff_pct = ((plant1['total_generation'] - plant2['total_generation']) / plant2['total_generation']) * 100
            response += f"🏆 WINNER: {plant1['name'].upper()}\n"
            response += f"• Advantage: {diff_pct:.1f}% higher generation\n"
        else:
            diff_pct = ((plant2['total_generation'] - plant1['total_generation']) / plant1['total_generation']) * 100
            response += f"🏆 WINNER: {plant2['name'].upper()}\n"
            response += f"• Advantage: {diff_pct:.1f}% higher generation\n"
        
        response += f"\n📊 AVAILABILITY COMPARISON\n"
        response += f"• {plant1['name']}: {plant1['availability']:.1f}%\n"
        response += f"• {plant2['name']}: {plant2['availability']:.1f}%\n"
        
        return response
    
    def _create_ranking_analysis(self) -> str:
        """Create demo ranking"""
        
        # Sort plants by total generation
        sorted_plants = sorted(self.demo_plants.items(), 
                             key=lambda x: x[1]['total_generation'], 
                             reverse=True)
        
        response = "🏆 PLANT PERFORMANCE RANKING\n"
        response += "═" * 50 + "\n\n"
        
        for i, (plant_id, plant) in enumerate(sorted_plants, 1):
            response += f"{i}. {plant['name']}: {plant['total_generation']:,.0f} kWh ({plant['type']})\n"
        
        return response
    
    def _create_energy_analysis(self, plants: List[str]) -> str:
        """Create demo energy analysis"""
        
        if plants:
            total_energy = sum(self.demo_plants[plant]['total_generation'] 
                             for plant in plants if plant in self.demo_plants)
            
            response = f"⚡ ENERGY GENERATION ANALYSIS\n"
            response += "═" * 50 + "\n\n"
            
            for plant in plants:
                if plant in self.demo_plants:
                    data = self.demo_plants[plant]
                    response += f"• {data['name']}: {data['total_generation']:,.0f} kWh\n"
            
            if len(plants) > 1:
                response += f"\n📊 SUMMARY\n"
                response += f"• Combined Total: {total_energy:,.0f} kWh\n"
                response += f"• Average Generation: {total_energy/len(plants):,.0f} kWh\n"
            
            return response
        else:
            return self._create_portfolio_analysis()
    
    def _create_portfolio_analysis(self) -> str:
        """Create demo portfolio overview"""
        
        total_energy = sum(plant['total_generation'] for plant in self.demo_plants.values())
        plant_count = len(self.demo_plants)
        
        response = f"🏭 PORTFOLIO OVERVIEW\n"
        response += "═" * 50 + "\n\n"
        
        response += f"📊 EXECUTIVE SUMMARY\n"
        response += f"• Total Plants: {plant_count}\n"
        response += f"• Total Generation: {total_energy:,.0f} kWh\n"
        response += f"• Average per Plant: {total_energy/plant_count:,.0f} kWh\n\n"
        
        # Sort by generation
        sorted_plants = sorted(self.demo_plants.items(), 
                             key=lambda x: x[1]['total_generation'], 
                             reverse=True)
        
        response += f"🏆 TOP CONTRIBUTORS\n"
        for i, (plant_id, plant) in enumerate(sorted_plants, 1):
            percentage = (plant['total_generation'] / total_energy) * 100
            response += f"{i}. {plant['name']}: {plant['total_generation']:,.0f} kWh ({percentage:.1f}%)\n"
        
        response += f"\n💡 DEMO MODE ACTIVE\n"
        response += f"• This dashboard is running with sample data\n"
        response += f"• Real-time plant data integration available\n"
        response += f"• All analytics features fully functional\n"
        
        return response
    
    def _create_help_message(self) -> str:
        """Create demo help message"""
        
        response = f"🤖 POWER PLANT AI ASSISTANT (DEMO MODE)\n"
        response += "═" * 50 + "\n\n"
        
        response += f"💡 Available Commands:\n\n"
        
        response += f"📊 PLANT ANALYSIS\n"
        response += f"• 'Analyze CEPPL performance'\n"
        response += f"• 'Tell me about AXPPL'\n"
        response += f"• 'PSEGPL stats'\n\n"
        
        response += f"⚖️ PLANT COMPARISON\n"
        response += f"• 'Compare CEPPL and AXPPL'\n"
        response += f"• 'CSPPL vs PSEGPL'\n\n"
        
        response += f"🏭 PORTFOLIO MANAGEMENT\n"
        response += f"• 'Portfolio overview'\n"
        response += f"• 'Top performing plants'\n"
        response += f"• 'Energy generation summary'\n\n"
        
        response += f"🌟 DEMO PLANTS AVAILABLE:\n"
        response += f"• CEPPL (Wind Power)\n"
        response += f"• AXPPL (Solar Power)\n"
        response += f"• PSEGPL (Hydroelectric)\n"
        response += f"• CSPPL (Thermal Power)\n"
        
        return response

# Compatibility wrapper
class MainAISystem(CleanChatbot):
    """Wrapper for compatibility"""
    pass