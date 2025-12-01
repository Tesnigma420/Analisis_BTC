# BTC Sentinel 🛰️  
_Plataforma ligera de monitoreo de mercado BTC con enfoque en Ciencia de Datos y DevOps._

## 1. Descripción general

**BTC Sentinel** es un proyecto académico orientado a Ciencia de Datos aplicado a criptomonedas, cuyo objetivo es:

- **Recolectar periódicamente datos de precio de Bitcoin (BTC)** desde una API pública.
- **Almacenar el histórico de precios en un archivo CSV** para su análisis.
- **Generar interpretaciones y gráficas** a partir de ese histórico.
- **Enviar actualizaciones y visualizaciones a un bot de Telegram**, que funciona como canal principal de notificación.

El sistema está pensado para ejecutarse de forma automática en una **Raspberry Pi**, integrándose con una mini–pipeline de tipo DevOps (control de versiones, automatización básica y monitoreo simple).

---

## 2. Objetivo del proyecto

Implementar una plataforma sencilla pero completa que:

1. Demuestre el uso de **metodologías DevOps** en un caso práctico real.
2. Aplique conceptos de **Ciencia de Datos** sobre series de tiempo de BTC.
3. Ejecute de forma periódica y autónoma en un entorno físico (Raspberry Pi).
4. Entregue resultados claros al usuario final mediante un **bot de Telegram**.

---

## 3. Alcance (MVP)

Este proyecto se limita a:

- Una sola criptomoneda: **Bitcoin (BTC)**.
- Un flujo de trabajo básico:
  - Recolección de datos de precio.
  - Almacenamiento en CSV.
  - Cálculo de métricas simples.
  - Generación de una gráfica básica.
  - Envío de un reporte por Telegram.
- Ejecución periódica en una Raspberry Pi (por ejemplo, cada 30 o 60 minutos).

Fuera de alcance (para esta primera versión):

- Trading automático o ejecución de órdenes.
- Modelo avanzado de predicción (redes neuronales, modelos complejos).
- Dashboard web completo.
- Soporte multi–criptomoneda.

Estos puntos se consideran como **posibles extensiones futuras**.

---

## 4. Arquitectura general

A alto nivel, el sistema se compone de los siguientes bloques:

1. **Módulo de recolección (`collector`)**
   - Consulta una API pública para obtener el precio actual de BTC.
   - Registra los datos en un archivo CSV con la forma:
     ```text
     timestamp,price
     ```

2. **Módulo de análisis (`analysis`)**
   - Lee el CSV con el histórico de precios.
   - Calcula métricas básicas, por ejemplo:
     - Precio actual.
     - Variación porcentual respecto al valor anterior.
     - Media móvil simple sobre las últimas n observaciones.
   - Genera una **gráfica** (imagen PNG) de la serie de tiempo y la media móvil.

3. **Módulo de notificación (`notifier`)**
   - Construye un mensaje con las métricas calculadas.
   - Envía ese mensaje y la gráfica generada a un **chat de Telegram** usando un bot.

4. **Orquestador (`run`)**
   - Ejecuta en orden:
     1. Recolección de datos.
     2. Análisis y generación de gráfica.
     3. Envío de notificación.
   - Es el punto de entrada que se agenda en la Raspberry (por ejemplo, usando `cron`).

5. **Entorno de ejecución (Raspberry Pi)**
   - Dispositivo donde corre el sistema de manera autónoma.
   - Clona el repositorio, instala dependencias y ejecuta el script de orquestación en intervalos definidos.

---

## 5. Relación con la metodología DevOps

Este proyecto aplica la cultura DevOps de la siguiente manera:

- **Planificación:**  
  Definición clara del alcance, métricas a calcular y componentes del sistema.

- **Control de versiones (Code):**  
  Todo el código fuente se gestiona en un repositorio Git, con estructura modular y documentación asociada.

- **Construcción y pruebas (Build/Test):**  
  Se utilizarán dependencias declaradas en `requirements.txt` y pruebas unitarias básicas sobre el módulo de análisis.

- **Integración continua (CI):**  
  Una pipeline sencilla (por ejemplo, con GitHub Actions) ejecutará la instalación de dependencias y los tests en cada cambio.

- **Despliegue (Deploy):**  
  El proyecto se despliega en la Raspberry Pi mediante clonación/actualización del repositorio.

- **Operación (Operate):**  
  La Raspberry ejecuta `run.py` de manera periódica a través de un programa como `cron`.

- **Monitoreo (Monitor):**  
  Se generarán logs básicos y se utilizará el propio bot de Telegram como canal para detectar errores o comportamientos inesperados.

---

## 6. Tecnologías previstas

Las principales tecnologías y herramientas a utilizar son:

- **Lenguaje:** Python 3.x  
- **Librerías (previstas):**
  - `requests` – consumo de API de precios.
  - `pandas` – manejo del CSV e indicadores simples.
  - `matplotlib` – generación de gráficas.
  - Cliente HTTP o librería para la **API de Telegram**.
  - `pytest` – pruebas unitarias básicas.
- **Hardware:** Raspberry Pi (modelo compatible con Python 3).
- **Control de versiones:** Git + GitHub.
- **Automatización en servidor:** `cron` (Raspberry Pi).
- **CI/CD (mínimo):** GitHub Actions (flujo de instalación + tests).

---

## 7. Flujo de alto nivel

1. En el intervalo configurado:
   - La Raspberry ejecuta `run.py`.
2. `run.py` llama al módulo de recolección:
   - Se obtiene el precio actual de BTC y se registra en `data/btc_prices.csv`.
3. `run.py` llama al módulo de análisis:
   - Se leen los datos históricos.
   - Se calculan métricas y se produce una gráfica PNG.
4. `run.py` llama al módulo de notificación:
   - Se construye un mensaje con la interpretación de los datos.
   - Se envía el mensaje y la gráfica al chat de Telegram configurado.
5. Se registran logs de cada ejecución para seguimiento y depuración.

---

## 8. Estado del proyecto

- **Estado actual:**  
  En fase de diseño y documentación inicial (bloque de planificación y definición de alcance).

- **Próximos pasos inmediatos:**
  1. Definir estructura de directorios del repositorio.
  2. Crear el repositorio Git e inicializar `README.md`, `.gitignore` y `requirements.txt`.
  3. Implementar el módulo de recolección de datos de BTC.
  4. Implementar el módulo de análisis y generación de gráfica.
  5. Implementar el módulo de notificación a Telegram.
  6. Integrar todo en `run.py` y probar en la Raspberry.
  7. Configurar la ejecución periódica y una pipeline de CI básica.

---

## 9. Requisitos mínimos (desarrollo)

- Python 3.9+  
- Acceso a internet (para:
  - consultar API de precios BTC,
  - comunicarse con la API de Telegram).
- Cuenta de Telegram y un **bot token** válido (obtenido vía BotFather).
- Sistema operativo compatible con Python (para desarrollo local).
- Raspberry Pi para el entorno de despliegue final (opcional en desarrollo local, obligatorio para la versión final del proyecto).

---

Este documento se irá actualizando conforme se implementen los módulos y se agreguen detalles técnicos (como comandos específicos, ejemplos de ejecución y configuración de la Raspberry Pi).
