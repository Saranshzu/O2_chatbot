"""
Enhanced KPI Assistant V2 - Deep Data Analysis & Intelligent Querying
Handles complex queries, time-based analysis, and detailed plant comparisons
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import json
from typing import Dict, List, Any, Optional, Tuple

class EnhancedKPIAssistantV2:
    def __init__(self, data_processor, advanced_analytics, smart_reporting):
        self.data_processor = data_processor
        self.analytics = advanced_analytics
        self.reporting = smart_reporting
        self.plant_data = data_processor.all_data if hasattr(data_processor, 'all_data') else {}
        
        # Enhanced query patterns for complex analysis
        self.query_patterns = {
            'time_comparison': [
                r'yesterday.*today', r'today.*yesterday', r'last week.*this week',
                r'previous.*current', r'compare.*(\w+day|\w+week|\w+month)',
                r'(\d+)\s*days?\s*ago.*today', r'last.*vs.*current'
            ],
            'plant_comparison': [
                r'compare\s+(\w+).*(\w+)', r'(\w+)\s+vs\s+(\w+)', 
                r'difference.*between.*(\w+).*(\w+)', r'which.*better.*(\w+).*(\w+)'
            ],
            'specific_date': [
                r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', r'(\d{4})-(\d{1,2})-(\d{1,2})',
                r'(january|february|march|april|may|june|july|august|september|october|november|december)\s*(\d{1,2})',
                r'(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
            ],
            'power_metrics': [
                r'power|energy|generation|output|production|kwh|mwh',
                r'export|import|consumption|load'
            ],
            'performance_metrics': [
                r'availability|performance.*ratio|pr|efficiency',
                r'downtime|uptime|operational'
            ],
            'trend_analysis': [
                r'trend|pattern|increase|decrease|improving|declining',
                r'forecast|predict|future|next.*week|next.*month'
            ]
        }
        
        # Initialize data analysis cache
        self.analysis_cache = {}
        self.last_query_context = {}

    def process_query(self, user_input: str) -> str:
        """Enhanced query processing with deep data analysis"""
        try:
            # Clean and normalize input
            query = user_input.lower().strip()
            
            # Determine query type and extract parameters
            query_type, params = self.analyze_query_intent(query)
            
            # Execute appropriate analysis
            if query_type == 'time_comparison':
                return self.handle_time_comparison(query, params)
            elif query_type == 'plant_comparison':
                return self.handle_plant_comparison(query, params)
            elif query_type == 'specific_data':
                return self.handle_specific_data_query(query, params)
            elif query_type == 'trend_analysis':
                return self.handle_trend_analysis(query, params)
            elif query_type == 'summary':
                return self.handle_summary_query(query, params)
            else:
                return self.handle_general_query(query)
                
        except Exception as e:
            return f"I encountered an error processing your query: {str(e)}. Could you please rephrase your question?"

    def analyze_query_intent(self, query: str) -> Tuple[str, Dict]:
        """Analyze user intent and extract relevant parameters"""
        params = {
            'plants': self.extract_plant_names(query),
            'dates': self.extract_dates(query),
            'metrics': self.extract_metrics(query),
            'time_periods': self.extract_time_periods(query)
        }
        
        # Determine primary intent
        if any(re.search(pattern, query) for pattern in self.query_patterns['time_comparison']):
            return 'time_comparison', params
        elif any(re.search(pattern, query) for pattern in self.query_patterns['plant_comparison']):
            return 'plant_comparison', params
        elif params['dates'] or 'specific' in query:
            return 'specific_data', params
        elif any(re.search(pattern, query) for pattern in self.query_patterns['trend_analysis']):
            return 'trend_analysis', params
        elif 'summary' in query or 'overview' in query:
            return 'summary', params
        else:
            return 'general', params

    def extract_plant_names(self, query: str) -> List[str]:
        """Extract plant names from query"""
        plants = []
        available_plants = list(self.plant_data.keys())
        
        for plant in available_plants:
            if plant.lower() in query:
                plants.append(plant)
        
        # Also check for plant patterns like "plant 1", "site a", etc.
        plant_patterns = re.findall(r'plant\s*(\w+)|site\s*(\w+)', query)
        for pattern in plant_patterns:
            plant_id = pattern[0] or pattern[1]
            matching_plants = [p for p in available_plants if plant_id.lower() in p.lower()]
            plants.extend(matching_plants)
        
        return list(set(plants))

    def extract_dates(self, query: str) -> List[datetime]:
        """Extract specific dates from query"""
        dates = []
        
        # Handle relative dates
        if 'yesterday' in query:
            dates.append(datetime.now() - timedelta(days=1))
        if 'today' in query:
            dates.append(datetime.now())
        if 'last week' in query:
            dates.append(datetime.now() - timedelta(weeks=1))
        
        # Handle specific date patterns
        for pattern in self.query_patterns['specific_date']:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                try:
                    if len(match) == 3:  # DD/MM/YYYY or YYYY-MM-DD
                        if len(match[0]) == 4:  # YYYY-MM-DD
                            date = datetime(int(match[0]), int(match[1]), int(match[2]))
                        else:  # DD/MM/YYYY
                            date = datetime(int(match[2]), int(match[1]), int(match[0]))
                        dates.append(date)
                except ValueError:
                    continue
        
        return dates

    def extract_metrics(self, query: str) -> List[str]:
        """Extract metrics of interest from query"""
        metrics = []
        
        if any(re.search(pattern, query) for pattern in self.query_patterns['power_metrics']):
            metrics.extend(['energy_export', 'energy_import', 'power_generation'])
        
        if any(re.search(pattern, query) for pattern in self.query_patterns['performance_metrics']):
            metrics.extend(['availability', 'performance_ratio'])
        
        # Specific metric mentions
        metric_mapping = {
            'availability': 'availability',
            'performance ratio': 'performance_ratio',
            'pr': 'performance_ratio',
            'power': 'power_generation',
            'energy': 'energy_export',
            'generation': 'power_generation',
            'export': 'energy_export',
            'import': 'energy_import'
        }
        
        for keyword, metric in metric_mapping.items():
            if keyword in query:
                metrics.append(metric)
        
        return list(set(metrics)) if metrics else ['energy_export', 'availability', 'performance_ratio']

    def extract_time_periods(self, query: str) -> Dict[str, Any]:
        """Extract time period information"""
        periods = {}
        
        # Days ago pattern
        days_match = re.search(r'(\d+)\s*days?\s*ago', query)
        if days_match:
            periods['days_ago'] = int(days_match.group(1))
        
        # Week/month patterns
        if 'week' in query:
            periods['period_type'] = 'week'
        elif 'month' in query:
            periods['period_type'] = 'month'
        elif 'day' in query:
            periods['period_type'] = 'day'
        
        return periods

    def handle_time_comparison(self, query: str, params: Dict) -> str:
        """Handle time-based comparisons"""
        try:
            plants = params['plants'] if params['plants'] else list(self.plant_data.keys())[:3]
            metrics = params['metrics']
            
            results = []
            
            for plant in plants:
                plant_result = self.get_time_comparison_data(plant, query, params)
                if plant_result:
                    results.append(plant_result)
            
            return self.format_time_comparison_response(results, query)
            
        except Exception as e:
            return f"Error analyzing time comparison: {str(e)}"

    def get_time_comparison_data(self, plant: str, query: str, params: Dict) -> Optional[Dict]:
        """Get time comparison data for a specific plant"""
        try:
            if plant not in self.plant_data:
                return None
            
            daily_data = self.plant_data[plant].get('daily_kpi')
            if daily_data is None or daily_data.empty:
                return None
            
            # Ensure Date column exists and is datetime
            if 'Date' not in daily_data.columns:
                return None
            
            daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
            daily_data = daily_data.dropna(subset=['Date']).sort_values('Date')
            
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            
            # Get today's and yesterday's data
            today_data = daily_data[daily_data['Date'].dt.date == today]
            yesterday_data = daily_data[daily_data['Date'].dt.date == yesterday]
            
            result = {
                'plant': plant,
                'today': self.extract_metrics_from_row(today_data, params['metrics']),
                'yesterday': self.extract_metrics_from_row(yesterday_data, params['metrics']),
                'comparison': {}
            }
            
            # Calculate comparisons
            for metric in params['metrics']:
                today_val = result['today'].get(metric, 0)
                yesterday_val = result['yesterday'].get(metric, 0)
                
                if yesterday_val > 0:
                    change_pct = ((today_val - yesterday_val) / yesterday_val) * 100
                    result['comparison'][metric] = {
                        'absolute_change': today_val - yesterday_val,
                        'percentage_change': change_pct,
                        'trend': 'increased' if change_pct > 0 else 'decreased' if change_pct < 0 else 'unchanged'
                    }
            
            return result
            
        except Exception as e:
            print(f"Error getting time comparison for {plant}: {str(e)}")
            return None

    def extract_metrics_from_row(self, data: pd.DataFrame, metrics: List[str]) -> Dict:
        """Extract specific metrics from data row"""
        result = {}
        
        if data.empty:
            return {metric: 0 for metric in metrics}
        
        # Use the most recent row if multiple rows
        row = data.iloc[-1]
        
        # Column mapping
        column_mapping = {
            'energy_export': ['Energy Export (kWh)', 'Export', 'Energy_Export', 'Total_Export'],
            'power_generation': ['Power Generation (kW)', 'Generation', 'Power', 'Total_Generation'],
            'availability': ['Availability (%)', 'Availability', 'Avail', 'Plant_Availability'],
            'performance_ratio': ['Performance Ratio (%)', 'PR', 'Performance_Ratio', 'PR_Actual'],
            'energy_import': ['Energy Import (kWh)', 'Import', 'Energy_Import']
        }
        
        for metric in metrics:
            value = 0
            if metric in column_mapping:
                for col_option in column_mapping[metric]:
                    if col_option in row.index:
                        try:
                            value = float(row[col_option]) if pd.notna(row[col_option]) else 0
                            break
                        except (ValueError, TypeError):
                            continue
            
            result[metric] = value
        
        return result

    def handle_plant_comparison(self, query: str, params: Dict) -> str:
        """Handle plant-to-plant comparisons"""
        try:
            plants = params['plants']
            if len(plants) < 2:
                # If not enough plants specified, get top performers for comparison
                plants = self.get_top_plants_for_comparison(2)
            
            metrics = params['metrics']
            comparison_data = {}
            
            for plant in plants[:5]:  # Limit to 5 plants for readability
                plant_data = self.get_plant_performance_summary(plant, days=7)
                if plant_data:
                    comparison_data[plant] = plant_data
            
            return self.format_plant_comparison_response(comparison_data, metrics, query)
            
        except Exception as e:
            return f"Error comparing plants: {str(e)}"

    def get_plant_performance_summary(self, plant: str, days: int = 7) -> Optional[Dict]:
        """Get comprehensive performance summary for a plant"""
        try:
            if plant not in self.plant_data:
                return None
            
            daily_data = self.plant_data[plant].get('daily_kpi')
            if daily_data is None or daily_data.empty:
                return None
            
            # Get recent data
            daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
            recent_data = daily_data.dropna(subset=['Date']).tail(days)
            
            if recent_data.empty:
                return None
            
            # Calculate comprehensive metrics
            result = {
                'total_energy_export': 0,
                'avg_availability': 0,
                'avg_performance_ratio': 0,
                'total_generation': 0,
                'data_points': len(recent_data),
                'date_range': {
                    'start': recent_data['Date'].min().strftime('%Y-%m-%d'),
                    'end': recent_data['Date'].max().strftime('%Y-%m-%d')
                }
            }
            
            # Column mapping for flexible column names
            column_maps = {
                'energy_export': ['Energy Export (kWh)', 'Export', 'Energy_Export', 'Total_Export'],
                'availability': ['Availability (%)', 'Availability', 'Avail', 'Plant_Availability'],
                'performance_ratio': ['Performance Ratio (%)', 'PR', 'Performance_Ratio', 'PR_Actual'],
                'generation': ['Power Generation (kW)', 'Generation', 'Power', 'Total_Generation']
            }
            
            # Calculate metrics
            for metric, col_options in column_maps.items():
                values = []
                for col in col_options:
                    if col in recent_data.columns:
                        values = recent_data[col].dropna()
                        break
                
                if len(values) > 0:
                    if metric == 'energy_export':
                        result['total_energy_export'] = values.sum()
                    elif metric == 'availability':
                        result['avg_availability'] = values.mean()
                    elif metric == 'performance_ratio':
                        result['avg_performance_ratio'] = values.mean()
                    elif metric == 'generation':
                        result['total_generation'] = values.sum()
            
            return result
            
        except Exception as e:
            print(f"Error getting plant summary for {plant}: {str(e)}")
            return None

    def get_top_plants_for_comparison(self, count: int) -> List[str]:
        """Get top performing plants for comparison"""
        plant_rankings = []
        
        for plant in self.plant_data.keys():
            summary = self.get_plant_performance_summary(plant)
            if summary:
                # Score based on availability and performance ratio
                score = (summary['avg_availability'] + summary['avg_performance_ratio']) / 2
                plant_rankings.append((plant, score))
        
        # Sort by score and return top plants
        plant_rankings.sort(key=lambda x: x[1], reverse=True)
        return [plant for plant, _ in plant_rankings[:count]]

    def handle_specific_data_query(self, query: str, params: Dict) -> str:
        """Handle queries for specific data points"""
        try:
            plants = params['plants'] if params['plants'] else list(self.plant_data.keys())[:3]
            dates = params['dates']
            metrics = params['metrics']
            
            results = {}
            
            for plant in plants:
                plant_results = self.get_specific_date_data(plant, dates, metrics)
                if plant_results:
                    results[plant] = plant_results
            
            return self.format_specific_data_response(results, query)
            
        except Exception as e:
            return f"Error retrieving specific data: {str(e)}"

    def get_specific_date_data(self, plant: str, dates: List[datetime], metrics: List[str]) -> Optional[Dict]:
        """Get data for specific dates"""
        try:
            if plant not in self.plant_data:
                return None
            
            daily_data = self.plant_data[plant].get('daily_kpi')
            if daily_data is None or daily_data.empty:
                return None
            
            daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
            
            result = {}
            for date in dates:
                date_data = daily_data[daily_data['Date'].dt.date == date.date()]
                if not date_data.empty:
                    result[date.strftime('%Y-%m-%d')] = self.extract_metrics_from_row(date_data, metrics)
            
            return result
            
        except Exception as e:
            print(f"Error getting specific date data for {plant}: {str(e)}")
            return None

    def handle_trend_analysis(self, query: str, params: Dict) -> str:
        """Handle trend analysis queries"""
        try:
            plants = params['plants'] if params['plants'] else list(self.plant_data.keys())[:3]
            metrics = params['metrics']
            
            trend_results = {}
            
            for plant in plants:
                plant_trends = self.analyze_plant_trends(plant, metrics, days=30)
                if plant_trends:
                    trend_results[plant] = plant_trends
            
            return self.format_trend_analysis_response(trend_results, query)
            
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"

    def analyze_plant_trends(self, plant: str, metrics: List[str], days: int = 30) -> Optional[Dict]:
        """Analyze trends for a specific plant"""
        try:
            if plant not in self.plant_data:
                return None
            
            daily_data = self.plant_data[plant].get('daily_kpi')
            if daily_data is None or daily_data.empty:
                return None
            
            daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
            recent_data = daily_data.dropna(subset=['Date']).tail(days)
            
            trends = {}
            
            for metric in metrics:
                metric_data = self.get_metric_series(recent_data, metric)
                if len(metric_data) > 5:  # Need sufficient data points
                    trend_analysis = self.calculate_trend(metric_data)
                    trends[metric] = trend_analysis
            
            return trends
            
        except Exception as e:
            print(f"Error analyzing trends for {plant}: {str(e)}")
            return None

    def get_metric_series(self, data: pd.DataFrame, metric: str) -> pd.Series:
        """Get time series data for a specific metric"""
        column_mapping = {
            'energy_export': ['Energy Export (kWh)', 'Export', 'Energy_Export'],
            'availability': ['Availability (%)', 'Availability', 'Avail'],
            'performance_ratio': ['Performance Ratio (%)', 'PR', 'Performance_Ratio']
        }
        
        if metric in column_mapping:
            for col in column_mapping[metric]:
                if col in data.columns:
                    return data[col].dropna()
        
        return pd.Series()

    def calculate_trend(self, series: pd.Series) -> Dict:
        """Calculate trend statistics"""
        if len(series) < 2:
            return {'trend': 'insufficient_data'}
        
        # Calculate basic trend
        first_half = series[:len(series)//2].mean()
        second_half = series[len(series)//2:].mean()
        
        trend_direction = 'increasing' if second_half > first_half else 'decreasing' if second_half < first_half else 'stable'
        trend_magnitude = abs((second_half - first_half) / first_half * 100) if first_half > 0 else 0
        
        return {
            'trend': trend_direction,
            'magnitude_percent': round(trend_magnitude, 2),
            'current_average': round(second_half, 2),
            'previous_average': round(first_half, 2),
            'min_value': round(series.min(), 2),
            'max_value': round(series.max(), 2),
            'std_deviation': round(series.std(), 2)
        }

    def handle_summary_query(self, query: str, params: Dict) -> str:
        """Handle summary and overview queries"""
        try:
            # Get executive summary using existing reporting
            exec_summary = self.reporting.generate_executive_summary(days=30)
            
            if 'error' in exec_summary:
                return "Unable to generate executive summary at this time. Please try again."
            
            return self.format_executive_summary(exec_summary)
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def handle_general_query(self, query: str) -> str:
        """Handle general queries that don't fit specific patterns"""
        try:
            # Try to find relevant plants and metrics
            plants = self.extract_plant_names(query)
            metrics = self.extract_metrics(query)
            
            if not plants:
                plants = list(self.plant_data.keys())[:3]
            
            # Generate a general analysis
            results = {}
            for plant in plants[:3]:
                plant_summary = self.get_plant_performance_summary(plant, days=7)
                if plant_summary:
                    results[plant] = plant_summary
            
            return self.format_general_response(results, query)
            
        except Exception as e:
            return f"I'm having trouble understanding your query. Could you please be more specific? Error: {str(e)}"

    # Response Formatting Methods
    
    def format_time_comparison_response(self, results: List[Dict], query: str) -> str:
        """Format time comparison results"""
        if not results:
            return "I couldn't find sufficient data for the time comparison you requested."
        
        response = "**Time Comparison Analysis:**\n\n"
        
        for result in results:
            plant = result['plant']
            response += f"**{plant}:**\n"
            
            for metric, comparison in result['comparison'].items():
                today_val = result['today'].get(metric, 0)
                yesterday_val = result['yesterday'].get(metric, 0)
                
                if metric == 'energy_export':
                    response += f"• Energy Export: Today {today_val:,.0f} kWh vs Yesterday {yesterday_val:,.0f} kWh\n"
                elif metric == 'availability':
                    response += f"• Availability: Today {today_val:.1f}% vs Yesterday {yesterday_val:.1f}%\n"
                elif metric == 'performance_ratio':
                    response += f"• Performance Ratio: Today {today_val:.1f}% vs Yesterday {yesterday_val:.1f}%\n"
                
                change = comparison.get('percentage_change', 0)
                trend = comparison.get('trend', 'unchanged')
                
                if abs(change) > 0.1:
                    response += f"  → {trend.title()} by {abs(change):.1f}%\n"
                else:
                    response += f"  → Relatively unchanged\n"
            
            response += "\n"
        
        return response

    def format_plant_comparison_response(self, comparison_data: Dict, metrics: List[str], query: str) -> str:
        """Format plant comparison results"""
        if not comparison_data:
            return "I couldn't find sufficient data for plant comparison."
        
        response = "**Plant Performance Comparison (Last 7 Days):**\n\n"
        
        # Create comparison table
        plants = list(comparison_data.keys())
        
        response += "| Plant | Energy Export (kWh) | Availability (%) | Performance Ratio (%) |\n"
        response += "|-------|-------------------|-----------------|---------------------|\n"
        
        for plant in plants:
            data = comparison_data[plant]
            response += f"| {plant} | {data['total_energy_export']:,.0f} | {data['avg_availability']:.1f} | {data['avg_performance_ratio']:.1f} |\n"
        
        # Add insights
        response += "\n**Key Insights:**\n"
        
        # Find best performers
        best_energy = max(plants, key=lambda p: comparison_data[p]['total_energy_export'])
        best_availability = max(plants, key=lambda p: comparison_data[p]['avg_availability'])
        best_pr = max(plants, key=lambda p: comparison_data[p]['avg_performance_ratio'])
        
        response += f"• Highest Energy Export: {best_energy} ({comparison_data[best_energy]['total_energy_export']:,.0f} kWh)\n"
        response += f"• Best Availability: {best_availability} ({comparison_data[best_availability]['avg_availability']:.1f}%)\n"
        response += f"• Best Performance Ratio: {best_pr} ({comparison_data[best_pr]['avg_performance_ratio']:.1f}%)\n"
        
        return response

    def format_specific_data_response(self, results: Dict, query: str) -> str:
        """Format specific data query results"""
        if not results:
            return "I couldn't find the specific data you requested."
        
        response = "**Specific Data Results:**\n\n"
        
        for plant, plant_data in results.items():
            response += f"**{plant}:**\n"
            
            for date, metrics in plant_data.items():
                response += f"• {date}:\n"
                for metric, value in metrics.items():
                    if metric == 'energy_export':
                        response += f"  - Energy Export: {value:,.0f} kWh\n"
                    elif metric == 'availability':
                        response += f"  - Availability: {value:.1f}%\n"
                    elif metric == 'performance_ratio':
                        response += f"  - Performance Ratio: {value:.1f}%\n"
            
            response += "\n"
        
        return response

    def format_trend_analysis_response(self, trend_results: Dict, query: str) -> str:
        """Format trend analysis results"""
        if not trend_results:
            return "I couldn't perform trend analysis with the available data."
        
        response = "**Trend Analysis (Last 30 Days):**\n\n"
        
        for plant, trends in trend_results.items():
            response += f"**{plant}:**\n"
            
            for metric, trend_data in trends.items():
                trend = trend_data.get('trend', 'unknown')
                magnitude = trend_data.get('magnitude_percent', 0)
                current = trend_data.get('current_average', 0)
                
                if metric == 'energy_export':
                    response += f"• Energy Export: {trend} trend"
                elif metric == 'availability':
                    response += f"• Availability: {trend} trend"
                elif metric == 'performance_ratio':
                    response += f"• Performance Ratio: {trend} trend"
                
                if magnitude > 1:
                    response += f" ({magnitude:.1f}% change)\n"
                    response += f"  Current average: {current:.1f}\n"
                else:
                    response += f" (stable)\n"
            
            response += "\n"
        
        return response

    def format_executive_summary(self, exec_summary: Dict) -> str:
        """Format executive summary"""
        try:
            portfolio_metrics = exec_summary.get('portfolio_metrics', {})
            
            response = "**Executive Portfolio Summary:**\n\n"
            response += f"• Total Energy Export: {portfolio_metrics.get('total_energy_export', 0):,.0f} kWh\n"
            response += f"• Portfolio Availability: {portfolio_metrics.get('portfolio_availability', 0):.1f}%\n"
            response += f"• Portfolio Performance Ratio: {portfolio_metrics.get('portfolio_performance_ratio', 0):.1f}%\n"
            response += f"• Operational Plants: {portfolio_metrics.get('operational_plants', 0)}/{portfolio_metrics.get('total_plants', 0)}\n\n"
            
            # Add key insights if available
            insights = exec_summary.get('key_insights', [])
            if insights:
                response += "**Key Insights:**\n"
                for insight in insights[:3]:
                    response += f"• {insight}\n"
            
            return response
            
        except Exception as e:
            return f"Error formatting executive summary: {str(e)}"

    def format_general_response(self, results: Dict, query: str) -> str:
        """Format general query response"""
        if not results:
            return "I couldn't find relevant data for your query. Please try being more specific."
        
        response = "**Performance Overview:**\n\n"
        
        for plant, data in results.items():
            response += f"**{plant}** (Last 7 days):\n"
            response += f"• Energy Export: {data['total_energy_export']:,.0f} kWh\n"
            response += f"• Availability: {data['avg_availability']:.1f}%\n"
            response += f"• Performance Ratio: {data['avg_performance_ratio']:.1f}%\n"
            response += f"• Data Points: {data['data_points']} days\n\n"
        
        return response

    def get_available_plants(self) -> List[str]:
        """Get list of all available plants"""
        return list(self.plant_data.keys())

    def get_available_metrics(self, plant: str) -> List[str]:
        """Get available metrics for a specific plant"""
        if plant not in self.plant_data:
            return []
        
        daily_data = self.plant_data[plant].get('daily_kpi')
        if daily_data is None or daily_data.empty:
            return []
        
        return list(daily_data.columns)

    def get_date_range(self, plant: str) -> Dict[str, str]:
        """Get available date range for a plant"""
        if plant not in self.plant_data:
            return {}
        
        daily_data = self.plant_data[plant].get('daily_kpi')
        if daily_data is None or daily_data.empty:
            return {}
        
        try:
            daily_data['Date'] = pd.to_datetime(daily_data['Date'], errors='coerce')
            date_data = daily_data.dropna(subset=['Date'])
            
            return {
                'start_date': date_data['Date'].min().strftime('%Y-%m-%d'),
                'end_date': date_data['Date'].max().strftime('%Y-%m-%d'),
                'total_days': len(date_data)
            }
        except Exception:
            return {}

    def debug_plant_data_structure(self, plant: str) -> str:
        """Debug method to understand plant data structure"""
        if plant not in self.plant_data:
            return f"Plant '{plant}' not found. Available plants: {list(self.plant_data.keys())}"
        
        plant_info = self.plant_data[plant]
        
        debug_info = f"**Data Structure for {plant}:**\n\n"
        
        for sheet_name, sheet_data in plant_info.items():
            debug_info += f"**{sheet_name}:**\n"
            
            if isinstance(sheet_data, pd.DataFrame):
                debug_info += f"• Rows: {len(sheet_data)}\n"
                debug_info += f"• Columns: {list(sheet_data.columns)}\n"
                
                if len(sheet_data) > 0:
                    debug_info += f"• Sample data:\n"
                    debug_info += f"{sheet_data.head(2).to_string()}\n"
                
                debug_info += "\n"
            else:
                debug_info += f"• Type: {type(sheet_data)}\n\n"
        
        return debug_info


class DataAnalysisHelper:
    """Helper class for advanced data analysis operations"""
    
    @staticmethod
    def calculate_daily_differences(series: pd.Series) -> pd.Series:
        """Calculate day-over-day differences"""
        return series.diff()
    
    @staticmethod
    def calculate_moving_average(series: pd.Series, window: int = 7) -> pd.Series:
        """Calculate moving average"""
        return series.rolling(window=window, min_periods=1).mean()
    
    @staticmethod
    def detect_outliers(series: pd.Series, method: str = 'iqr') -> pd.Series:
        """Detect outliers using IQR or Z-score method"""
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (series < lower_bound) | (series > upper_bound)
        elif method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > 3
        
        return pd.Series([False] * len(series))
    
    @staticmethod
    def calculate_efficiency_score(availability: float, performance_ratio: float, 
                                 energy_export: float, benchmark_export: float = 100000) -> float:
        """Calculate overall efficiency score"""
        availability_score = min(availability / 100, 1.0)
        pr_score = min(performance_ratio / 100, 1.0)
        energy_score = min(energy_export / benchmark_export, 1.0)
        
        # Weighted average
        return (availability_score * 0.4 + pr_score * 0.4 + energy_score * 0.2) * 100


def create_enhanced_assistant(data_processor, advanced_analytics, smart_reporting):
    """Factory function to create enhanced assistant"""
    return EnhancedKPIAssistantV2(data_processor, advanced_analytics, smart_reporting)


# Example usage and testing functions
def test_enhanced_assistant():
    """Test function for the enhanced assistant"""
    # This would be called with actual data processor, analytics, and reporting instances
    print("Enhanced KPI Assistant V2 - Test Suite")
    print("=" * 50)
    
    test_queries = [
        "What was yesterday's power compared to today's power for Plant1?",
        "Compare Plant1 vs Plant2 performance this week",
        "Show me availability trends for the last month",
        "Which plant performed better yesterday - Plant1 or Plant2?",
        "What was the energy export on 2024-01-15?",
        "How is Plant1 trending compared to last week?",
        "Give me an executive summary",
        "Compare all plants by availability this month"
    ]
    
    print("Supported Query Types:")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    
    print("\nEnhanced Features:")
    print("• Deep Excel data analysis - entire sheets processed")
    print("• Time-based comparisons (yesterday vs today, week over week)")
    print("• Plant-to-plant detailed comparisons")
    print("• Specific date queries with exact data retrieval")
    print("• Trend analysis with statistical insights")
    print("• Smart metric extraction from natural language")
    print("• Flexible column name handling for different Excel formats")
    print("• Comprehensive error handling and data validation")


if __name__ == "__main__":
    test_enhanced_assistant()