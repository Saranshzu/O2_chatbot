#!/usr/bin/env python3
"""
Clean Formatted Chatbot - main_ai_system.py
Perfect formatting for web display
"""

import pandas as pd
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from clean_fixed_processor import DataProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanChatbot:
    """
    Clean chatbot with perfect web formatting
    """
    
    def __init__(self):
        self.data_processor = None
        self.is_initialized = False
        self.plant_aliases = {}
        
        logger.info("Clean Chatbot initialized")
    
    def initialize_system(self):
        """Initialize with data processor"""
        try:
            logger.info("Initializing clean chatbot...")
            
            self.data_processor = DataProcessor()
            success = self.data_processor.load_all_plants()
            
            if success:
                self._setup_plant_aliases()
                self.is_initialized = True
                logger.info("Clean chatbot ready")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to initialize: {str(e)}")
            return False
    
    def _setup_plant_aliases(self):
        """Setup plant name aliases for flexible matching"""
        all_plants = self.data_processor.get_available_plants()
        
        for plant in all_plants:
            self.plant_aliases[plant.lower()] = plant
            
            parts = plant.split('_')
            for part in parts:
                if len(part) > 2:
                    self.plant_aliases[part.lower()] = plant
            
            self.plant_aliases[plant.replace('_', '').lower()] = plant
            clean_name = re.sub(r'\d+', '', plant).replace('_', '').lower()
            if clean_name:
                self.plant_aliases[clean_name] = plant
    
    def process_query(self, user_query: str) -> str:
        """Process query with clean formatting"""
        
        if not self.is_initialized:
            return "❌ System not initialized. Please restart the server."
        
        try:
            query = user_query.lower().strip()
            query = self._clean_query(query)
            mentioned_plants = self._find_plants_in_query(query)
            intent = self._detect_intent(query, mentioned_plants)
            
            return self._generate_clean_response(intent, query, mentioned_plants, user_query)
            
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
        
        if any(word in query for word in ['june', 'july', 'may', 'april', 'yesterday', 'today', '12th', '11th', '6th']):
            return 'date_query'
        
        if any(word in query for word in ['best', 'worst', 'top', 'bottom', 'most', 'least', 'highest', 'lowest']):
            return 'ranking'
        
        if any(word in query for word in ['energy', 'power', 'generation', 'kwh']):
            return 'energy_query'
        
        if any(word in query for word in ['portfolio', 'all', 'total', 'overall']):
            return 'portfolio'
        
        if plants:
            return 'plant_analysis'
        
        return 'general'
    
    def _generate_clean_response(self, intent: str, query: str, plants: List[str], original_query: str) -> str:
        """Generate clean responses"""
        
        if intent == 'plant_analysis':
            return self._create_plant_analysis(plants[0] if plants else None, original_query)
        elif intent == 'comparison':
            return self._create_comparison_analysis(plants, original_query)
        elif intent == 'date_query':
            return self._create_date_analysis(query, original_query)
        elif intent == 'ranking':
            return self._create_ranking_analysis(query, original_query)
        elif intent == 'energy_query':
            return self._create_energy_analysis(plants, original_query)
        elif intent == 'portfolio':
            return self._create_portfolio_analysis(original_query)
        else:
            return self._create_help_message(original_query)
    
    def _create_plant_analysis(self, plant_name: str, original_query: str) -> str:
        """Create clean plant analysis"""
        
        if not plant_name:
            return """💡 Please specify which plant you would like to analyze.

Example: 'Analyze AXPPL performance'"""
        
        plant_data = self.data_processor.get_plant_data(plant_name)
        if plant_data is None or plant_data.empty:
            return f"❌ No data available for {plant_name}. Please verify the plant name."
        
        # Clean header
        response = f"🏭 PLANT ANALYSIS: {plant_name.upper()}\n"
        response += "═" * 50 + "\n\n"
        
        # Data overview
        response += f"📊 DATA OVERVIEW\n"
        response += f"• Records Analyzed: {len(plant_data):,}\n"
        
        if 'Date' in plant_data.columns:
            start_date = plant_data['Date'].min().strftime('%B %Y')
            end_date = plant_data['Date'].max().strftime('%B %Y')
            response += f"• Analysis Period: {start_date} → {end_date}\n\n"
        
        # Energy performance
        if 'Mtr_Export (kWh)' in plant_data.columns:
            total_energy = plant_data['Mtr_Export (kWh)'].sum()
            avg_daily = plant_data['Mtr_Export (kWh)'].mean()
            max_daily = plant_data['Mtr_Export (kWh)'].max()
            
            response += f"⚡ ENERGY PERFORMANCE\n"
            response += f"• Total Generation: {total_energy:,.0f} kWh\n"
            response += f"• Daily Average: {avg_daily:,.0f} kWh\n"
            response += f"• Peak Daily Output: {max_daily:,.0f} kWh\n\n"
        
        # Operational metrics
        if 'PA(%)' in plant_data.columns:
            availability = plant_data['PA(%)'].mean()
            
            response += f"📈 OPERATIONAL METRICS\n"
            response += f"• Plant Availability: {availability:.2f}%\n"
            
            # Status assessment
            if availability > 95:
                status = "✅ EXCELLENT"
            elif availability > 85:
                status = "⚠️ GOOD"
            elif availability > 70:
                status = "🟡 FAIR"
            else:
                status = "🔴 POOR"
            
            response += f"• Operational Status: {status}\n"
        
        # Additional metrics
        if 'PR(%)' in plant_data.columns:
            performance = plant_data['PR(%)'].mean()
            if pd.notna(performance):
                response += f"• Performance Ratio: {performance:.2f}%\n"
        
        if 'CUF(%)' in plant_data.columns:
            capacity = plant_data['CUF(%)'].mean()
            if pd.notna(capacity):
                response += f"• Capacity Utilization: {capacity:.2f}%\n\n"
        
        # Plant type
        plant_type = self._classify_plant_type(plant_name, plant_data)
        response += f"🏷️ PLANT TYPE\n• Technology: {plant_type}\n\n"
        
        # Key insights
        response += f"💡 KEY INSIGHTS\n"
        
        if 'Mtr_Export (kWh)' in plant_data.columns and total_energy > 0:
            monthly_avg = (total_energy / len(plant_data)) * 30
            response += f"• Estimated monthly generation: {monthly_avg:,.0f} kWh\n"
        
        if 'PA(%)' in plant_data.columns:
            if availability > 95:
                response += f"• Outstanding operational performance\n"
            elif availability > 85:
                response += f"• Good performance with optimization potential\n"
            else:
                response += f"• Requires operational attention and maintenance\n"
        
        return response
    
    def _create_comparison_analysis(self, plants: List[str], original_query: str) -> str:
        """Create clean plant comparison"""
        
        if len(plants) < 2:
            all_plants = self.data_processor.get_available_plants()
            query_words = original_query.lower().split()
            
            found_plants = []
            for plant in all_plants:
                plant_parts = plant.lower().split('_')
                if any(part in query_words for part in plant_parts if len(part) > 2):
                    found_plants.append(plant)
            
            if len(found_plants) >= 2:
                plants = found_plants[:2]
            else:
                return """💡 Comparison requires at least two plant names.

Example: 'Compare CSPPL and PSEGPL performance'"""
        
        plant1, plant2 = plants[0], plants[1]
        
        # Clean header
        response = f"⚖️ PLANT COMPARISON\n"
        response += f"{plant1.upper()} vs {plant2.upper()}\n"
        response += "═" * 50 + "\n\n"
        
        # Get data for both plants
        data1 = self.data_processor.get_plant_data(plant1)
        data2 = self.data_processor.get_plant_data(plant2)
        
        if data1 is None or data1.empty:
            return f"❌ No data available for {plant1}"
        if data2 is None or data2.empty:
            return f"❌ No data available for {plant2}"
        
        # Energy generation comparison
        if 'Mtr_Export (kWh)' in data1.columns and 'Mtr_Export (kWh)' in data2.columns:
            energy1 = data1['Mtr_Export (kWh)'].sum()
            energy2 = data2['Mtr_Export (kWh)'].sum()
            
            response += f"⚡ ENERGY GENERATION\n"
            response += f"• {plant1}: {energy1:,.0f} kWh\n"
            response += f"• {plant2}: {energy2:,.0f} kWh\n\n"
            
            # Performance verdict
            if energy1 > energy2:
                diff_pct = ((energy1 - energy2) / energy2) * 100
                response += f"🏆 WINNER: {plant1.upper()}\n"
                response += f"• Advantage: {diff_pct:.1f}% higher generation\n"
                response += f"• Difference: {energy1-energy2:,.0f} kWh\n\n"
            else:
                diff_pct = ((energy2 - energy1) / energy1) * 100
                response += f"🏆 WINNER: {plant2.upper()}\n"
                response += f"• Advantage: {diff_pct:.1f}% higher generation\n"
                response += f"• Difference: {energy2-energy1:,.0f} kWh\n\n"
        
        # Availability comparison
        if 'PA(%)' in data1.columns and 'PA(%)' in data2.columns:
            avail1 = data1['PA(%)'].mean()
            avail2 = data2['PA(%)'].mean()
            
            response += f"📊 AVAILABILITY COMPARISON\n"
            response += f"• {plant1}: {avail1:.2f}%\n"
            response += f"• {plant2}: {avail2:.2f}%\n"
            
            if abs(avail1 - avail2) > 1:
                better_plant = plant1 if avail1 > avail2 else plant2
                response += f"• Better Availability: {better_plant.upper()}\n"
            else:
                response += f"• Status: Comparable performance\n"
        
        return response
    
    def _create_date_analysis(self, query: str, original_query: str) -> str:
        """Create clean date analysis"""
        
        target_date = self._extract_date_from_query(query)
        
        if not target_date:
            return """💡 Please specify a valid date for analysis.

Examples: 'June 12', 'yesterday', 'today'"""
        
        response = f"📅 DAILY GENERATION REPORT\n"
        response += f"{target_date.strftime('%A, %B %d, %Y')}\n"
        response += "═" * 50 + "\n\n"
        
        total_energy = 0
        plant_data_list = []
        
        for plant in self.data_processor.get_available_plants():
            plant_data = self.data_processor.get_plant_data(plant)
            
            if plant_data is not None and not plant_data.empty and 'Date' in plant_data.columns:
                day_data = plant_data[plant_data['Date'].dt.date == target_date]
                
                if not day_data.empty and 'Mtr_Export (kWh)' in day_data.columns:
                    day_energy = day_data['Mtr_Export (kWh)'].sum()
                    if pd.notna(day_energy) and day_energy > 0:
                        total_energy += day_energy
                        plant_data_list.append((plant, day_energy))
        
        if not plant_data_list:
            return f"""❌ No generation data available for {target_date.strftime('%B %d, %Y')}.

This date may be outside the available data range."""
        
        # Sort by energy generation
        plant_data_list.sort(key=lambda x: x[1], reverse=True)
        
        # Summary
        response += f"📊 PORTFOLIO SUMMARY\n"
        response += f"• Total Generation: {total_energy:,.0f} kWh\n"
        response += f"• Active Plants: {len(plant_data_list)}\n"
        response += f"• Average per Plant: {total_energy/len(plant_data_list):,.0f} kWh\n\n"
        
        response += f"🏆 TOP PERFORMERS\n"
        for i, (plant, energy) in enumerate(plant_data_list[:5], 1):
            percentage = (energy / total_energy) * 100 if total_energy > 0 else 0
            response += f"{i}. {plant}: {energy:,.0f} kWh ({percentage:.1f}%)\n"
        
        return response
    
    def _extract_date_from_query(self, query: str) -> Optional[datetime.date]:
        """Extract date from query"""
        today = datetime.now().date()
        
        if 'yesterday' in query:
            return today - timedelta(days=1)
        elif 'today' in query:
            return today
        elif 'june 12' in query or '12th june' in query or '12 june' in query:
            return datetime(2025, 6, 12).date()
        elif 'june 11' in query or '11th june' in query or '11 june' in query:
            return datetime(2025, 6, 11).date()
        elif 'june 6' in query or '6th june' in query or '6 june' in query:
            return datetime(2025, 6, 6).date()
        
        return None
    
    def _create_ranking_analysis(self, query: str, original_query: str) -> str:
        """Create clean ranking analysis"""
        
        plant_rankings = []
        
        for plant in self.data_processor.get_available_plants():
            plant_data = self.data_processor.get_plant_data(plant)
            if plant_data is not None and not plant_data.empty and 'Mtr_Export (kWh)' in plant_data.columns:
                total_energy = plant_data['Mtr_Export (kWh)'].sum()
                if pd.notna(total_energy):
                    plant_rankings.append((plant, total_energy))
        
        plant_rankings.sort(key=lambda x: x[1], reverse=True)
        
        # Determine ranking type
        if 'best' in query or 'top' in query or 'most' in query or 'highest' in query:
            response = "🏆 TOP PERFORMING PLANTS\n"
            plants_to_show = plant_rankings[:8]
        elif 'worst' in query or 'bottom' in query or 'least' in query or 'lowest' in query:
            response = "⚠️ UNDERPERFORMING PLANTS\n"
            plants_to_show = plant_rankings[-8:]
        else:
            response = "📊 COMPLETE PLANT RANKING\n"
            plants_to_show = plant_rankings
        
        response += "═" * 50 + "\n\n"
        
        # Create clean ranking
        for i, (plant, energy) in enumerate(plants_to_show, 1):
            response += f"{i}. {plant}: {energy:,.0f} kWh\n"
        
        return response
    
    def _create_energy_analysis(self, plants: List[str], original_query: str) -> str:
        """Create clean energy analysis"""
        
        if plants:
            total_energy = 0
            plant_energies = []
            
            for plant in plants:
                plant_data = self.data_processor.get_plant_data(plant)
                if plant_data is not None and not plant_data.empty and 'Mtr_Export (kWh)' in plant_data.columns:
                    energy = plant_data['Mtr_Export (kWh)'].sum()
                    if pd.notna(energy):
                        total_energy += energy
                        plant_energies.append((plant, energy))
            
            response = f"⚡ ENERGY GENERATION ANALYSIS\n"
            response += "═" * 50 + "\n\n"
            
            for plant, energy in plant_energies:
                response += f"• {plant}: {energy:,.0f} kWh\n"
            
            if len(plant_energies) > 1:
                response += f"\n📊 SUMMARY\n"
                response += f"• Combined Total: {total_energy:,.0f} kWh\n"
                response += f"• Average Generation: {total_energy/len(plant_energies):,.0f} kWh\n"
            
            return response
        
        else:
            return self._create_portfolio_analysis(original_query)
    
    def _create_portfolio_analysis(self, original_query: str) -> str:
        """Create clean portfolio overview"""
        
        total_energy = 0
        plant_count = 0
        plant_energies = []
        
        for plant in self.data_processor.get_available_plants():
            plant_data = self.data_processor.get_plant_data(plant)
            if plant_data is not None and not plant_data.empty:
                plant_count += 1
                if 'Mtr_Export (kWh)' in plant_data.columns:
                    energy = plant_data['Mtr_Export (kWh)'].sum()
                    if pd.notna(energy):
                        total_energy += energy
                        plant_energies.append((plant, energy))
        
        plant_energies.sort(key=lambda x: x[1], reverse=True)
        
        response = f"🏭 PORTFOLIO OVERVIEW\n"
        response += "═" * 50 + "\n\n"
        
        # Executive summary
        response += f"📊 EXECUTIVE SUMMARY\n"
        response += f"• Total Plants: {plant_count}\n"
        response += f"• Total Generation: {total_energy:,.0f} kWh\n"
        
        if plant_energies:
            avg_energy = total_energy / len(plant_energies)
            response += f"• Average per Plant: {avg_energy:,.0f} kWh\n\n"
            
            # Top performers
            response += f"🏆 TOP CONTRIBUTORS\n"
            for i, (plant, energy) in enumerate(plant_energies[:8], 1):
                percentage = (energy / total_energy) * 100
                response += f"{i}. {plant}: {energy:,.0f} kWh ({percentage:.1f}%)\n"
            
            # Performance distribution
            response += f"\n📈 PERFORMANCE DISTRIBUTION\n"
            
            q1_threshold = avg_energy * 0.5
            q2_threshold = avg_energy * 0.8
            q3_threshold = avg_energy * 1.2
            
            q1_count = sum(1 for _, energy in plant_energies if energy <= q1_threshold)
            q2_count = sum(1 for _, energy in plant_energies if q1_threshold < energy <= q2_threshold)
            q3_count = sum(1 for _, energy in plant_energies if q2_threshold < energy <= q3_threshold)
            q4_count = sum(1 for _, energy in plant_energies if energy > q3_threshold)
            
            response += f"• High Performers: {q4_count} plants\n"
            response += f"• Above Average: {q3_count} plants\n"
            response += f"• Below Average: {q2_count} plants\n"
            response += f"• Low Performers: {q1_count} plants\n"
        
        return response
    
    def _classify_plant_type(self, plant_name: str, data: pd.DataFrame) -> str:
        """Classify plant type"""
        name_lower = plant_name.lower()
        
        if 'wind' in name_lower:
            return "🌪️ Wind Power"
        elif any(term in name_lower for term in ['solar', 'pv']):
            return "☀️ Solar Power"
        elif any(term in name_lower for term in ['hydro', 'water']):
            return "💧 Hydroelectric"
        else:
            if 'WS_Avg(m/s)' in data.columns and data['WS_Avg(m/s)'].mean() > 0:
                return "🌪️ Wind Power"
            elif 'GHI-UP (KWh/m2)' in data.columns and data['GHI-UP (KWh/m2)'].mean() > 0:
                return "☀️ Solar Power"
            else:
                return "⚙️ Thermal/Conventional"
    
    def _create_help_message(self, original_query: str) -> str:
        """Create clean help message"""
        
        response = f"🤖 POWER PLANT AI ASSISTANT\n"
        response += "═" * 50 + "\n\n"
        
        response += f"💡 I can help you with:\n\n"
        
        response += f"📊 PLANT ANALYSIS\n"
        response += f"• Individual plant performance metrics\n"
        response += f"• Operational efficiency assessment\n"
        response += f"• Historical trend analysis\n\n"
        
        response += f"⚖️ PLANT COMPARISON\n"
        response += f"• Side-by-side performance analysis\n"
        response += f"• Efficiency benchmarking\n"
        response += f"• Head-to-head comparisons\n\n"
        
        response += f"📅 DATE ANALYSIS\n"
        response += f"• Daily generation reports\n"
        response += f"• Historical date analysis\n"
        response += f"• Time-specific performance\n\n"
        
        response += f"🏭 PORTFOLIO MANAGEMENT\n"
        response += f"• Complete portfolio overview\n"
        response += f"• Performance rankings\n"
        response += f"• Risk assessment metrics\n\n"
        
        response += f"🚀 SAMPLE QUERIES\n"
        response += f"• 'Analyze AXPPL performance'\n"
        response += f"• 'Compare CSPPL and PSEGPL'\n"
        response += f"• 'Generation report for June 12'\n"
        response += f"• 'Top performing plants'\n"
        response += f"• 'Portfolio overview'\n"
        
        return response

# Compatibility wrapper
class MainAISystem(CleanChatbot):
    """Wrapper for compatibility"""
    pass