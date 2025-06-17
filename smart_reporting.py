"""
Smart Reporting Engine - Day 3
Automated report generation with executive summaries, alerts, and insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional

class SmartReporting:
    """
    Smart Reporting Engine for automated business intelligence reports
    """
    
    def __init__(self, data_processor, advanced_analytics):
        self.data_processor = data_processor
        self.analytics = advanced_analytics
        self.logger = logging.getLogger(__name__)
        
        # Alert thresholds
        self.alert_thresholds = {
            'critical': {
                'availability': 90,
                'performance_ratio': 70,
                'data_completeness': 70
            },
            'warning': {
                'availability': 95,
                'performance_ratio': 80,
                'data_completeness': 85
            }
        }
    
    def generate_executive_summary(self, plants: List[str] = None, days: int = 30) -> Dict:
        """Generate executive-level summary report"""
        try:
            if plants is None:
                plants = self.data_processor.get_available_plants()
            
            if not plants:
                return {"error": "No plants available for reporting"}
            
            portfolio_metrics = self._calculate_portfolio_metrics(plants, days)
            highlights = self._generate_performance_highlights(plants, days)
            alerts = self._generate_portfolio_alerts(plants)
            recommendations = self._generate_executive_recommendations(portfolio_metrics, alerts)
            
            return {
                "report_type": "Executive Summary",
                "reporting_period": f"Last {days} days",
                "total_plants": len(plants),
                "portfolio_metrics": portfolio_metrics,
                "performance_highlights": highlights,
                "key_alerts": alerts,
                "strategic_recommendations": recommendations,
                "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "next_review": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {str(e)}")
            return {"error": f"Report generation failed: {str(e)}"}
    
    def _calculate_portfolio_metrics(self, plants: List[str], days: int) -> Dict:
        """Calculate high-level portfolio KPIs"""
        total_export = 0
        availability_scores = []
        pr_scores = []
        data_quality_scores = []
        operational_plants = 0
        
        for plant in plants:
            try:
                summary = self.data_processor.get_plant_summary(plant, days=days)
                if summary and summary.get('total_days', 0) > 0:
                    operational_plants += 1
                    total_export += summary.get('total_export', 0)
                    
                    if summary.get('avg_availability', 0) > 0:
                        availability_scores.append(summary['avg_availability'])
                    if summary.get('avg_performance_ratio', 0) > 0:
                        pr_scores.append(summary['avg_performance_ratio'])
                    if summary.get('data_completeness_pct', 0) > 0:
                        data_quality_scores.append(summary['data_completeness_pct'])
                        
            except Exception as e:
                self.logger.warning(f"Failed to get summary for {plant}: {str(e)}")
                continue
        
        portfolio_availability = np.mean(availability_scores) if availability_scores else 0
        portfolio_pr = np.mean(pr_scores) if pr_scores else 0
        portfolio_data_quality = np.mean(data_quality_scores) if data_quality_scores else 0
        
        return {
            "total_energy_export": round(total_export, 0),
            "operational_plants": operational_plants,
            "total_plants": len(plants),
            "operational_rate": round((operational_plants / len(plants)) * 100, 1),
            "portfolio_availability": round(portfolio_availability, 1),
            "portfolio_performance_ratio": round(portfolio_pr, 1),
            "portfolio_data_quality": round(portfolio_data_quality, 1),
            "avg_daily_export": round(total_export / max(days, 1), 0) if total_export > 0 else 0
        }
    
    def _generate_performance_highlights(self, plants: List[str], days: int) -> Dict:
        """Generate performance highlights and rankings"""
        plant_performances = []
        
        for plant in plants:
            try:
                summary = self.data_processor.get_plant_summary(plant, days=days)
                if summary and summary.get('total_days', 0) > 0:
                    plant_performances.append({
                        "plant": plant,
                        "export": summary.get('total_export', 0),
                        "availability": summary.get('avg_availability', 0),
                        "performance_ratio": summary.get('avg_performance_ratio', 0),
                        "data_quality": summary.get('data_completeness_pct', 0)
                    })
            except Exception:
                continue
        
        if not plant_performances:
            return {"error": "No performance data available"}
        
        top_by_export = sorted(plant_performances, key=lambda x: x['export'], reverse=True)[:3]
        top_by_availability = sorted(plant_performances, key=lambda x: x['availability'], reverse=True)[:3]
        bottom_performers = sorted(plant_performances, key=lambda x: x['availability'])[:3]
        
        return {
            "top_energy_producers": [{"plant": p["plant"], "export_kwh": p["export"]} for p in top_by_export],
            "highest_availability": [{"plant": p["plant"], "availability_pct": p["availability"]} for p in top_by_availability],
            "needs_attention": [{"plant": p["plant"], "availability_pct": p["availability"], "reason": "Low availability"} for p in bottom_performers]
        }
    
    def _generate_portfolio_alerts(self, plants: List[str]) -> Dict:
        """Generate critical and warning alerts across portfolio"""
        critical_alerts = []
        warning_alerts = []
        info_alerts = []
        
        for plant in plants:
            try:
                summary = self.data_processor.get_plant_summary(plant, days=7)
                if not summary or summary.get('total_days', 0) == 0:
                    info_alerts.append({
                        "plant": plant,
                        "type": "No Data",
                        "message": "No recent data available",
                        "severity": "info"
                    })
                    continue
                
                availability = summary.get('avg_availability', 0)
                pr = summary.get('avg_performance_ratio', 0)
                data_quality = summary.get('data_completeness_pct', 0)
                
                # Critical alerts
                if availability < self.alert_thresholds['critical']['availability']:
                    critical_alerts.append({
                        "plant": plant,
                        "type": "Low Availability",
                        "message": f"Availability {availability:.1f}% (Critical: <{self.alert_thresholds['critical']['availability']}%)",
                        "severity": "critical",
                        "value": availability
                    })
                
                if pr < self.alert_thresholds['critical']['performance_ratio']:
                    critical_alerts.append({
                        "plant": plant,
                        "type": "Low Performance",
                        "message": f"Performance Ratio {pr:.1f}% (Critical: <{self.alert_thresholds['critical']['performance_ratio']}%)",
                        "severity": "critical",
                        "value": pr
                    })
                
                # Warning alerts
                elif availability < self.alert_thresholds['warning']['availability']:
                    warning_alerts.append({
                        "plant": plant,
                        "type": "Availability Warning",
                        "message": f"Availability {availability:.1f}% (Warning: <{self.alert_thresholds['warning']['availability']}%)",
                        "severity": "warning",
                        "value": availability
                    })
                
                elif pr < self.alert_thresholds['warning']['performance_ratio']:
                    warning_alerts.append({
                        "plant": plant,
                        "type": "Performance Warning",
                        "message": f"Performance Ratio {pr:.1f}% (Warning: <{self.alert_thresholds['warning']['performance_ratio']}%)",
                        "severity": "warning",
                        "value": pr
                    })
                
            except Exception as e:
                info_alerts.append({
                    "plant": plant,
                    "type": "System Error",
                    "message": f"Unable to analyze: {str(e)}",
                    "severity": "info"
                })
        
        alert_summary = self._generate_alert_summary(critical_alerts, warning_alerts, info_alerts)
        
        return {
            "critical_count": len(critical_alerts),
            "warning_count": len(warning_alerts),
            "info_count": len(info_alerts),
            "critical_alerts": critical_alerts[:5],
            "warning_alerts": warning_alerts[:5],
            "info_alerts": info_alerts[:3],
            "alert_summary": alert_summary
        }
    
    def _generate_alert_summary(self, critical: List, warning: List, info: List) -> str:
        """Generate human-readable alert summary"""
        if len(critical) > 0:
            return f"🚨 {len(critical)} critical issues require immediate attention"
        elif len(warning) > 5:
            return f"⚠️ {len(warning)} plants need monitoring and potential intervention"
        elif len(warning) > 0:
            return f"⚠️ {len(warning)} minor issues detected - preventive action recommended"
        elif len(critical) == 0 and len(warning) == 0:
            return "✅ All plants operating within normal parameters"
        else:
            return f"ℹ️ {len(info)} informational items noted"
    
    def _generate_executive_recommendations(self, portfolio_metrics: Dict, alerts: Dict) -> List[str]:
        """Generate strategic recommendations for executives"""
        recommendations = []
        
        # Portfolio performance recommendations
        if portfolio_metrics.get('operational_rate', 0) < 90:
            recommendations.append("🏭 Portfolio Optimization: Review non-operational plants and develop reactivation plan")
        
        if portfolio_metrics.get('portfolio_availability', 0) < 95:
            recommendations.append("🔧 Maintenance Strategy: Implement predictive maintenance program to improve availability")
        
        if portfolio_metrics.get('portfolio_performance_ratio', 0) < 80:
            recommendations.append("⚡ Performance Enhancement: Conduct technical review of underperforming assets")
        
        if portfolio_metrics.get('portfolio_data_quality', 0) < 85:
            recommendations.append("📊 Data Infrastructure: Invest in monitoring system upgrades and data quality initiatives")
        
        # Alert-based recommendations
        critical_count = alerts.get('critical_count', 0)
        warning_count = alerts.get('warning_count', 0)
        
        if critical_count > 3:
            recommendations.append("🚨 Emergency Response: Deploy technical teams to address critical performance issues")
        elif critical_count > 0:
            recommendations.append("🔧 Urgent Intervention: Prioritize resolution of critical plant issues")
        
        if warning_count > 5:
            recommendations.append("📈 Performance Review: Conduct quarterly performance assessment for flagged plants")
        
        # Strategic recommendations
        if portfolio_metrics.get('avg_daily_export', 0) > 0:
            recommendations.append("💰 Revenue Optimization: Analyze peak performance periods to maximize energy trading")
        
        if not recommendations:
            recommendations.append("✅ Continue Excellence: Portfolio performing well - maintain current operational standards")
        
        return recommendations
    
    def generate_plant_detailed_report(self, plant_name: str, days: int = 30) -> Dict:
        """Generate detailed technical report for a specific plant"""
        try:
            # Basic plant summary
            summary = self.data_processor.get_plant_summary(plant_name, days=days)
            if not summary:
                return {"error": f"No data available for {plant_name}"}
            
            # Try to get advanced analytics (may fail if dependencies missing)
            trends = {}
            predictions = {}
            benchmark = {}
            anomalies = {}
            
            try:
                trends = self.analytics.generate_trend_analysis(plant_name, days)
            except Exception as e:
                trends = {"error": f"Trend analysis failed: {str(e)}"}
            
            try:
                predictions = self.analytics.predict_performance(plant_name, days_ahead=7)
            except Exception as e:
                predictions = {"error": f"Prediction failed: {str(e)}"}
            
            try:
                benchmark = self.analytics.benchmark_performance(plant_name)
            except Exception as e:
                benchmark = {"error": f"Benchmarking failed: {str(e)}"}
            
            try:
                anomalies = self.analytics.detect_anomalies(plant_name, days)
            except Exception as e:
                anomalies = {"error": f"Anomaly detection failed: {str(e)}"}
            
            # Maintenance recommendations
            maintenance_rec = self._generate_maintenance_recommendations(summary, anomalies, benchmark)
            
            return {
                "plant_name": plant_name,
                "report_type": "Detailed Plant Analysis",
                "reporting_period": f"Last {days} days",
                "plant_summary": summary,
                "trend_analysis": trends,
                "performance_predictions": predictions,
                "benchmark_analysis": benchmark,
                "anomaly_detection": anomalies,
                "maintenance_recommendations": maintenance_rec,
                "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating detailed report for {plant_name}: {str(e)}")
            return {"error": f"Detailed report generation failed: {str(e)}"}
    
    def _generate_maintenance_recommendations(self, summary: Dict, anomalies: Dict, benchmark: Dict) -> Dict:
        """Generate specific maintenance recommendations"""
        recommendations = {
            "immediate_actions": [],
            "preventive_actions": [],
            "optimization_opportunities": [],
            "priority_level": "low"
        }
        
        # Check availability issues
        availability = summary.get('avg_availability', 0)
        if availability < 90:
            recommendations["immediate_actions"].append("Investigate equipment downtime and failure modes")
            recommendations["priority_level"] = "high"
        elif availability < 95:
            recommendations["preventive_actions"].append("Schedule preventive maintenance review")
            if recommendations["priority_level"] == "low":
                recommendations["priority_level"] = "medium"
        
        # Check performance issues
        pr = summary.get('avg_performance_ratio', 0)
        if pr < 75:
            recommendations["immediate_actions"].append("Perform inverter efficiency analysis and module cleaning")
            recommendations["priority_level"] = "high"
        elif pr < 85:
            recommendations["preventive_actions"].append("Schedule module soiling assessment")
        
        # Anomaly-based recommendations
        if anomalies and not anomalies.get('error'):
            severity = anomalies.get('severity_analysis', {}).get('overall_severity', 'None')
            if severity == 'High':
                recommendations["immediate_actions"].append("Investigate detected performance anomalies")
                recommendations["priority_level"] = "high"
            elif severity == 'Medium':
                recommendations["preventive_actions"].append("Monitor anomaly patterns closely")
        
        # Benchmark-based recommendations
        if benchmark and not benchmark.get('error'):
            grade = benchmark.get('overall_grade', {}).get('grade', 'C')
            if grade in ['D', 'C']:
                recommendations["optimization_opportunities"].append("Consider performance optimization program")
            
            bench_recs = benchmark.get('recommendations', [])
            recommendations["optimization_opportunities"].extend(bench_recs[:3])
        
        # Add general recommendations if no specific issues
        if not any([recommendations["immediate_actions"], recommendations["preventive_actions"]]):
            recommendations["preventive_actions"].append("Continue routine maintenance schedule")
            recommendations["optimization_opportunities"].append("Monitor industry best practices for efficiency improvements")
        
        return recommendations
    
    def generate_weekly_digest(self, plants: List[str] = None) -> Dict:
        """Generate weekly performance digest email/report"""
        try:
            if plants is None:
                plants = self.data_processor.get_available_plants()
            
            # This week vs last week comparison
            this_week = self._get_weekly_summary(plants, 0)  # Current week
            last_week = self._get_weekly_summary(plants, 1)  # Previous week
            
            # Key changes
            week_over_week = self._calculate_week_over_week_changes(this_week, last_week)
            
            # Top stories
            top_stories = self._generate_top_stories(plants, week_over_week)
            
            # Action items
            action_items = self._generate_weekly_action_items(plants)
            
            return {
                "digest_type": "Weekly Performance Digest",
                "week_ending": datetime.now().strftime("%Y-%m-%d"),
                "this_week_summary": this_week,
                "last_week_summary": last_week,
                "week_over_week_changes": week_over_week,
                "top_stories": top_stories,
                "action_items": action_items,
                "plants_covered": len(plants),
                "digest_generated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
        except Exception as e:
            self.logger.error(f"Error generating weekly digest: {str(e)}")
            return {"error": f"Weekly digest generation failed: {str(e)}"}
    
    def _get_weekly_summary(self, plants: List[str], weeks_ago: int) -> Dict:
        """Get weekly summary for specified week"""
        end_date = datetime.now().date() - timedelta(weeks=weeks_ago)
        start_date = end_date - timedelta(days=7)
        
        total_export = 0
        operational_count = 0
        availability_sum = 0
        pr_sum = 0
        
        for plant in plants:
            try:
                plant_data = self.data_processor.get_plant_data(plant)
                if plant_data is not None and not plant_data.empty:
                    filtered_data = self.data_processor.filter_by_date_range(plant_data, start_date, end_date)
                    if len(filtered_data) > 0:
                        operational_count += 1
                        cleaned_data = self.data_processor.clean_data(filtered_data)
                        
                        if 'Mtr_Export (kWh)' in cleaned_data.columns:
                            total_export += cleaned_data['Mtr_Export (kWh)'].sum()
                        if 'PA(%)' in cleaned_data.columns:
                            availability_sum += cleaned_data['PA(%)'].mean()
                        if 'PR(%)' in cleaned_data.columns:
                            pr_sum += cleaned_data['PR(%)'].mean()
                            
            except Exception:
                continue
        
        return {
            "total_export_kwh": round(total_export, 0),
            "operational_plants": operational_count,
            "avg_availability": round(availability_sum / max(operational_count, 1), 1),
            "avg_performance_ratio": round(pr_sum / max(operational_count, 1), 1),
            "week_start": start_date.strftime("%Y-%m-%d"),
            "week_end": end_date.strftime("%Y-%m-%d")
        }
    
    def _calculate_week_over_week_changes(self, this_week: Dict, last_week: Dict) -> Dict:
        """Calculate week-over-week percentage changes"""
        # Export change
        this_export = this_week.get('total_export_kwh', 0)
        last_export = last_week.get('total_export_kwh', 0)
        if last_export > 0:
            export_change = ((this_export - last_export) / last_export) * 100
        else:
            export_change = 0
        
        # Availability change
        this_avail = this_week.get('avg_availability', 0)
        last_avail = last_week.get('avg_availability', 0)
        avail_change = this_avail - last_avail
        
        # Performance ratio change
        this_pr = this_week.get('avg_performance_ratio', 0)
        last_pr = last_week.get('avg_performance_ratio', 0)
        pr_change = this_pr - last_pr
        
        return {
            "export_change_pct": round(export_change, 1),
            "availability_change_pts": round(avail_change, 1),
            "performance_ratio_change_pts": round(pr_change, 1),
            "operational_plants_change": this_week.get('operational_plants', 0) - last_week.get('operational_plants', 0)
        }
    
    def _generate_top_stories(self, plants: List[str], changes: Dict) -> List[str]:
        """Generate top stories for weekly digest"""
        stories = []
        
        # Export performance story
        export_change = changes.get('export_change_pct', 0)
        if export_change > 10:
            stories.append(f"📈 Strong Performance: Energy export increased {export_change:+.1f}% this week")
        elif export_change < -10:
            stories.append(f"📉 Performance Alert: Energy export decreased {export_change:+.1f}% this week")
        else:
            stories.append(f"📊 Stable Production: Energy export {export_change:+.1f}% week-over-week")
        
        # Availability story
        avail_change = changes.get('availability_change_pts', 0)
        if avail_change > 2:
            stories.append(f"🔧 Improved Reliability: Plant availability increased {avail_change:+.1f} percentage points")
        elif avail_change < -2:
            stories.append(f"⚠️ Maintenance Alert: Plant availability decreased {avail_change:+.1f} percentage points")
        
        # Operational changes
        ops_change = changes.get('operational_plants_change', 0)
        if ops_change > 0:
            stories.append(f"🏭 Expansion: {ops_change} additional plant(s) came online")
        elif ops_change < 0:
            stories.append(f"🔧 Maintenance: {abs(ops_change)} plant(s) offline for maintenance")
        
        return stories[:3]  # Top 3 stories
    
    def _generate_weekly_action_items(self, plants: List[str]) -> List[str]:
        """Generate action items for the upcoming week"""
        action_items = []
        
        # Check plants needing attention
        for plant in plants[:5]:  # Check top 5 plants
            try:
                summary = self.data_processor.get_plant_summary(plant, days=7)
                if summary:
                    availability = summary.get('avg_availability', 0)
                    pr = summary.get('avg_performance_ratio', 0)
                    
                    if availability < 90:
                        action_items.append(f"🔧 {plant}: Schedule maintenance review (availability: {availability:.1f}%)")
                    elif pr < 75:
                        action_items.append(f"⚡ {plant}: Investigate performance issues (PR: {pr:.1f}%)")
                        
            except Exception:
                continue
        
        # General action items
        if not action_items:
            action_items.append("✅ Continue monitoring all plants - performance within acceptable ranges")
            action_items.append("📊 Review monthly performance trends and update forecasts")
        
        action_items.append("📈 Prepare next week's optimization strategy")
        
        return action_items[:5]  # Top 5 action items