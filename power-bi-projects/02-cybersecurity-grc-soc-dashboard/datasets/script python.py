import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# 1. Tabla DIM_USUARIOS (150 empleados)
departamentos = ['Finanzas', 'TI', 'Recursos Humanos', 'Operaciones', 'Ventas', 'Legal']
usuarios = []
for i in range(1, 151):
    dept = random.choice(departamentos)
    es_admin = np.random.choice([True, False], p=[0.12, 0.88])
    mfa = np.random.choice([True, False], p=[0.92, 0.08]) if not es_admin else np.random.choice([True, False], p=[0.96, 0.04])
    sod_conflicto = np.random.choice([True, False], p=[0.15, 0.85]) if dept in ['Finanzas', 'Operaciones'] else False
    dias_sin_revision = random.randint(10, 180) if es_admin else random.randint(10, 90)
    usuarios.append([f'USR-{i:03d}', f'Usuario_{i}', dept, es_admin, mfa, sod_conflicto, dias_sin_revision])

df_usuarios = pd.DataFrame(usuarios, columns=['id_usuario', 'nombre', 'departamento', 'es_admin', 'mfa_activo', 'conflicto_sod', 'dias_ultima_revision'])

# 2. Tabla FACT_TICKETS_IAM (300 tickets en los últimos 6 meses)
fecha_base = datetime(2026, 6, 1)
tickets = []
tipos_ticket = ['Alta', 'Baja', 'Modificación']
for i in range(1, 301):
    usr = random.choice(df_usuarios['id_usuario'])
    tipo = np.random.choice(tipos_ticket, p=[0.4, 0.35, 0.25])
    f_creacion = fecha_base + timedelta(days=random.randint(0, 170), hours=random.randint(8, 18))
    sla_horas = 24 if tipo == 'Baja' else 48
    horas_resolucion = int(np.random.exponential(scale=22)) + 2
    f_cierre = f_creacion + timedelta(hours=horas_resolucion)
    tickets.append([f'TCK-{i:04d}', usr, tipo, f_creacion, f_cierre, sla_horas, horas_resolucion])

df_tickets = pd.DataFrame(tickets, columns=['id_ticket', 'id_usuario', 'tipo_solicitud', 'fecha_creacion', 'fecha_cierre', 'sla_objetivo_hs', 'horas_resolucion'])

# 3. Tabla FACT_VULNERABILIDADES (250 registros)
activos = ['SRV-ERP-01', 'SRV-DB-PROD', 'WEB-PORTAL', 'FW-PERIMETRAL', 'APP-COBRANZAS', 'SRV-AD-01']
severidades = ['Crítica', 'Alta', 'Media', 'Baja']
vulns = []
for i in range(1, 251):
    activo = random.choice(activos)
    sev = np.random.choice(severidades, p=[0.15, 0.30, 0.35, 0.20])
    f_det = fecha_base + timedelta(days=random.randint(0, 170))
    sla_dias = {'Crítica': 7, 'Alta': 15, 'Media': 30, 'Baja': 60}[sev]
    estado = np.random.choice(['Cerrada', 'Abierta'], p=[0.72, 0.28])
    dias_abierta = random.randint(2, 45)
    f_rem = (f_det + timedelta(days=dias_abierta)) if estado == 'Cerrada' else None
    vulns.append([f'VULN-{i:04d}', activo, sev, f_det, f_rem, sla_dias, estado])

df_vulns = pd.DataFrame(vulns, columns=['id_vuln', 'activo', 'severidad', 'fecha_deteccion', 'fecha_remediacion', 'sla_dias', 'estado'])

# 4. Tabla FACT_INCIDENTES_SOC (120 incidentes)
vectores = ['Phishing', 'Fuerza Bruta', 'Malware', 'Acceso No Autorizado', 'Exfiltración Sospechosa']
incidentes = []
for i in range(1, 121):
    usr = random.choice(df_usuarios['id_usuario'])
    vec = np.random.choice(vectores, p=[0.45, 0.25, 0.15, 0.10, 0.05])
    f_inc = fecha_base + timedelta(days=random.randint(0, 170))
    mttd_min = random.randint(5, 120)
    mttr_min = random.randint(15, 360)
    incidentes.append([f'INC-{i:03d}', usr, vec, f_inc, mttd_min, mttr_min])

df_incidentes = pd.DataFrame(incidentes, columns=['id_incidente', 'id_usuario', 'vector_ataque', 'fecha_incidente', 'mttd_minutos', 'mttr_minutos'])

# Exportar a CSV
df_usuarios.to_csv('dim_usuarios.csv', index=False)
df_tickets.to_csv('fact_tickets_iam.csv', index=False)
df_vulns.to_csv('fact_vulnerabilidades.csv', index=False)
df_incidentes.to_csv('fact_incidentes_soc.csv', index=False)
print("¡Archivos CSV generados con éxito!")
import os
print("Los archivos se guardaron en:", os.getcwd())