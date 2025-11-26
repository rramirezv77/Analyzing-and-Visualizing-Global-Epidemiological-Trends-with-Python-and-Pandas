import streamlit as st
import pandas as pd

# caché para velocidad
@st.cache_data(ttl=3600)
def load_data_simple():
    """
    Carga datos optimizada y asigna continentes a TODOS los países.
    """
    base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
    
    def fetch_and_melt(filename, value_name):
        url = f"{base_url}{filename}"
        try:
            df = pd.read_csv(url)
            df = df.drop(columns=['Lat', 'Long', 'Province/State'])
            df = df.groupby('Country/Region').sum().reset_index()
            df_melted = df.melt(id_vars=['Country/Region'], var_name='date', value_name=value_name)
            df_melted['date'] = pd.to_datetime(df_melted['date'])
            return df_melted
        except Exception as e:
            st.error(f"Error cargando {filename}: {e}")
            return pd.DataFrame()

    # 1. Carga
    df_confirmed = fetch_and_melt("time_series_covid19_confirmed_global.csv", "confirmed")
    df_deaths = fetch_and_melt("time_series_covid19_deaths_global.csv", "deceased")
    df_recovered = fetch_and_melt("time_series_covid19_recovered_global.csv", "recovered")

    # 2. Fusión
    if df_confirmed.empty: return pd.DataFrame()
    
    df_final = pd.merge(df_confirmed, df_deaths, on=['Country/Region', 'date'], how='left')
    df_final = pd.merge(df_final, df_recovered, on=['Country/Region', 'date'], how='left')
    
    df_final.rename(columns={'Country/Region': 'country'}, inplace=True)
    df_final = df_final.fillna(0)
    
    # 3. Filtrado de Fechas (Enero 2020 - Junio 2021)
    mask = (df_final['date'] >= '2020-01-22') & (df_final['date'] <= '2021-06-30')
    df_final = df_final[mask]

    # 4. Cálculos
    df_final['active'] = df_final['confirmed'] - df_final['deceased'] - df_final['recovered']
    df_final['active'] = df_final['active'].clip(lower=0)

    # 5. Mapeo Completo de Continentes
    continent_map = {
        # North America
        'US': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
        'Antigua and Barbuda': 'North America', 'Bahamas': 'North America', 'Barbados': 'North America',
        'Belize': 'North America', 'Costa Rica': 'North America', 'Cuba': 'North America',
        'Dominica': 'North America', 'Dominican Republic': 'North America', 'El Salvador': 'North America',
        'Grenada': 'North America', 'Guatemala': 'North America', 'Haiti': 'North America',
        'Honduras': 'North America', 'Jamaica': 'North America', 'Nicaragua': 'North America',
        'Panama': 'North America', 'Saint Kitts and Nevis': 'North America', 'Saint Lucia': 'North America',
        'Saint Vincent and the Grenadines': 'North America', 'Trinidad and Tobago': 'North America',
        
        # South America
        'Argentina': 'South America', 'Bolivia': 'South America', 'Brazil': 'South America',
        'Chile': 'South America', 'Colombia': 'South America', 'Ecuador': 'South America',
        'Guyana': 'South America', 'Paraguay': 'South America', 'Peru': 'South America',
        'Suriname': 'South America', 'Uruguay': 'South America', 'Venezuela': 'South America',
        
        # Europe
        'Albania': 'Europe', 'Andorra': 'Europe', 'Armenia': 'Europe', 'Austria': 'Europe',
        'Azerbaijan': 'Europe', 'Belarus': 'Europe', 'Belgium': 'Europe', 'Bosnia and Herzegovina': 'Europe',
        'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Cyprus': 'Europe', 'Czechia': 'Europe',
        'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe', 'France': 'Europe',
        'Georgia': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe',
        'Iceland': 'Europe', 'Ireland': 'Europe', 'Italy': 'Europe', 'Kazakhstan': 'Europe',
        'Kosovo': 'Europe', 'Latvia': 'Europe', 'Liechtenstein': 'Europe', 'Lithuania': 'Europe',
        'Luxembourg': 'Europe', 'Malta': 'Europe', 'Moldova': 'Europe', 'Monaco': 'Europe',
        'Montenegro': 'Europe', 'Netherlands': 'Europe', 'North Macedonia': 'Europe', 'Norway': 'Europe',
        'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe', 'Russia': 'Europe',
        'San Marino': 'Europe', 'Serbia': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe',
        'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe', 'Turkey': 'Europe',
        'Ukraine': 'Europe', 'United Kingdom': 'Europe', 'Holy See': 'Europe',
        
        # Asia
        'Afghanistan': 'Asia', 'Bahrain': 'Asia', 'Bangladesh': 'Asia', 'Bhutan': 'Asia',
        'Brunei': 'Asia', 'Burma': 'Asia', 'Cambodia': 'Asia', 'China': 'Asia',
        'East Timor': 'Asia', 'India': 'Asia', 'Indonesia': 'Asia', 'Iran': 'Asia',
        'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia', 'Jordan': 'Asia',
        'Korea, North': 'Asia', 'Korea, South': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia',
        'Laos': 'Asia', 'Lebanon': 'Asia', 'Malaysia': 'Asia', 'Maldives': 'Asia',
        'Mongolia': 'Asia', 'Nepal': 'Asia', 'Oman': 'Asia', 'Pakistan': 'Asia',
        'Philippines': 'Asia', 'Qatar': 'Asia', 'Saudi Arabia': 'Asia', 'Singapore': 'Asia',
        'Sri Lanka': 'Asia', 'Syria': 'Asia', 'Taiwan*': 'Asia', 'Tajikistan': 'Asia',
        'Thailand': 'Asia', 'Timor-Leste': 'Asia', 'United Arab Emirates': 'Asia', 'Uzbekistan': 'Asia',
        'Vietnam': 'Asia', 'Yemen': 'Asia',
        
        # Africa
        'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
        'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cabo Verde': 'Africa', 'Cameroon': 'Africa',
        'Central African Republic': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa',
        'Congo (Brazzaville)': 'Africa', 'Congo (Kinshasa)': 'Africa', 'Cote d\'Ivoire': 'Africa',
        'Djibouti': 'Africa', 'Egypt': 'Africa', 'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa',
        'Eswatini': 'Africa', 'Ethiopia': 'Africa', 'Gabon': 'Africa', 'Gambia': 'Africa',
        'Ghana': 'Africa', 'Guinea': 'Africa', 'Guinea-Bissau': 'Africa', 'Kenya': 'Africa',
        'Lesotho': 'Africa', 'Liberia': 'Africa', 'Libya': 'Africa', 'Madagascar': 'Africa',
        'Malawi': 'Africa', 'Mali': 'Africa', 'Mauritania': 'Africa', 'Mauritius': 'Africa',
        'Morocco': 'Africa', 'Mozambique': 'Africa', 'Namibia': 'Africa', 'Niger': 'Africa',
        'Nigeria': 'Africa', 'Rwanda': 'Africa', 'Sao Tome and Principe': 'Africa', 'Senegal': 'Africa',
        'Seychelles': 'Africa', 'Sierra Leone': 'Africa', 'Somalia': 'Africa', 'South Africa': 'Africa',
        'South Sudan': 'Africa', 'Sudan': 'Africa', 'Tanzania': 'Africa', 'Togo': 'Africa',
        'Tunisia': 'Africa', 'Uganda': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
        
        # Oceania
        'Australia': 'Oceania', 'Fiji': 'Oceania', 'Kiribati': 'Oceania', 'Marshall Islands': 'Oceania',
        'Micronesia': 'Oceania', 'New Zealand': 'Oceania', 'Palau': 'Oceania', 'Papua New Guinea': 'Oceania',
        'Samoa': 'Oceania', 'Solomon Islands': 'Oceania', 'Tonga': 'Oceania', 'Vanuatu': 'Oceania'
    }
    
    def get_continent(country):
        return continent_map.get(country, 'Other')

    df_final['continent'] = df_final['country'].apply(get_continent)
    
    return df_final