import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import de votre classe EarthDataAnalyzer existante
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from Earth import EarthDataAnalyzer
except ImportError:
    st.error("Impossible d'importer EarthDataAnalyzer. Création d'une version simplifiée...")
    
    # Version de secours si l'import échoue
    class EarthDataAnalyzer:
        def __init__(self, data_type):
            self.data_type = data_type
            self.config = self._get_config()
            
        def _get_config(self):
            configs = {
                "temperature": {"base_value": 14.0, "unit": "°C", "description": "Température moyenne globale"},
                "co2": {"base_value": 280, "unit": "ppm", "description": "Concentration de CO2 atmosphérique"},
                "sea_level": {"base_value": 0, "unit": "mm", "description": "Élévation du niveau de la mer"},
                "precipitation": {"base_value": 1000, "unit": "mm/an", "description": "Précipitations annuelles"},
                "glaciers": {"base_value": 100, "unit": "% de masse", "description": "Masse des glaciers"},
                "biodiversity": {"base_value": 100, "unit": "Index", "description": "Diversité biologique"},
                "air_quality": {"base_value": 50, "unit": "AQI", "description": "Qualité de l'air"},
                "ocean_ph": {"base_value": 8.1, "unit": "pH", "description": "Acidification des océans"},
            }
            return configs.get(self.data_type, {"base_value": 100, "unit": "Unités", "description": "Données génériques"})
        
        def generate_earth_data(self):
            # Simulation de données simplifiée - CORRIGE avec 'YE'
            dates = pd.date_range(start='1850-01-01', end='2025-12-31', freq='YE')  # CORRECTION ICI
            data = {'Year': [date.year for date in dates]}
            
            # Données simulées basiques
            base_value = self.config["base_value"]
            years = np.array([date.year for date in dates])
            
            # Tendances selon le type de données
            if self.data_type in ["temperature", "co2", "sea_level"]:
                trend = base_value * (1 + 0.01 * (years - 1850) / 100)
            elif self.data_type in ["glaciers", "biodiversity", "ocean_ph"]:
                trend = base_value * (1 - 0.005 * (years - 1850) / 100)
            else:
                trend = base_value * np.ones_like(years)
            
            data['Base_Value'] = trend + np.random.normal(0, base_value * 0.1, len(years))
            data['Risk_Level'] = np.clip(20 + 0.5 * (years - 1850), 0, 100)
            data['Climate_Trend'] = 1 + 0.005 * (years - 1850)
            data['Human_Impact'] = 1 + 0.01 * (years - 1850)
            data['Extreme_Events'] = 1 + 0.002 * (years - 1850) + np.random.normal(0, 0.1, len(years))
            data['Future_Projection'] = data['Base_Value'] * (1 + 0.01 * np.maximum(0, years - 2020))
            
            return pd.DataFrame(data)

class EarthStreamlitDashboard:
    def __init__(self):
        self.setup_page()
        
    def setup_page(self):
        """Configure la page Streamlit"""
        st.set_page_config(
            page_title="🌍 Dashboard Terre - Surveillance Environnementale",
            page_icon="🌍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def run(self):
        """Lance le dashboard Streamlit"""
        # En-tête
        st.markdown("""
            <style>
            .main-header {
                font-size: 2.5rem;
                color: #1E3A5F;
                text-align: center;
                margin-bottom: 2rem;
            }
            .kpi-card {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin: 0.5rem;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-header">🌍 DASHBOARD TERRE - SURVEILLANCE ENVIRONNEMENTALE</h1>', 
                   unsafe_allow_html=True)
        st.markdown("**Surveillance en temps réel des données climatiques et environnementales (1850-2025)**")
        
        # Sidebar - Contrôles
        st.sidebar.title("🔧 Paramètres d'Analyse")
        
        # Sélecteur de données
        data_type = st.sidebar.selectbox(
            "Type de données environnementales:",
            options=["temperature", "co2", "sea_level", "precipitation", 
                    "glaciers", "biodiversity", "air_quality", "ocean_ph"],
            format_func=lambda x: {
                "temperature": "🌡️ Température globale",
                "co2": "🏭 CO2 atmosphérique", 
                "sea_level": "🌊 Niveau de la mer",
                "precipitation": "💧 Précipitations",
                "glaciers": "🏔️ Glaciers",
                "biodiversity": "🦋 Biodiversité",
                "air_quality": "💨 Qualité de l'air",
                "ocean_ph": "🌊 pH des océans"
            }[x]
        )
        
        # Paramètres avancés
        st.sidebar.subheader("Paramètres d'Analyse")
        year_range = st.sidebar.slider(
            "Période d'analyse:",
            min_value=1850,
            max_value=2025,
            value=(1950, 2025)
        )
        
        smoothing = st.sidebar.slider(
            "Fenêtre de lissage:",
            min_value=1,
            max_value=20,
            value=10
        )
        
        alert_threshold = st.sidebar.slider(
            "Seuil d'alerte risque:",
            min_value=0,
            max_value=100,
            value=70
        )
        
        # Générer les données
        analyzer = EarthDataAnalyzer(data_type)
        df = analyzer.generate_earth_data()
        df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()  # CORRECTION ICI
        
        # Appliquer le lissage - CORRIGE avec .loc
        if smoothing > 1:
            df_filtered.loc[:, 'Smoothed_Value'] = df_filtered['Base_Value'].rolling(window=smoothing, center=True).mean()  # CORRECTION ICI
        
        # KPI Cards
        self.display_kpi_cards(df, analyzer)
        
        # Graphiques principaux
        col1, col2 = st.columns(2)
        
        with col1:
            self.plot_main_timeline(df_filtered, analyzer, smoothing)
        
        with col2:
            self.plot_risk_analysis(df_filtered, analyzer, alert_threshold)
        
        # Graphiques secondaires
        col3, col4 = st.columns(2)
        
        with col3:
            self.plot_seasonal_analysis(df_filtered, analyzer)
        
        with col4:
            self.plot_impact_analysis(df, analyzer)
        
        # Graphiques supplémentaires
        col5, col6 = st.columns(2)
        
        with col5:
            self.plot_future_projections(df, analyzer)
        
        with col6:
            self.plot_extreme_events(df_filtered, analyzer)
        
        # Carte thermique
        st.subheader("🌐 Carte Globale des Données Environnementales")
        self.plot_global_heatmap(analyzer)
        
        # Insights et analyses
        self.display_insights(df, analyzer)
    
    def display_kpi_cards(self, df, analyzer):
        """Affiche les cartes KPI"""
        col1, col2, col3, col4 = st.columns(4)
        
        # KPI 1: Valeur actuelle
        current_value = df['Base_Value'].iloc[-1]
        unit = analyzer.config["unit"]
        
        with col1:
            st.markdown(f"""
                <div class="kpi-card">
                    <h3>Valeur Actuelle</h3>
                    <h2 style="color: #2E8B57;">{current_value:.1f}{unit}</h2>
                    <p>{analyzer.config['description']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # KPI 2: Tendance
        recent_trend = ((df['Base_Value'].iloc[-1] / df[df['Year'] >= 2000]['Base_Value'].iloc[0]) - 1) * 100
        trend_icon = "📈" if recent_trend > 0 else "📉"
        
        with col2:
            st.markdown(f"""
                <div class="kpi-card">
                    <h3>Tendance Récente</h3>
                    <h2 style="color: #FF8C00;">{trend_icon} {recent_trend:+.1f}%</h2>
                    <p>depuis 2000</p>
                </div>
            """, unsafe_allow_html=True)
        
        # KPI 3: Risque
        current_risk = df['Risk_Level'].iloc[-1]
        risk_color = "#DC143C" if current_risk > 70 else "#FF8C00" if current_risk > 40 else "#2E8B57"
        risk_text = "Élevé" if current_risk > 70 else "Modéré" if current_risk > 40 else "Faible"
        
        with col3:
            st.markdown(f"""
                <div class="kpi-card">
                    <h3>Niveau de Risque</h3>
                    <h2 style="color: {risk_color};">{current_risk:.0f}/100</h2>
                    <p>{risk_text}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # KPI 4: Changement total
        total_change = ((df['Base_Value'].iloc[-1] / df['Base_Value'].iloc[0]) - 1) * 100
        
        with col4:
            st.markdown(f"""
                <div class="kpi-card">
                    <h3>Changement Total</h3>
                    <h2 style="color: #1E90FF;">{total_change:+.1f}%</h2>
                    <p>depuis 1850</p>
                </div>
            """, unsafe_allow_html=True)
    
    def plot_main_timeline(self, df, analyzer, smoothing):
        """Graphique de la timeline principale"""
        st.subheader(f"{analyzer.config['description']} - Évolution Temporelle")
        
        fig = go.Figure()
        
        # Données brutes
        fig.add_trace(go.Scatter(
            x=df['Year'], y=df['Base_Value'],
            name='Données brutes',
            line=dict(color='#1E90FF', width=1, dash='dot'),
            opacity=0.6
        ))
        
        # Données lissées
        if smoothing > 1 and 'Smoothed_Value' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Smoothed_Value'],
                name=f'Données lissées ({smoothing} ans)',
                line=dict(color='#FF4500', width=3),
                opacity=0.9
            ))
        
        # Tendance linéaire
        z = np.polyfit(df['Year'], df['Base_Value'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=df['Year'], y=p(df['Year']),
            name='Tendance linéaire',
            line=dict(color='#32CD32', width=2, dash='dash'),
            opacity=0.8
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=True,
            xaxis_title='Année',
            yaxis_title=analyzer.config["unit"]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_risk_analysis(self, df, analyzer, threshold):
        """Analyse des risques"""
        st.subheader('Analyse des Risques Environnementaux')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Niveau de risque
        fig.add_trace(go.Scatter(
            x=df['Year'], y=df['Risk_Level'],
            name='Niveau de risque',
            line=dict(color='#DC143C', width=3),
            fill='tozeroy',
            fillcolor='rgba(220, 20, 60, 0.1)'
        ), secondary_y=False)
        
        # Impact humain
        if 'Human_Impact' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Human_Impact'],
                name='Impact humain',
                line=dict(color='#8A2BE2', width=2),
                opacity=0.7
            ), secondary_y=True)
        
        # Ligne de seuil d'alerte
        fig.add_hline(y=threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"Seuil d'alerte: {threshold}%")
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=True
        )
        
        fig.update_yaxes(title_text="Niveau de risque (%)", secondary_y=False)
        fig.update_yaxes(title_text="Facteur d'impact", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_seasonal_analysis(self, df, analyzer):
        """Analyse des variations saisonnières"""
        st.subheader('Variations Saisonnières')
        
        fig = go.Figure()
        
        if 'Seasonal_Min' in df.columns and 'Seasonal_Max' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Seasonal_Min'],
                name='Minimum saisonnier',
                line=dict(color='#1E90FF', width=2),
                fill=None
            ))
            
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Seasonal_Max'],
                name='Maximum saisonnier',
                line=dict(color='#FF6347', width=2),
                fill='tonexty',
                fillcolor='rgba(255, 99, 71, 0.1)'
            ))
        else:
            # Fallback si les colonnes n'existent pas
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Base_Value'],
                name='Valeur de base',
                line=dict(color='#1E90FF', width=2)
            ))
        
        fig.update_layout(
            height=350,
            template='plotly_white',
            showlegend=True,
            xaxis_title='Année',
            yaxis_title='Facteur d\'amplitude'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_impact_analysis(self, df, analyzer):
        """Analyse d'impact avec graphique radar"""
        st.subheader('Analyse d\'Impact - Profil Environnemental')
        
        # Créer un graphique radar
        categories = ['Tendance', 'Risque', 'Impact Humain', 'Événements Extrêmes', 'Stabilité']
        
        # Normaliser les valeurs pour le radar
        trend_norm = (df['Climate_Trend'].iloc[-1] - df['Climate_Trend'].min()) / (df['Climate_Trend'].max() - df['Climate_Trend'].min()) * 100
        risk_norm = df['Risk_Level'].iloc[-1]
        impact_norm = (df['Human_Impact'].iloc[-1] - df['Human_Impact'].min()) / (df['Human_Impact'].max() - df['Human_Impact'].min()) * 100
        extreme_norm = (df['Extreme_Events'].iloc[-1] - df['Extreme_Events'].min()) / (df['Extreme_Events'].max() - df['Extreme_Events'].min()) * 100
        stability_norm = 100 - (abs(df['Base_Value'].pct_change().std()) * 1000)
        
        values = [trend_norm, risk_norm, impact_norm, extreme_norm, min(stability_norm, 100)]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(30, 144, 255, 0.3)',
            line=dict(color='#1E90FF', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            height=350,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_future_projections(self, df, analyzer):
        """Projections futures"""
        st.subheader('Projections Futures avec Incertitude')
        
        fig = go.Figure()
        
        # Données historiques
        historical = df[df['Year'] <= 2020]
        fig.add_trace(go.Scatter(
            x=historical['Year'], y=historical['Base_Value'],
            name='Données historiques',
            line=dict(color='#1E90FF', width=3),
            opacity=0.8
        ))
        
        # Projections futures
        if 'Future_Projection' in df.columns:
            future = df[df['Year'] >= 2020]
            fig.add_trace(go.Scatter(
                x=future['Year'], y=future['Future_Projection'],
                name='Projections futures',
                line=dict(color='#FF8C00', width=3, dash='dash'),
                opacity=0.8
            ))
        
        fig.add_vline(x=2020, line_dash="dash", line_color="red", 
                     annotation_text="Début projections")
        
        fig.update_layout(
            height=350,
            template='plotly_white',
            showlegend=True,
            xaxis_title='Année',
            yaxis_title=analyzer.config["unit"]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_extreme_events(self, df, analyzer):
        """Événements extrêmes"""
        st.subheader('Événements Climatiques Extrêmes')
        
        # Identifier les événements extrêmes
        if 'Extreme_Events' in df.columns:
            threshold = df['Extreme_Events'].quantile(0.9)
            extreme_df = df[df['Extreme_Events'] > threshold]
            
            fig = go.Figure()
            
            # Tous les événements
            fig.add_trace(go.Bar(
                x=df['Year'], y=df['Extreme_Events'],
                name='Intensité des événements',
                marker_color='lightgray',
                opacity=0.5
            ))
            
            # Événements extrêmes
            fig.add_trace(go.Bar(
                x=extreme_df['Year'], y=extreme_df['Extreme_Events'],
                name='Événements extrêmes',
                marker_color='#FF4500'
            ))
        
        else:
            # Fallback
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['Year'], y=df['Base_Value'],
                name='Données de base',
                line=dict(color='#1E90FF', width=2)
            ))
        
        fig.update_layout(
            height=350,
            template='plotly_white',
            showlegend=True,
            xaxis_title='Année',
            yaxis_title='Intensité relative'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_global_heatmap(self, analyzer):
        """Carte thermique globale"""
        # Simuler des données spatiales
        lat = np.linspace(-90, 90, 18)
        lon = np.linspace(-180, 180, 36)
        lat_grid, lon_grid = np.meshgrid(lat, lon)
        
        # Simulation de données
        base_temp = analyzer.config["base_value"]
        data = base_temp + 30 * np.sin(np.radians(lat_grid)) + np.random.normal(0, 5, lat_grid.shape)
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=lon[::2],
            y=lat[::2],
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            xaxis_title='Longitude',
            yaxis_title='Latitude'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_insights(self, df, analyzer):
        """Affiche les insights analytiques"""
        st.subheader("🎯 Insights et Analyses")
        
        # Calculer les métriques
        current_value = df['Base_Value'].iloc[-1]
        total_change = ((df['Base_Value'].iloc[-1] / df['Base_Value'].iloc[0]) - 1) * 100
        recent_change = ((df['Base_Value'].iloc[-1] / df[df['Year'] >= 2000]['Base_Value'].iloc[0]) - 1) * 100
        current_risk = df['Risk_Level'].iloc[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Points Clés")
            st.metric("Valeur Actuelle", f"{current_value:.1f} {analyzer.config['unit']}")
            st.metric("Changement depuis 1850", f"{total_change:+.1f}%")
            st.metric("Changement depuis 2000", f"{recent_change:+.1f}%")
            st.metric("Niveau de Risque Actuel", f"{current_risk:.0f}/100")
        
        with col2:
            st.markdown("### 🔍 Recommandations")
            
            if current_risk > 70:
                st.error("**Action Immédiate Requise** - Niveau de risque critique")
                st.write("• Renforcement des mesures d'urgence")
                st.write("• Surveillance accrue")
                st.write("• Plan d'action immédiat")
            elif current_risk > 40:
                st.warning("**Vigilance Renforcée** - Niveau de risque modéré")
                st.write("• Surveillance continue")
                st.write("• Planification d'actions préventives")
                st.write("• Préparation aux scénarios")
            else:
                st.success("**Situation Stable** - Niveau de risque acceptable")
                st.write("• Maintien de la surveillance")
                st.write("• Actions préventives recommandées")
                st.write("• Continuité des bonnes pratiques")
        
        # Alertes contextuelles
        st.markdown("### ⚠️ Alertes Contextuelles")
        
        if recent_change > 10:
            st.error(f"**ALERTE** - Augmentation rapide détectée: {recent_change:+.1f}% depuis 2000")
        elif recent_change > 5:
            st.warning(f"**Attention** - Augmentation modérée: {recent_change:+.1f}% depuis 2000")
        elif recent_change < -5:
            st.info(f"**Amélioration** - Tendances positives: {recent_change:+.1f}% depuis 2000")

def main():
    """Fonction principale pour lancer le dashboard Streamlit"""
    st.sidebar.title("🌍 Dashboard Terre")
    st.sidebar.markdown("""
    **Instructions:**
    1. Choisissez le type de données environnementales
    2. Ajustez les paramètres d'analyse
    3. Explorez les visualisations interactives
    
    **Données:** 1850-2025
    **Source:** Modèles climatiques simulés
    """)
    
    # Lancer le dashboard
    dashboard = EarthStreamlitDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()