<<<<<<< HEAD
# Gestion De Datos Proyecto
=======
# **📊 Dashboard Financiero COVID-19**

El proyecto tiene como objetivo aplicar los conocimientos adquiridos en el curso para procesar,
analizar y visualizar grandes volúmenes de datos reales, usando Python y librerías como Pandas,
NumPy, Matplotlib y Seaborn.

Se trabajo con los reportes diarios de COVID-19 publicados por la Johns Hopkins University (JHU
CSSE), disponibles en formato CSV dentro del repositorio.

Construido con **Python**, **Streamlit** y **Plotly**, diseñado para visualizar la evolución de la pandemia de COVID-19 con una estética financiera moderna y limpia.

## **🛠️ Guía de Instalación**

### **1\. Instalar Python**

Instalar Python en tu sistema.

1. Descarga la última versión desde [python.org](https://www.python.org/downloads/).
2. Ejecuta el instalador.

### **2\. Preparar el Proyecto**

1. Descarga este código en una carpeta de tu elección.
2. Abre la terminal (Símbolo del sistema, PowerShell o Terminal) y navega hasta esa carpeta:  
   cd ruta/a/tu/carpeta

### **3\. Crear un Entorno Virtual (Recomendado)**

Esto mantiene tu sistema limpio y evita conflictos con otras librerías.  
**En Windows:**

```Python
python -m venv venv
.\venv\Scripts\activate
```

```python
# En caso de no encontrar la carpeta Scripts
.\venv\bin\activate
```

**En macOS / Linux:**

```Python
python3 -m venv venv
source venv/bin/activate
```

_(Deberías ver (venv) al principio de la línea de comandos después de activar)._

### **4\. Instalar Dependencias Básicas**

Instala las librerías necesarias para ejecutar el dashboard con el siguiente comando:  
pip install streamlit pandas plotly numpy

## **📦 Instalación Completa de Dependencias (Para desarrollo y análisis adicionales)**

Si necesitas ejecutar scripts adicionales o trabajar con notebooks, instala estas dependencias extra:

### **1\. Comprobar Python y pip (asegúrate de usar el intérprete correcto)**

```Python
python --version
python -m pip --version
```

### **2\. Actualizar pip e instalar Streamlit en el entorno actual**

```
python -m pip install --upgrade pip
python -m pip install streamlit
```

### **3\. Ejecutar la app usando el módulo (evita depender del PATH)**

```Python
python -m streamlit run main.py
```

### **4\. Instalar módulo plotly (para ver los gráficos)**

```Python
python -m pip install plotly
```

### 5\. Librerías adicionales

Librerias necesarias para análisis de datos más profundos o ejecución de notebooks:

```
pip install ipykernel -U
python -m pip install ipykernel
python -m pip install pandas
python -m pip install numpy
python -m pip install seaborn
python -m pip install dask
pip install aiohttp -q
python -m pip install ydata_profiling
```

## **▶️ Cómo Ejecutar el Dashboard**

Una vez instalado todo, inicia la aplicación con este comando:

```python
streamlit run dashboard/main.py
```

- El navegador se abrirá automáticamente en http://localhost:8501.
- Si es la primera vez, tardará unos segundos en descargar los datos iniciales.

## **📂 Estructura del Código**

El proyecto está organizado para ser fácil de entender y modificar:

- **dashboard/main.py**: El cerebro de la aplicación. Conecta los datos, los cálculos y la interfaz.
- **dashboard/ui.py**: El diseñador. Contiene todo el HTML, CSS y componentes visuales (tarjetas, sidebar, gráficos).
- **dashboard/data.py**: El gestor de datos. Se encarga de descargar y limpiar la información de JHU.
- **dashboard/metrics.py**: El matemático. Calcula tendencias, picos y alertas de rebrote.

## **🐛 Solución de Problemas Comunes**

- **"streamlit no se reconoce como un comando..."**:
  - Asegúrate de haber activado el entorno virtual (venv).
  - Si estás en Windows, verifica que agregaste Python al PATH durante la instalación.
  - Prueba ejecutando: python -m streamlit run dashboard/main.py.
- **Error "ModuleNotFoundError":**
  - Te falta instalar alguna librería. Ejecuta de nuevo el paso 4 de la instalación o la sección de dependencias completa.
>>>>>>> dev
