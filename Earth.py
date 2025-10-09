import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class EarthDataAnalyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.colors = ['#1E90FF', '#32CD32', '#FF4500', '#8A2BE2', '#FFD700', 
                      '#00CED1', '#FF6347', '#6A5ACD', '#2E8B57', '#DA70D6']
        
        self.start_year = 1850  # Début des observations météorologiques modernes
        self.end_year = 2025
        
        # Configuration spécifique pour chaque type de données terrestres
        self.config = self._get_earth_config()
        
    def _get_earth_config(self):
        """Retourne la configuration spécifique pour chaque type de données terrestres"""
        configs = {
            "temperature": {
                "base_value": 14.0,
                "cycle_years": 1.0,
                "amplitude": 15.0,
                "trend": "croissante",
                "unit": "°C",
                "description": "Température moyenne globale"
            },
            "co2": {
                "base_value": 280,
                "cycle_years": 1.0,
                "amplitude": 10,
                "trend": "croissante",
                "unit": "ppm",
                "description": "Concentration de CO2 atmosphérique"
            },
            "sea_level": {
                "base_value": 0,
                "cycle_years": 1.0,
                "amplitude": 5,
                "trend": "croissante",
                "unit": "mm",
                "description": "Élévation du niveau de la mer"
            },
            "precipitation": {
                "base_value": 1000,
                "cycle_years": 1.0,
                "amplitude": 300,
                "trend": "variable",
                "unit": "mm/an",
                "description": "Précipitations annuelles"
            },
            "glaciers": {
                "base_value": 100,
                "cycle_years": 10.0,
                "amplitude": 30,
                "trend": "décroissante",
                "unit": "% de masse",
                "description": "Masse des glaciers"
            },
            "biodiversity": {
                "base_value": 100,
                "cycle_years": 10.0,
                "amplitude": 20,
                "trend": "décroissante",
                "unit": "Index de diversité",
                "description": "Diversité biologique"
            },
            "air_quality": {
                "base_value": 50,
                "cycle_years": 1.0,
                "amplitude": 30,
                "trend": "variable",
                "unit": "AQI",
                "description": "Qualité de l'air"
            },
            "ocean_ph": {
                "base_value": 8.1,
                "cycle_years": 10.0,
                "amplitude": 0.3,
                "trend": "décroissante",
                "unit": "pH",
                "description": "Acidification des océans"
            },
            # Configuration par défaut
            "default": {
                "base_value": 100,
                "cycle_years": 1.0,
                "amplitude": 20,
                "trend": "stable",
                "unit": "Unités",
                "description": "Données terrestres génériques"
            }
        }
        
        return configs.get(self.data_type, configs["default"])
    
    def generate_earth_data(self):
        """Génère des données terrestres simulées basées sur les cycles climatiques réels"""
        print(f"🌍 Génération des données terrestres pour {self.config['description']}...")
        
        # Créer une base de données annuelle
        dates = pd.date_range(start=f'{self.start_year}-01-01', 
                             end=f'{self.end_year}-12-31', freq='Y')
        
        data = {'Year': [date.year for date in dates]}
        
        # Données principales basées sur les cycles climatiques
        data['Base_Value'] = self._simulate_earth_cycle(dates)
        data['Seasonal_Min'] = self._simulate_seasonal_minima(dates)
        data['Seasonal_Max'] = self._simulate_seasonal_maxima(dates)
        data['Annual_Cycle'] = self._simulate_annual_cycle(dates)
        
        # Variations à long terme
        data['Climate_Trend'] = self._simulate_climate_trend(dates)
        data['Extreme_Events'] = self._simulate_extreme_events(dates)
        data['Human_Impact'] = self._simulate_human_impact(dates)
        
        # Données dérivées
        data['Smoothed_Value'] = self._simulate_smoothed_data(dates)
        data['Monthly_Variation'] = self._simulate_monthly_variation(dates)
        data['Decadal_Variation'] = self._simulate_decadal_variation(dates)
        
        # Indices environnementaux complémentaires
        data['Environmental_Index'] = self._simulate_environmental_index(dates)
        data['Risk_Level'] = self._simulate_risk_level(dates)
        data['Future_Projection'] = self._simulate_future_projection(dates)
        
        df = pd.DataFrame(data)
        
        # Ajouter des événements climatiques historiques
        self._add_climate_events(df)
        
        return df
    
    def _simulate_earth_cycle(self, dates):
        """Simule le cycle climatique principal"""
        base_value = self.config["base_value"]
        cycle_years = self.config["cycle_years"]
        amplitude = self.config["amplitude"]
        
        values = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Cycle annuel de base
            annual_cycle = np.sin(2 * np.pi * (year - self.start_year) / cycle_years)
            
            # Ajustement pour différents types de données
            if self.config["trend"] == "croissante":
                trend_factor = 1 + 0.01 * (year - 1850) / 100
            elif self.config["trend"] == "décroissante":
                trend_factor = 1 - 0.01 * (year - 1850) / 100
            else:
                trend_factor = 1.0
            
            value = base_value * trend_factor + amplitude * annual_cycle
            
            # Bruit naturel
            noise = np.random.normal(0, amplitude * 0.05)
            values.append(value + noise)
        
        return values
    
    def _simulate_seasonal_minima(self, dates):
        """Simule les périodes de minimum saisonnier"""
        minima = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Variation saisonnière
            seasonal_phase = (year - self.start_year) % 1.0
            
            if self.data_type == "temperature":
                # Minimum en hiver
                if seasonal_phase < 0.25 or seasonal_phase > 0.75:
                    min_factor = 0.7
                else:
                    min_factor = 1.0
            else:
                min_factor = 0.8 + 0.2 * np.sin(2 * np.pi * seasonal_phase)
            
            minima.append(min_factor)
        
        return minima
    
    def _simulate_seasonal_maxima(self, dates):
        """Simule les périodes de maximum saisonnier"""
        maxima = []
        for i, date in enumerate(dates):
            year = date.year
            seasonal_phase = (year - self.start_year) % 1.0
            
            if self.data_type == "temperature":
                # Maximum en été
                if 0.25 <= seasonal_phase <= 0.75:
                    max_factor = 1.0
                else:
                    max_factor = 0.8
            else:
                max_factor = 1.0 + 0.2 * np.sin(2 * np.pi * seasonal_phase)
            
            maxima.append(max_factor)
        
        return maxima
    
    def _simulate_annual_cycle(self, dates):
        """Simule le cycle annuel (0-1)"""
        cycles = []
        for date in dates:
            year = date.year
            cycle = (year - self.start_year) % 1.0
            cycles.append(cycle)
        
        return cycles
    
    def _simulate_climate_trend(self, dates):
        """Simule les tendances climatiques à long terme"""
        trends = []
        for i, date in enumerate(dates):
            year = date.year
            
            # Tendance climatique basée sur l'ère industrielle
            if year < 1900:
                trend = 1.0  # Période pré-industrielle
            elif 1900 <= year < 1950:
                trend = 1.0 + 0.002 * (year - 1900)  # Début industrialisation
            elif 1950 <= year < 1980:
                trend = 1.02 + 0.005 * (year - 1950)  # Accélération
            elif 1980 <= year < 2000:
                trend = 1.1 + 0.01 * (year - 1980)  # Période moderne
            else:
                trend = 1.3 + 0.015 * (year - 2000)  # Période contemporaine
            
            trends.append(trend)
        
        return trends
    
    def _simulate_extreme_events(self, dates):
        """Simule les événements climatiques extrêmes"""
        extremes = []
        for date in dates:
            year = date.year
            
            # Augmentation des événements extrêmes avec le temps
            base_prob = 0.1
            time_factor = 0.001 * (year - 1850)
            extreme_prob = min(0.8, base_prob + time_factor)
            
            # Simulation d'événement extrême
            if np.random.random() < extreme_prob:
                intensity = 1.0 + 0.5 * (year - 1850) / 100
            else:
                intensity = 1.0
            
            extremes.append(intensity)
        
        return extremes
    
    def _simulate_human_impact(self, dates):
        """Simule l'impact des activités humaines"""
        impacts = []
        for date in dates:
            year = date.year
            
            # Impact croissant des activités humaines
            if year < 1800:
                impact = 1.0  # Impact négligeable
            elif 1800 <= year < 1900:
                impact = 1.0 + 0.005 * (year - 1800)  # Révolution industrielle
            elif 1900 <= year < 1950:
                impact = 1.5 + 0.01 * (year - 1900)  # Industrialisation
            elif 1950 <= year < 1980:
                impact = 2.0 + 0.02 * (year - 1950)  # Expansion
            elif 1980 <= year < 2000:
                impact = 2.6 + 0.03 * (year - 1980)  # Mondialisation
            else:
                impact = 3.2 + 0.04 * (year - 2000)  # Période actuelle
            
            impacts.append(impact)
        
        return impacts
    
    def _simulate_smoothed_data(self, dates):
        """Simule des données lissées (moyenne mobile sur 10 ans)"""
        base_cycle = self._simulate_earth_cycle(dates)
        
        smoothed = []
        for i in range(len(base_cycle)):
            # Moyenne mobile centrée sur 10 ans
            start_idx = max(0, i - 5)
            end_idx = min(len(base_cycle), i + 5)
            window = base_cycle[start_idx:end_idx]
            smoothed.append(np.mean(window))
        
        return smoothed
    
    def _simulate_monthly_variation(self, dates):
        """Simule les variations mensuelles"""
        variations = []
        for date in dates:
            # Variation saisonnière
            month = date.month
            seasonal_variation = 0.1 * np.sin(2 * np.pi * (month - 1) / 12)
            variations.append(1 + seasonal_variation)
        
        return variations
    
    def _simulate_decadal_variation(self, dates):
        """Simule les variations décennales"""
        variations = []
        for i, date in enumerate(dates):
            year = date.year
            # Variation décennale
            decadal_variation = 0.05 * np.sin(2 * np.pi * (year - self.start_year) / 10)
            variations.append(1 + decadal_variation)
        
        return variations
    
    def _simulate_environmental_index(self, dates):
        """Simule un indice environnemental composite"""
        indices = []
        base_cycle = self._simulate_earth_cycle(dates)
        climate_trend = self._simulate_climate_trend(dates)
        
        for i in range(len(dates)):
            # Indice composite pondéré
            index = (base_cycle[i] * 0.6 + 
                    climate_trend[i] * self.config["base_value"] * 0.4)
            indices.append(index)
        
        return indices
    
    def _simulate_risk_level(self, dates):
        """Simule le niveau de risque environnemental (0-100)"""
        risk_levels = []
        human_impact = self._simulate_human_impact(dates)
        extreme_events = self._simulate_extreme_events(dates)
        
        for i in range(len(dates)):
            # Calcul du risque basé sur l'impact humain et les événements extrêmes
            risk = min(100, human_impact[i] * 20 + (extreme_events[i] - 1) * 50)
            risk_levels.append(risk)
        
        return risk_levels
    
    def _simulate_future_projection(self, dates):
        """Simule des projections futures"""
        projections = []
        base_cycle = self._simulate_earth_cycle(dates)
        climate_trend = self._simulate_climate_trend(dates)
        
        for i, date in enumerate(dates):
            year = date.year
            current_value = base_cycle[i]
            trend_factor = climate_trend[i]
            
            if year > 2020:  # Période de projection
                # Ajouter une incertitude croissante
                years_since_2020 = year - 2020
                uncertainty = 0.03 * years_since_2020
                
                if self.config["trend"] == "croissante":
                    projection = current_value * trend_factor * (1 + np.random.normal(0.02, uncertainty))
                elif self.config["trend"] == "décroissante":
                    projection = current_value * trend_factor * (1 - np.random.normal(0.01, uncertainty))
                else:
                    projection = current_value * (1 + np.random.normal(0, uncertainty))
            else:
                projection = current_value
            
            projections.append(projection)
        
        return projections
    
    def _add_climate_events(self, df):
        """Ajoute des événements climatiques historiques significatifs"""
        for i, row in df.iterrows():
            year = row['Year']
            
            # Événements climatiques historiques
            if 1815 <= year <= 1816:
                # Éruption du Tambora - année sans été
                df.loc[i, 'Base_Value'] *= 0.9
                df.loc[i, 'Risk_Level'] *= 1.2
            
            elif 1930 <= year <= 1939:
                # Dust Bowl - sécheresse extrême
                if self.data_type in ["temperature", "precipitation"]:
                    df.loc[i, 'Base_Value'] *= 1.1
                    df.loc[i, 'Risk_Level'] *= 1.3
            
            elif 1982 <= year <= 1983:
                # El Niño majeur
                df.loc[i, 'Base_Value'] *= 1.05
                df.loc[i, 'Extreme_Events'] *= 1.5
            
            elif 1997 <= year <= 1998:
                # El Niño record
                df.loc[i, 'Base_Value'] *= 1.08
                df.loc[i, 'Extreme_Events'] *= 1.8
            
            elif 2003:
                # Canicule européenne
                if self.data_type == "temperature":
                    df.loc[i, 'Base_Value'] *= 1.1
                    df.loc[i, 'Risk_Level'] = min(100, df.loc[i, 'Risk_Level'] * 1.4)
            
            elif 2005:
                # Ouragan Katrina
                df.loc[i, 'Extreme_Events'] *= 1.6
            
            elif 2011:
                # Sécheresse du Texas + Fukushima
                df.loc[i, 'Risk_Level'] *= 1.3
            
            elif 2019:
                # Incendies en Australie
                if self.data_type in ["temperature", "air_quality"]:
                    df.loc[i, 'Base_Value'] *= 1.05
                    df.loc[i, 'Risk_Level'] *= 1.2
            
            elif 2020:
                # Année record de températures
                if self.data_type == "temperature":
                    df.loc[i, 'Base_Value'] *= 1.02
    
    def create_earth_analysis(self, df):
        """Crée une analyse complète des données terrestres"""
        plt.style.use('seaborn-v0_8')  # Style clair pour les données terrestres
        fig = plt.figure(figsize=(20, 28))
        
        # 1. Données principales
        ax1 = plt.subplot(5, 2, 1)
        self._plot_primary_data(df, ax1)
        
        # 2. Tendances climatiques
        ax2 = plt.subplot(5, 2, 2)
        self._plot_climate_trends(df, ax2)
        
        # 3. Variations saisonnières
        ax3 = plt.subplot(5, 2, 3)
        self._plot_seasonal_variations(df, ax3)
        
        # 4. Impact humain
        ax4 = plt.subplot(5, 2, 4)
        self._plot_human_impact(df, ax4)
        
        # 5. Cycle annuel
        ax5 = plt.subplot(5, 2, 5)
        self._plot_annual_cycle(df, ax5)
        
        # 6. Données lissées
        ax6 = plt.subplot(5, 2, 6)
        self._plot_smoothed_data_plot(df, ax6)
        
        # 7. Niveau de risque
        ax7 = plt.subplot(5, 2, 7)
        self._plot_risk_level(df, ax7)
        
        # 8. Événements extrêmes
        ax8 = plt.subplot(5, 2, 8)
        self._plot_extreme_events(df, ax8)
        
        # 9. Indice environnemental
        ax9 = plt.subplot(5, 2, 9)
        self._plot_environmental_index(df, ax9)
        
        # 10. Projections futures
        ax10 = plt.subplot(5, 2, 10)
        self._plot_future_projections(df, ax10)
        
        plt.suptitle(f'Analyse des Données Terrestres: {self.config["description"]} ({self.start_year}-{self.end_year})', 
                    fontsize=16, fontweight='bold', color='darkblue')
        plt.tight_layout()
        plt.savefig(f'earth_{self.data_type}_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
        
        # Générer les insights
        self._generate_earth_insights(df)
    
    def _plot_primary_data(self, df, ax):
        """Plot des données principales"""
        ax.plot(df['Year'], df['Base_Value'], label='Valeur observée', 
               linewidth=2, color='#1E90FF', alpha=0.9)
        
        ax.set_title(f'Données Principales - {self.config["description"]}', 
                    fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel(self.config["unit"], color='#1E90FF')
        ax.tick_params(axis='y', labelcolor='#1E90FF')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        
        # Ajouter des annotations pour les décennies
        for year in range(1850, 2026, 10):
            if year in df['Year'].values:
                ax.axvline(x=year, alpha=0.2, color='blue', linestyle='--')
    
    def _plot_climate_trends(self, df, ax):
        """Plot des tendances climatiques"""
        ax.plot(df['Year'], df['Climate_Trend'], label='Tendance climatique', 
               linewidth=2, color='#FF4500')
        ax.plot(df['Year'], df['Human_Impact'], label='Impact humain', 
               linewidth=2, color='#8A2BE2')
        
        ax.set_title('Tendances Climatiques et Impact Humain', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Facteur multiplicatif', color='darkblue')
        ax.legend()
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_seasonal_variations(self, df, ax):
        """Plot des variations saisonnières"""
        ax.plot(df['Year'], df['Seasonal_Min'], label='Minimum saisonnier', 
               color='#1E90FF', alpha=0.7)
        ax.plot(df['Year'], df['Seasonal_Max'], label='Maximum saisonnier', 
               color='#FF6347', alpha=0.7)
        
        ax.set_title('Variations Saisonnières', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Facteur d\'amplitude', color='darkblue')
        ax.legend()
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_human_impact(self, df, ax):
        """Plot de l'impact humain"""
        ax.fill_between(df['Year'], df['Human_Impact'], alpha=0.6, 
                       color='#8A2BE2', label='Impact humain')
        
        ax.set_title('Impact des Activités Humaines', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Niveau d\'impact', color='darkblue')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_annual_cycle(self, df, ax):
        """Plot du cycle annuel"""
        scatter = ax.scatter(df['Year'], df['Annual_Cycle'], c=df['Annual_Cycle'], 
                           cmap='viridis', alpha=0.7, s=30)
        
        ax.set_title('Cycle Annuel (0-1)', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Phase du cycle', color='darkblue')
        ax.set_xlabel('Année', color='darkblue')
        plt.colorbar(scatter, ax=ax, label='Phase annuelle')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_smoothed_data_plot(self, df, ax):
        """Plot des données lissées"""
        ax.plot(df['Year'], df['Base_Value'], label='Données brutes', 
               alpha=0.5, color='#1E90FF')
        ax.plot(df['Year'], df['Smoothed_Value'], label='Données lissées (10 ans)', 
               linewidth=2, color='#32CD32')
        
        ax.set_title('Données Brutes vs Lissées', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel(self.config["unit"], color='darkblue')
        ax.legend()
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_risk_level(self, df, ax):
        """Plot du niveau de risque environnemental"""
        ax.fill_between(df['Year'], df['Risk_Level'], alpha=0.6, 
                       color='#FF4500', label='Niveau de risque')
        ax.plot(df['Year'], df['Risk_Level'], color='#8B0000', alpha=0.8)
        
        ax.set_title('Niveau de Risque Environnemental (0-100)', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Niveau de risque', color='darkblue')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_extreme_events(self, df, ax):
        """Plot des événements extrêmes"""
        ax.bar(df['Year'], df['Extreme_Events'], alpha=0.6, 
              color='#FF6347', label='Intensité des événements extrêmes')
        
        ax.set_title('Événements Climatiques Extrêmes', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Intensité relative', color='darkblue')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_environmental_index(self, df, ax):
        """Plot de l'indice environnemental composite"""
        ax.plot(df['Year'], df['Environmental_Index'], label='Indice environnemental', 
               linewidth=2, color='#2E8B57')
        
        ax.set_title('Indice Environnemental Composite', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel('Valeur de l\'indice', color='darkblue')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _plot_future_projections(self, df, ax):
        """Plot des projections futures"""
        ax.plot(df['Year'], df['Base_Value'], label='Données historiques', 
               color='#1E90FF', alpha=0.7)
        ax.plot(df['Year'], df['Future_Projection'], label='Projections futures', 
               linewidth=2, color='#FF8C00', linestyle='--')
        
        ax.axvline(x=2020, color='red', linestyle=':', alpha=0.7, label='Début des projections')
        
        ax.set_title('Données Historiques et Projections Futures', fontsize=12, fontweight='bold', color='darkblue')
        ax.set_ylabel(self.config["unit"], color='darkblue')
        ax.legend()
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_facecolor('lightcyan')
        ax.tick_params(colors='darkblue')
    
    def _generate_earth_insights(self, df):
        """Génère des insights analytiques sur les données terrestres"""
        print(f"🌍 INSIGHTS ANALYTIQUES - {self.config['description']}")
        print("=" * 70)
        
        # 1. Statistiques de base
        print("\n1. 📊 STATISTIQUES FONDAMENTALES:")
        avg_value = df['Base_Value'].mean()
        max_value = df['Base_Value'].max()
        min_value = df['Base_Value'].min()
        current_value = df['Base_Value'].iloc[-1]
        
        print(f"Valeur moyenne: {avg_value:.2f} {self.config['unit']}")
        print(f"Valeur maximale: {max_value:.2f} {self.config['unit']}")
        print(f"Valeur minimale: {min_value:.2f} {self.config['unit']}")
        print(f"Valeur actuelle: {current_value:.2f} {self.config['unit']}")
        
        # 2. Analyse des tendances
        print("\n2. 📈 ANALYSE DES TENDANCES:")
        total_change = ((df['Base_Value'].iloc[-1] / df['Base_Value'].iloc[0]) - 1) * 100
        recent_change = ((df['Base_Value'].iloc[-1] / df[df['Year'] >= 2000]['Base_Value'].iloc[0]) - 1) * 100
        
        print(f"Changement total depuis 1850: {total_change:+.1f}%")
        print(f"Changement depuis 2000: {recent_change:+.1f}%")
        print(f"Tendance principale: {self.config['trend']}")
        
        # 3. Risque environnemental
        print("\n3. ⚠️  RISQUE ENVIRONNEMENTAL:")
        current_risk = df['Risk_Level'].iloc[-1]
        risk_trend = (df['Risk_Level'].iloc[-1] / df[df['Year'] >= 2000]['Risk_Level'].iloc[0] - 1) * 100
        
        print(f"Niveau de risque actuel: {current_risk:.1f}/100")
        print(f"Évolution du risque depuis 2000: {risk_trend:+.1f}%")
        
        if current_risk > 70:
            print("→ Niveau de risque ÉLEVÉ")
        elif current_risk > 40:
            print("→ Niveau de risque MODÉRÉ")
        else:
            print("→ Niveau de risque FAIBLE")
        
        # 4. Événements majeurs
        print("\n4. 🌪️  ÉVÉNEMENTS CLIMATIQUES MARQUANTS:")
        print("• 1815-1816: Éruption du Tambora - 'année sans été'")
        print("• 1930-1939: Dust Bowl - sécheresse extrême aux États-Unis")
        print("• 1982-1983: El Niño majeur avec impacts globaux")
        print("• 1997-1998: El Niño le plus intense du 20ème siècle")
        print("• 2003: Canicule européenne - 70,000 morts")
        print("• 2005: Ouragan Katrina - New Orleans inondée")
        print("• 2019-2020: Incendies records en Australie")
        print("• 2020: Année record de températures globales")
        
        # 5. Impact humain
        print("\n5. 👥 IMPACT HUMAIN:")
        human_impact_current = df['Human_Impact'].iloc[-1]
        human_growth = (df['Human_Impact'].iloc[-1] / df['Human_Impact'].iloc[0] - 1) * 100
        
        print(f"Facteur d'impact humain actuel: {human_impact_current:.1f}x")
        print(f"Augmentation depuis 1850: {human_growth:+.0f}%")
        
        # 6. Projections futures
        print("\n6. 🔮 PROJECTIONS FUTURES:")
        future_change = ((df['Future_Projection'].iloc[-1] / 
                         df['Base_Value'].iloc[-1]) - 1) * 100
        
        print(f"Changement projeté d'ici 2025: {future_change:+.1f}%")
        
        if self.config["trend"] == "croissante":
            print("→ Tendance à la hausse prévue")
        elif self.config["trend"] == "décroissante":
            print("→ Tendance à la baisse prévue")
        else:
            print("→ Stabilité relative prévue")
        
        # 7. Implications environnementales
        print("\n7. 🎯 IMPLICATIONS ENVIRONNEMENTALES:")
        if self.data_type == "temperature":
            print("• Impact direct sur les écosystèmes")
            print("• Risque d'événements extrêmes accru")
            print("• Implications pour la sécurité alimentaire")
        
        elif self.data_type == "co2":
            print("• Principal facteur du changement climatique")
            print("• Acidification des océans")
            print("• Impact sur la photosynthèse")
        
        elif self.data_type == "sea_level":
            print("• Menace pour les zones côtières")
            print("• Déplacement des populations")
            print("• Perte de territoires")
        
        elif self.data_type == "biodiversity":
            print("• Effondrement des écosystèmes")
            print("• Perte de services écosystémiques")
            print("• Risque pour la sécurité alimentaire")
        
        print("• Nécessité d'actions d'atténuation")
        print("• Importance de l'adaptation climatique")
        print("• Enjeu de gouvernance mondiale")

def main():
    """Fonction principale pour l'analyse des données terrestres"""
    # Types de données terrestres disponibles
    earth_data_types = [
        "temperature", "co2", "sea_level", "precipitation",
        "glaciers", "biodiversity", "air_quality", "ocean_ph"
    ]
    
    print("🌍 ANALYSE DES DONNÉES NUMÉRIQUES DE LA TERRE (1850-2025)")
    print("=" * 65)
    
    # Demander à l'utilisateur de choisir un type de données
    print("Types de données terrestres disponibles:")
    for i, data_type in enumerate(earth_data_types, 1):
        analyzer_temp = EarthDataAnalyzer(data_type)
        print(f"{i}. {analyzer_temp.config['description']}")
    
    try:
        choix = int(input("\nChoisissez le numéro du type de données à analyser: "))
        if choix < 1 or choix > len(earth_data_types):
            raise ValueError
        selected_type = earth_data_types[choix-1]
    except (ValueError, IndexError):
        print("Choix invalide. Sélection de la température par défaut.")
        selected_type = "temperature"
    
    # Initialiser l'analyseur
    analyzer = EarthDataAnalyzer(selected_type)
    
    # Générer les données
    earth_data = analyzer.generate_earth_data()
    
    # Sauvegarder les données
    output_file = f'earth_{selected_type}_data_1850_2025.csv'
    earth_data.to_csv(output_file, index=False)
    print(f"💾 Données sauvegardées: {output_file}")
    
    # Aperçu des données
    print("\n👀 Aperçu des données:")
    print(earth_data[['Year', 'Base_Value', 'Risk_Level', 'Environmental_Index']].head())
    
    # Créer l'analyse
    print("\n📈 Création de l'analyse des données terrestres...")
    analyzer.create_earth_analysis(earth_data)
    
    print(f"\n✅ Analyse des données {analyzer.config['description']} terminée!")
    print(f"📊 Période: {analyzer.start_year}-{analyzer.end_year}")
    print("🌡️ Données: Climat, environnement, tendances, projections")

if __name__ == "__main__":
    main()