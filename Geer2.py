import csv
import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

# --- DICCIONARIO DE MATERIAS ---
SUBJECT_MAPPING = {
    'LC': 'Lengua Castellana y Literatura', 'MA': 'Matemáticas', 'GH': 'Geografía e Historia',
    'EFE': 'Educación Física', 'BG': 'Biología y Geología', 'EPVA': 'Educación Plástica, Visual y Audiovisual',
    'MUS': 'Música', 'ACS': 'Ámbito de Competencia Social', 'APR': 'Ámbito Práctico',
    'ACT': 'Ámbito Científico-Tecnológico', 'ASL': 'Ámbito Sociolingüístico', 'AC': 'Actividades Complementarias',
    'LEX (AL)': 'Lengua Extranjera (Alemán)', 'LEX (FR)': 'Lengua Extranjera (Francés)',
    'LEX (IN)': 'Lengua Extranjera (Inglés)', 'LEX (IA)': 'Lengua Extranjera (Inglés Avanzado)',
    'LEX (IT)': 'Lengua Extranjera (Italiano)', 'LEX (PO)': 'Lengua Extranjera (Portugués)',
    '2LE (AL)': 'Segunda Lengua Extranjera (Alemán)', '2LE (FR)': 'Segunda Lengua Extranjera (Francés)',
    '2LE (IN)': 'Segunda Lengua Extranjera (Inglés)', '2LE (IT)': 'Segunda Lengua Extranjera (Italiano)',
    '2LE (PO)': 'Segunda Lengua Extranjera (Portugués)', 'CCOM': 'Ciencias de la Computación',
    'DEP': 'Deporte', 'RLC': 'Refuerzo de Lengua Castellana y Literatura', 'RMA': 'Refuerzo de Matemáticas',
    'AE': 'Atención Educativa', 'RE (CA)': 'Religión (Católica)', 'RE (EV)': 'Religión (Evangélica)',
    'RE (IS)': 'Religión (Islámica)', 'RE (JU)': 'Religión (Judía)', 'FQE': 'Física y Química',
    'TEDI': 'Tecnología y Digitalización', 'EVCE': 'Educación en Valores Cívicos y Éticos',
    'TDMU': 'Taller de Música', 'ALS': 'Ámbito Lingüístico y Social', 'CUC': 'Cultura Clásica',
    'UE': 'Unión Europea', 'PICIT': 'Proy. invest. científica e innov. tecn.',
    'PHPC': 'Proy. historia y patrimonio cultural', 'PEEFCR': 'Proy. emprendimiento y educ. financiera',
    'PCIM': 'Proy. creación e investigación musical', 'PCAP': 'Proy. creación audiovisual y plástica',
    'POAT': 'Proy. oratoria, argumentación y teatro', 'PCDH': 'Proy. Convivencia y derechos humanos',
    'PROY': 'Proyecto', 'FOPP': 'Formación y Orientación Personal y Profesional', 'FIL': 'Filosofía',
    'MAA': 'Matemáticas A', 'MAB': 'Matemáticas B', 'DIG': 'Digitalización',
    'ECEM': 'Economía y Emprendimiento', 'EXAR': 'Expresión Artística', 'LAT': 'Latín',
    'TEC': 'Tecnología', 'EFB': 'Educación Física', 'FI': 'Filosofía', 'LC1': 'Lengua Cas. y Lit. I',
    'MA1': 'Matemáticas I', 'DT1': 'Dibujo Técnico I', 'FQB': 'Física y Química',
    'BGCA': 'Biología, Geología y C. Ambientales', 'TEIN1': 'Tecnología e Ingeniería I',
    'LEX1 (AL)': 'Lengua Ext. I (Alemán)', 'LEX1 (FR)': 'Lengua Ext. I (Francés)',
    'LEX1 (IN)': 'Lengua Ext. I (Inglés)', 'LEX1 (IA)': 'Lengua Ext. I (Inglés Av.)',
    'LEX1 (IT)': 'Lengua Ext. I (Italiano)', 'LEX1 (PO)': 'Lengua Ext. I (Portugués)',
    'DA1': 'Dibujo Artístico I', 'CAV': 'Cultura Audiovisual', 'HMC': 'Hª Mundo Contemporáneo',
    'LIU': 'Literatura Universal', 'VOL': 'Volumen', 'AM1': 'Análisis Musical I',
    'LPM': 'Lenguaje y Práctica Musical', '2LE1 (IN)': '2ª Lengua Ext. I (Inglés)',
    '2LE1 (FR)': '2ª Lengua Ext. I (Francés)', '2LE1 (AL)': '2ª Lengua Ext. I (Alemán)',
    '2LE1 (PO)': '2ª Lengua Ext. I (Portugués)', '2LE1 (IT)': '2ª Lengua Ext. I (Italiano)',
    'LA1': 'Latín I', 'EC': 'Economía', 'GR1': 'Griego I', 'MAS1': 'Mat. CCSS I',
    'PROYA': 'Proyectos Artísticos', 'DTAPD1': 'Dibujo Téc. Artes Plásticas I',
    'AES1': 'Artes Escénicas I', 'CTV1': 'Coro y Técnica Vocal I', 'MAGE': 'Matemáticas Generales',
    'ECEAE': 'Economía, Emprend. y Act. Empresarial', 'FLMGACT': 'Fund. Léxicos Grecolatinos',
    'CCOM1': 'Ciencias de la Comp.', 'MAE': 'Medidas de Atención Educativa',
    'RECA1': 'Religión (Católica)', 'REEV1': 'Religión (Evangélica)', 'REIS1': 'Religión (Islámica)',
    'REJU1': 'Religión (Judía)', 'HES': 'Historia de España', 'HFI': 'Historia de la Filosofía',
    'LCL2': 'Lengua Cas. y Lit. II', 'MA2': 'Matemáticas II', 'MAS2': 'Mat. CCSS II',
    'BIO': 'Biología', 'DT2': 'Dibujo Técnico II', 'FIS': 'Física', 'GCA': 'Geología y C. Ambientales',
    'QUI': 'Química', 'TEIN2': 'Tecnología e Ingeniería II', 'LEX2 (IA)': 'Lengua Ext. II (Inglés Av.)',
    'LEX2 (IN)': 'Lengua Ext. II (Inglés)', 'LEX2 (FR)': 'Lengua Ext. II (Francés)',
    'LEX2 (AL)': 'Lengua Ext. II (Alemán)', 'LEX2 (IT)': 'Lengua Ext. II (Italiano)',
    'LEX2 (PO)': 'Lengua Ext. II (Portugués)', '2LE2(FR)': '2ª Lengua Ext. II (Francés)',
    '2LE2(AL)': '2ª Lengua Ext. II (Alemán)', '2LE2(IT)': '2ª Lengua Ext. II (Italiano)',
    '2LE2(PO)': '2ª Lengua Ext. II (Portugués)', '2LE2(IN)': '2ª Lengua Ext. II (Inglés)',
    'DAR2': 'Dibujo Artístico II', 'DIS': 'Diseño', 'FUA': 'Fundamentos Artísticos',
    'TGP': 'Téc. Expresión Gráfico-Plástica', 'AM2': 'Análisis Musical II', 'AES2': 'Artes Escénicas II',
    'CTV2': 'Coro y Técnica Vocal II', 'HMD': 'Hª de la Música y de la Danza', 'LITDR': 'Literatura Dramática',
    'DTAPD2': 'Dibujo Téc. Artes Plásticas II', 'CG': 'Ciencias Generales', 'MCA': 'Mov. culturales y artísticos',
    'LA2': 'Latín II', 'EDMN': 'Empresa y Diseño Modelos Negocio', 'GE': 'Geografía',
    'GR2': 'Griego II', 'HA': 'Historia del Arte', 'CCOM2': 'Ciencias de la Comp.',
    'FAG': 'Fund. Admin. y Gestión', 'PSI': 'Psicología', 'RECA2': 'Religión (Católica)',
    'REEV2': 'Religión (Evangélica)', 'REIS2': 'Religión (Islámica)', 'REJU2': 'Religión (Judía)',
    'EST': 'Estudio'
}

def get_subject_name(abbr):
    return SUBJECT_MAPPING.get(abbr, abbr)

def analyze_csv(file_path):
    # Inicialización de estructuras de datos
    materias = [] 
    alumnado = [] 
    tramos_suspensos = [0, 0, 0, 0]
    tramos_media = [0, 0, 0, 0, 0]
    suma_suspensos_total = 0
    total_alumnos = 0
    
    try:
        with open(file_path, newline='', encoding='cp1252') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            if not rows:
                print(f"Skipping empty file: {file_path}")
                return None

            headers = rows[0]
            if headers[0] != "Alumno/a":
                print(f"Skipping invalid format: {file_path}")
                return None

            # Inicializar materias
            for h in headers[1:]:
                materias.append({'abbr': h, 'count': 0, 'sum': 0, 'passed': 0, 'others': 0})

            # Procesar alumnos
            for row in rows[1:]:
                nombre_alumno = row[0]
                suma_calific_alum = 0
                cuenta_calific_alum = 0
                cuenta_suspensos = 0
                
                for i, cell in enumerate(row[1:]):
                    if i >= len(materias): break 
                    
                    val_str = cell.strip()
                    materia_idx = i
                    val_num = 0
                    is_numeric = False
                    
                    if val_str.isdigit():
                        val_num = int(val_str)
                        is_numeric = True
                    
                    if is_numeric:
                        materias[materia_idx]['count'] += 1
                        materias[materia_idx]['sum'] += val_num
                        suma_calific_alum += val_num
                        cuenta_calific_alum += 1
                        
                        if val_num > 4:
                            materias[materia_idx]['passed'] += 1
                        else:
                            cuenta_suspensos += 1
                    else:
                        if val_str == '10-M':
                            materias[materia_idx]['count'] += 1
                            materias[materia_idx]['sum'] += 10
                            materias[materia_idx]['passed'] += 1
                            suma_calific_alum += 10
                            cuenta_calific_alum += 1
                        elif val_str in ['NP', 'NE']:
                            materias[materia_idx]['others'] += 1
                            cuenta_suspensos += 1
                        elif len(val_str) > 2:
                            materias[materia_idx]['others'] += 1
                
                nota_media = 0.0
                if cuenta_calific_alum > 0:
                    nota_media = suma_calific_alum / cuenta_calific_alum
                
                alumnado.append({'name': nombre_alumno, 'media': nota_media})
                
                # Tramos Media
                if nota_media >= 9: tramos_media[4] += 1
                elif nota_media >= 7: tramos_media[3] += 1
                elif nota_media >= 5: tramos_media[2] += 1
                elif nota_media >= 2.5: tramos_media[1] += 1
                else: tramos_media[0] += 1
                
                # Tramos Suspensos
                if cuenta_suspensos > 4: tramos_suspensos[3] += 1
                elif cuenta_suspensos >= 3: tramos_suspensos[2] += 1
                elif cuenta_suspensos >= 1: tramos_suspensos[1] += 1
                else: tramos_suspensos[0] += 1
                
                suma_suspensos_total += cuenta_suspensos
                total_alumnos += 1

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    return {
        'materias': materias,
        'alumnado': alumnado,
        'tramos_suspensos': tramos_suspensos,
        'tramos_media': tramos_media,
        'suma_suspensos_total': suma_suspensos_total,
        'total_alumnos': total_alumnos
    }

def create_pdf(data, output_filename, title_text="Estadísticas de Evaluación"):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # --- Estilos ---
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Heading2'], spaceAfter=10, textColor=colors.HexColor('#363636'))
    normal_style = styles['Normal']
    # Estilo para el footer solicitado
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=8, textColor=colors.grey)
    
    # Título y Resumen
    elements.append(Paragraph(title_text, title_style))
    resumen_text = f"{data['total_alumnos']} alumnos y alumnas - {len(data['materias'])} materias, ámbitos o módulos."
    elements.append(Paragraph(resumen_text, normal_style))
    elements.append(Spacer(1, 10))

    # Tabla Materias
    table_data = [["Materia", "Alum.\nCalif.", "Calif.\nMedia", "Superan\n(Nº)", "Superan\n(%)", "No Sup.\n(Nº)", "No Sup.\n(%)", "Otros"]]
    suma_porcentaje_superan = 0
    
    for m in data['materias']:
        if m['count'] > 0:
            media = m['sum'] / m['count']
            pct_superan = (m['passed'] * 100) / m['count']
            suma_porcentaje_superan += pct_superan
            pct_no_superan = 100 - pct_superan
            row = [get_subject_name(m['abbr']), m['count'], f"{media:.2f}", m['passed'], f"{round(pct_superan)}%", (m['count'] - m['passed']), f"{round(pct_no_superan)}%", m['others']]
        else:
            row = [get_subject_name(m['abbr']), 0, "-", "-", "-", "-", "-", "-"]
        table_data.append(row)

    t_materias = Table(table_data, colWidths=[200, 40, 40, 40, 40, 40, 40, 40])
    t_materias.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    # Zebra striping
    for i in range(1, len(table_data)):
        if i % 2 == 0: t_materias.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.whitesmoke)]))
    elements.append(t_materias)
    elements.append(Spacer(1, 20))

    # Tablas Distribución
    elements.append(Paragraph("Alumnado por número de suspensos:", subtitle_style))
    ts = data['tramos_suspensos']
    tot = data['total_alumnos'] if data['total_alumnos'] > 0 else 1
    p_susp_5 = round(ts[3]*100/tot)
    p_susp_3 = round(ts[2]*100/tot)
    p_susp_1 = round(ts[1]*100/tot)
    p_susp_0 = 100 - (p_susp_5 + p_susp_3 + p_susp_1)
    if p_susp_0 < 0: p_susp_0 = 0

    ts_data = [
        ["5 o más suspensos", ts[3], f"{p_susp_5}%"],
        ["3 o 4 suspensos", ts[2], f"{p_susp_3}%"],
        ["1 o 2 suspensos", ts[1], f"{p_susp_1}%"],
        ["Todo superado", ts[0], f"{p_susp_0}%"]
    ]
    t_suspensos = Table(ts_data, colWidths=[150, 50, 50], hAlign='LEFT')
    t_suspensos.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(t_suspensos)
    elements.append(Spacer(1, 10))
    
    media_suspensos = data['suma_suspensos_total'] / tot if tot > 0 else 0
    media_pct_superan = suma_porcentaje_superan / len(data['materias']) if len(data['materias']) > 0 else 0
    elements.append(Paragraph(f"Media de suspensos por alumno/a: {media_suspensos:.2f}", normal_style))
    elements.append(Paragraph(f"Media de % de alumnado que supera materias: {media_pct_superan:.2f}%", normal_style))
    elements.append(Spacer(1, 20))
    
    # Ranking
    elements.append(Paragraph("Materias ordenadas por porcentaje de superación:", subtitle_style))
    materias_sort = []
    for m in data['materias']:
        if m['count'] > 0:
            pct = (m['passed'] * 100) / m['count']
            materias_sort.append({'name': get_subject_name(m['abbr']), 'pct': pct})
    materias_sort.sort(key=lambda x: x['pct'], reverse=True)
    
    rank_data = []
    for m in materias_sort:
        desv = m['pct'] - media_pct_superan
        rank_data.append([m['name'], f"Supera el {m['pct']:.1f}%", f"desv. {desv:+.2f}%"])
    t_rank = Table(rank_data, colWidths=[250, 100, 100], hAlign='LEFT')
   #t_medias.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    t_rank.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    #t_rank.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 9)]))
    elements.append(t_rank)
    elements.append(Spacer(1, 20))
    
    # Medias
    elements.append(Paragraph("Distribución de alumnado por media de calificaciones:", subtitle_style))
    tm = data['tramos_media']
    pm_0 = round(tm[0]*100/tot)
    pm_1 = round(tm[1]*100/tot)
    pm_2 = round(tm[2]*100/tot)
    pm_3 = round(tm[3]*100/tot)
    pm_4 = 100 - (pm_0 + pm_1 + pm_2 + pm_3)
    if pm_4 < 0: pm_4 = 0
    tm_data = [
        ["Media [0, 2.5)", tm[0], f"{pm_0}%"],
        ["Media [2.5, 5)", tm[1], f"{pm_1}%"],
        ["Media [5, 7)", tm[2], f"{pm_2}%"],
        ["Media [7, 9)", tm[3], f"{pm_3}%"],
        ["Media [9, 10]", tm[4], f"{pm_4}%"]
    ]
    t_medias = Table(tm_data, colWidths=[150, 50, 50], hAlign='LEFT')
    t_medias.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(t_medias)
    elements.append(Spacer(1, 20))
    
    # Mejores alumnos
    elements.append(Paragraph("Alumnado con mejor media:", subtitle_style))
    alumnado_sorted = sorted(data['alumnado'], key=lambda x: x['media'], reverse=True)
    limit = 10 if tot > 40 else 5
    limit = min(limit, len(alumnado_sorted))
    best_data = []
    for i in range(limit):
        alum = alumnado_sorted[i]
        best_data.append([alum['name'], f"{alum['media']:.2f}"])
    t_best = Table(best_data, colWidths=[250, 60], hAlign='LEFT')
    
    t_best.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(t_best)

    # --- PIE DE PÁGINA REQUERIDO ---
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Generado con GEEr v2.0.2", footer_style))

    doc.build(elements)
    print(f"OK: {output_filename}")

def process_file_or_directory(path_input):
    if os.path.isfile(path_input):
        # Modo fichero único
        if path_input.lower().endswith(".csv"):
            process_single_file(path_input)
        else:
            print("El archivo indicado no es un .csv")
    elif os.path.isdir(path_input):
        # Modo directorio (recursivo)
        print(f"Procesando directorio: {path_input} ...")
        count = 0
        for root, dirs, files in os.walk(path_input):
            for file in files:
                if file.lower().endswith(".csv"):
                    full_path = os.path.join(root, file)
                    process_single_file(full_path)
                    count += 1
        print(f"Procesamiento completado. {count} ficheros generados.")
    else:
        print("La ruta especificada no existe.")

def process_single_file(csv_path):
    # Generar nombre de salida: mismo nombre, extensión .pdf
    base_name = os.path.splitext(csv_path)[0]
    pdf_path = base_name + ".pdf"
    
    # Nombre del archivo para el título del PDF
    file_name_only = os.path.basename(base_name)
    
    data = analyze_csv(csv_path)
    if data:
        create_pdf(data, pdf_path, title_text=f"{file_name_only}")

# --- MAIN ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python geer_converter_v2.py <archivo.csv | carpeta>")
    else:
        user_input = sys.argv[1]
        process_file_or_directory(user_input)
