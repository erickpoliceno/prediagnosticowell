"""
Dashboard ODS - Projeto Bússola WELL
Versão v13 - Corrigida
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging
from datetime import datetime
import os
import glob
import base64
import requests
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Dashboard ODS - Projeto Bússola WELL",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Link de Download Direto do Google Drive
GDRIVE_FILE_ID = "1QCa7GX6z2SJNINK2c1G9TelULaSA0LTJ"
EXCEL_URL = f"https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}"

# Paleta de Cores Personalizada (Gradiente Amarelo, Detalhes Azul-Petróleo)
PRIMARY_GRADIENT = "linear-gradient(90deg, #FFD700 0%, #FFA500 100%)"  # Gradiente amarelo
PRIMARY_COLOR = "#005F6B"  # Azul-Petróleo para detalhes e elementos secundários
SECONDARY_COLOR = "#FFD700"  # Amarelo dourado
STATUS_GREEN = "#16a34a"  # Bom
STATUS_ORANGE = "#d97706"  # Regular
STATUS_RED = "#dc2626"  # Crítico
BACKGROUND_COLOR = "white"
BACKGROUND_LIGHT = "#f8fafc"
TEXT_DARK = "#333"
TEXT_LIGHT = "#fff"

# Definições dos ODS COM JUSTIFICATIVAS INTEGRADAS
ODS_DEFINITIONS = {
    1: {
        "nome": "Erradicação da Pobreza", 
        "cor": "#E5243B", 
        "meta": "Acabar com a pobreza em todas as suas formas, em todos os lugares", 
        "justificativa": "Necessário reduzir significativamente a proporção de homens, mulheres e crianças de todas as idades que vivem na pobreza em todas as suas dimensões, de acordo com as definições nacionais",
        "icone": "🏠"
    },
    2: {
        "nome": "Fome Zero e Agricultura Sustentável", 
        "cor": "#DDA63A", 
        "meta": "Acabar com a fome, alcançar a segurança alimentar e melhoria da nutrição e promover a agricultura sustentável", 
        "justificativa": "Fundamental garantir acesso de todas as pessoas a alimentos seguros, nutritivos e suficientes durante todo o ano, especialmente para populações vulneráveis",
        "icone": "🌾"
    },
    3: {
        "nome": "Saúde e Bem-Estar", 
        "cor": "#4C9F38", 
        "meta": "Assegurar uma vida saudável e promover o bem-estar para todos, em todas as idades", 
        "justificativa": "Essencial reduzir a mortalidade materna e infantil, combater doenças transmissíveis e garantir acesso universal aos serviços de saúde",
        "icone": "🏥"
    },
    4: {
        "nome": "Educação de Qualidade", 
        "cor": "#C5192D", 
        "meta": "Assegurar a educação inclusiva e equitativa e de qualidade, e promover oportunidades de aprendizagem ao longo da vida para todos", 
        "justificativa": "Crucial garantir que todas as crianças completem o ensino primário e secundário gratuito, equitativo e de qualidade",
        "icone": "📚"
    },
    5: {
        "nome": "Igualdade de Gênero", 
        "cor": "#FF3A21", 
        "meta": "Alcançar a igualdade de gênero e empoderar todas as mulheres e meninas", 
        "justificativa": "Importante eliminar todas as formas de discriminação e violência contra mulheres e meninas, promovendo participação plena na vida política e econômica",
        "icone": "⚖️"
    },
    6: {
        "nome": "Água Limpa e Saneamento", 
        "cor": "#26BDE2", 
        "meta": "Assegurar a disponibilidade e gestão sustentável da água e saneamento para todos", 
        "justificativa": "Vital alcançar acesso universal e equitativo à água potável segura e ao saneamento adequado para todos",
        "icone": "💧"
    },
    7: {
        "nome": "Energia Limpa e Acessível", 
        "cor": "#FCC30B", 
        "meta": "Assegurar o acesso confiável, sustentável, moderno e a preço acessível à energia para todos", 
        "justificativa": "Necessário garantir acesso universal a serviços de energia modernos, confiáveis e sustentáveis a preços acessíveis",
        "icone": "⚡"
    },
    8: {
        "nome": "Trabalho Decente e Crescimento Econômico", 
        "cor": "#A21942", 
        "meta": "Promover o crescimento econômico sustentado, inclusivo e sustentável, emprego pleno e produtivo e trabalho decente para todos", 
        "justificativa": "Fundamental promover políticas que apoiem atividades produtivas, criação de emprego decente, empreendedorismo e inovação",
        "icone": "💼"
    },
    9: {
        "nome": "Indústria, Inovação e Infraestrutura", 
        "cor": "#FD6925", 
        "meta": "Construir infraestruturas resilientes, promover a industrialização inclusiva e sustentável e fomentar a inovação", 
        "justificativa": "Essencial desenvolver infraestrutura de qualidade, confiável, sustentável e resiliente para apoiar o desenvolvimento econômico e bem-estar humano",
        "icone": "🏭"
    },
    10: {
        "nome": "Redução das Desigualdades", 
        "cor": "#DD1367", 
        "meta": "Reduzir a desigualdade dentro dos países e entre eles", 
        "justificativa": "Importante alcançar e sustentar o crescimento da renda dos 40% mais pobres da população a uma taxa maior que a média nacional",
        "icone": "📊"
    },
    11: {
        "nome": "Cidades e Comunidades Sustentáveis", 
        "cor": "#FD9D24", 
        "meta": "Tornar as cidades e os assentamentos humanos inclusivos, seguros, resilientes e sustentáveis", 
        "justificativa": "Crucial garantir acesso de todos à habitação segura, adequada e a preço acessível, e aos serviços básicos e urbanizar as favelas",
        "icone": "🏙️"
    },
    12: {
        "nome": "Consumo e Produção Responsáveis", 
        "cor": "#BF8B2E", 
        "meta": "Assegurar padrões de produção e de consumo sustentáveis", 
        "justificativa": "Necessário alcançar gestão sustentável e uso eficiente dos recursos naturais, reduzindo pela metade o desperdício de alimentos per capita mundial",
        "icone": "♻️"
    },
    13: {
        "nome": "Ação Contra a Mudança Global do Clima", 
        "cor": "#3F7E44", 
        "meta": "Tomar medidas urgentes para combater a mudança climática e seus impactos", 
        "justificativa": "Urgente integrar medidas da mudança do clima nas políticas, estratégias e planejamentos nacionais",
        "icone": "🌍"
    },
    14: {
        "nome": "Vida na Água", 
        "cor": "#0A97D9", 
        "meta": "Conservação e uso sustentável dos oceanos, dos mares e dos recursos marinhos para o desenvolvimento sustentável", 
        "justificativa": "Vital prevenir e reduzir significativamente a poluição marinha de todos os tipos, especialmente a advinda de atividades terrestres",
        "icone": "🐠"
    },
    15: {
        "nome": "Vida Terrestre", 
        "cor": "#56C02B", 
        "meta": "Proteger, recuperar e promover o uso sustentável dos ecossistemas terrestres, gerir de forma sustentável as florestas, combater a desertificação, deter e reverter a degradação da terra e deter a perda de biodiversidade", 
        "justificativa": "Essencial assegurar a conservação, recuperação e uso sustentável de ecossistemas terrestres e de água doce interiores",
        "icone": "🌳"
    },
    16: {
        "nome": "Paz, Justiça e Instituições Eficazes", 
        "cor": "#00689D", 
        "meta": "Promover sociedades pacíficas e inclusivas para o desenvolvimento sustentável, proporcionar o acesso à justiça para todos e construir instituições eficazes, responsáveis e inclusivas em todos os níveis", 
        "justificativa": "Fundamental reduzir significativamente todas as formas de violência e as taxas de mortalidade relacionada em todos os lugares",
        "icone": "⚖️"
    },
    17: {
        "nome": "Parcerias e Meios de Implementação", 
        "cor": "#19486A", 
        "meta": "Fortalecer os meios de implementação e revitalizar a parceria global para o desenvolvimento sustentável", 
        "justificativa": "Importante fortalecer a mobilização de recursos internos para melhorar a capacidade nacional de arrecadação de impostos e outras receitas",
        "icone": "🤝"
    }
}

def get_base64_of_bin_file(bin_file):
    """Converte arquivo binário para base64"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def format_number(value, decimal_places=2):
    """Formata números usando vírgula como separador decimal e ponto como separador de milhares"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        # Converter para float se necessário
        if isinstance(value, str):
            # Remover caracteres não numéricos exceto pontos e vírgulas
            clean_value = ''.join(c for c in value if c.isdigit() or c in '.,')
            if ',' in clean_value and '.' in clean_value:
                # Se tem ambos, assumir formato americano (ponto decimal)
                clean_value = clean_value.replace(',', '')
            elif ',' in clean_value:
                # Se só tem vírgula, pode ser decimal ou separador de milhares
                parts = clean_value.split(',')
                if len(parts) == 2 and len(parts[1]) <= 2:
                    # Provavelmente decimal
                    clean_value = clean_value.replace(',', '.')
                else:
                    # Provavelmente separador de milhares
                    clean_value = clean_value.replace(',', '')
            
            value = float(clean_value)
        
        # Formatar com vírgula decimal e ponto para milhares
        if decimal_places == 0:
            formatted = f"{value:,.0f}"
        else:
            formatted = f"{value:,.{decimal_places}f}"
        
        # Trocar ponto e vírgula para padrão brasileiro
        formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
        
        return formatted
    except:
        return str(value)

def format_currency(value):
    """Formata valores monetários em reais"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        formatted = format_number(value, 2)
        return f"R$ {formatted}"
    except:
        return f"R$ {value}"

def format_percentage(value):
    """Formata valores como percentual"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        # Se valor está entre 0-1, converter para percentual
        if 0 <= value <= 1:
            value = value * 100
        
        formatted = format_number(value, 2)
        return f"{formatted}%"
    except:
        return f"{value}%"

class ODSDataManager:
    """Classe responsável pelo gerenciamento e carregamento de dados"""
    
    # CORREÇÃO 2: Adicionando cache de dados
    @st.cache_data(ttl=600)
    @staticmethod
    def load_data() -> Dict[str, Any]:
        """Carrega dados do arquivo Excel com mapeamento correto de colunas"""
        try:
            logger.info("Fazendo download da planilha do Google Drive...")
            
            # Faz o download da planilha online
            resposta = requests.get(EXCEL_URL)
            if resposta.status_code != 200:
                st.error("❌ Não foi possível ler a planilha do Google Drive. O link está público?")
                return {}
            
            # Ler o arquivo baixado diretamente para a memória do site
            excel_data = pd.read_excel(BytesIO(resposta.content), sheet_name=None)
            
            # Processar cada aba
            df_ods = ODSDataManager._process_ods_municipios(excel_data.get('ODS_Municipios', pd.DataFrame()))
            df_well = ODSDataManager._process_metodo_well(excel_data.get('Metodo_Well', pd.DataFrame()))
            df_connection = ODSDataManager._process_well_ods_connection(excel_data.get('Well_ODS_Connection', pd.DataFrame()))
            
            # NOVO: Processar abas com dados reais
            df_tabela_geral = ODSDataManager._process_tabela_geral(excel_data.get('TabelaGeral', pd.DataFrame()))
            df_dados_comparacao = ODSDataManager._process_dados_tabela_din(excel_data.get('Dados_Tabela_Din', pd.DataFrame()))
            
            # NOVO: Processar aba de imagens (com fallback para diferentes nomes)
            df_imagens = ODSDataManager._process_imagens_ods(excel_data)
            
            # CORRIGIDO: Processar aba ODS_Completo para justificativas com método específico
            df_ods_completo = ODSDataManager._process_ods_completo(excel_data.get('ODS_Completo', pd.DataFrame()))
            
            # Testar justificativas após carregamento
            data_temp = {'ods_completo': df_ods_completo}
            ODSDataManager.testar_justificativas(data_temp)
            
            return {
                'ods_municipios': df_ods,
                'metodo_well': df_well,
                'well_ods_connection': df_connection,
                'tabela_geral': df_tabela_geral,
                'dados_comparacao': df_dados_comparacao,
                'imagens_ods': df_imagens,
                'ods_completo': df_ods_completo,
                'raw_data': excel_data,
                'last_update': datetime.now(),
                'file_path': 'Google Drive (Nuvem)',
                'file_modified_time': datetime.now()
            }
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados do Drive: {str(e)}")
            logger.error(f"Erro no carregamento: {str(e)}")
            return {}
    
    @staticmethod
    def _process_ods_completo(df_raw: pd.DataFrame) -> pd.DataFrame:
        """CORRIGIDO: Processa dados da aba ODS_Completo com range específico (linhas 6-22, coluna K)"""
        if df_raw.empty:
            return pd.DataFrame()
        
        logger.info(f"Processando ODS_Completo - Shape: {df_raw.shape}")
        
        try:
            # CORREÇÃO: Ler especificamente as linhas 6-22 (índices 5-21 no pandas)
            # Linha 6 = ODS 1, Linha 7 = ODS 2, ..., Linha 22 = ODS 17
            
            if len(df_raw) < 22:
                logger.warning(f"Planilha tem apenas {len(df_raw)} linhas, esperado pelo menos 22")
                return pd.DataFrame()
            
            # Extrair dados das linhas 6-22 (índices 5-21)
            df_justificativas = df_raw.iloc[5:22].copy()  # Linhas 6-22
            
            # Criar estrutura padronizada
            dados_processados = []
            
            for i, (idx, row) in enumerate(df_justificativas.iterrows()):
                ods_numero = i + 1  # ODS 1-17
                
                # Buscar justificativa na coluna K (índice 10, pois K é a 11ª coluna)
                justificativa = ""
                
                # Tentar diferentes formas de acessar a coluna K
                if len(row) > 10:  # Verificar se tem coluna K (índice 10)
                    justificativa = row.iloc[10]  # Coluna K
                
                # Se não encontrou por índice, tentar por nome da coluna
                if (pd.isna(justificativa) or justificativa == "") and 'Justificativa_ODS' in df_raw.columns:
                    justificativa = row.get('Justificativa_ODS', "")
                
                # Limpar e validar justificativa
                if pd.notna(justificativa):
                    justificativa = str(justificativa).strip()
                else:
                    justificativa = ""
                
                dados_processados.append({
                    'ODS_Numero': ods_numero,
                    'Justificativa_ODS': justificativa,
                    'Linha_Original': idx + 1  # Para debug
                })
            
            df_resultado = pd.DataFrame(dados_processados)
            
            logger.info(f"ODS_Completo processado: {len(df_resultado)} justificativas")
            logger.info(f"Justificativas não vazias: {len(df_resultado[df_resultado['Justificativa_ODS'] != ''])}")
            
            return df_resultado
            
        except Exception as e:
            logger.error(f"Erro ao processar ODS_Completo: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def _process_imagens_ods(excel_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Processa dados da aba Imagens_ODS (com suporte a diferentes nomes de aba)"""
        # Tentar diferentes nomes de aba para imagens
        possible_sheet_names = ['Imagens_ODS', 'Imagens_Ods', 'Imagens_ODS ', 'imagens_ods', 'Imagem_ODS', 'Imagens ODS', 'Imagens']
        
        df_raw = pd.DataFrame()
        sheet_name_found = None
        
        # Procurar pela aba correta
        for sheet_name in possible_sheet_names:
            if sheet_name in excel_data:
                df_raw = excel_data[sheet_name]
                sheet_name_found = sheet_name
                break
        
        if df_raw.empty:
            logger.info("Aba de imagens não encontrada")
            return pd.DataFrame()
        
        logger.info(f"Processando aba de imagens: {sheet_name_found} - Shape: {df_raw.shape}")
        
        # CORREÇÃO: Ler especificamente o range A1:C19
        # Limitar aos primeiros 19 linhas e 3 colunas
        if len(df_raw) > 19:
            df_raw = df_raw.iloc[:19]
        if len(df_raw.columns) > 3:
            df_raw = df_raw.iloc[:, :3]
        
        # Limpar dados completamente vazios
        df_raw = df_raw.dropna(how='all')
        
        if df_raw.empty:
            return pd.DataFrame()
        
        # CORREÇÃO: Assumir que a primeira linha é o cabeçalho
        header_row = 0
        
        # Usar a primeira linha como cabeçalho
        if len(df_raw) > 1:
            header_values = df_raw.iloc[0].values
            data_rows = df_raw.iloc[1:].copy()
            
            # Definir nomes de colunas padrão se o cabeçalho não for claro
            column_names = ['ODS_Numero', 'ODS_Nome', 'Imagem_ODS']
            
            # Usar os nomes padrão
            data_rows.columns = column_names[:len(data_rows.columns)]
        else:
            return pd.DataFrame()
        
        if data_rows.empty:
            return pd.DataFrame()
        
        # Limpar dados
        if 'ODS_Numero' in data_rows.columns:
            # Remover linhas onde ODS_Numero é NaN ou vazio
            data_rows = data_rows.dropna(subset=['ODS_Numero'])
            # Converter para numérico
            data_rows['ODS_Numero'] = pd.to_numeric(data_rows['ODS_Numero'], errors='coerce')
            # Remover linhas onde a conversão falhou
            data_rows = data_rows.dropna(subset=['ODS_Numero'])
            # Converter para int
            data_rows['ODS_Numero'] = data_rows['ODS_Numero'].astype(int)
        
        logger.info(f"Imagens_ODS processadas: {len(data_rows)} registros")
        logger.info(f"ODS encontrados: {sorted(data_rows['ODS_Numero'].tolist()) if 'ODS_Numero' in data_rows.columns else 'N/A'}")
        
        return data_rows
    
    @staticmethod
    def _process_tabela_geral(df_raw: pd.DataFrame) -> pd.DataFrame:
        """Processa dados da aba TabelaGeral com PIB per capita real e NOVAS COLUNAS DE CATEGORIA"""
        if df_raw.empty:
            return pd.DataFrame()
        
        # Encontrar cabeçalho
        header_row = None
        for idx, row in df_raw.iterrows():
            row_values = [str(v).strip().lower() for v in row.values if pd.notna(v)]
            if any('municipio' in val or 'pib' in val for val in row_values):
                header_row = idx
                break
        
        if header_row is not None:
            new_header = df_raw.iloc[header_row].values
            df_data = df_raw.iloc[header_row + 1:].copy()
            df_data.columns = new_header
            df_data = df_data.dropna(how='all').reset_index(drop=True)
            
            # Converter colunas numéricas
            numeric_columns = ['Populacao', 'PIB_per_Capita', 'PIB_Total_Milhoes', 'Pontuacao_Geral_ODS']
            
            # NOVO: Colunas de categoria (tratadas como string)
            string_columns = ['Classificacao_Estado', 'Classificacao_Brasil', 'Região_Municipio', 
                            'Grande_Regiao', 'Faixa_Populacional', 'Faixa_de_PIB']
            
            for col in numeric_columns:
                if col in df_data.columns:
                    df_data[col] = pd.to_numeric(df_data[col], errors='coerce')
            
            # Garantir que colunas de texto sejam tratadas como string
            for col in string_columns:
                if col in df_data.columns:
                    df_data[col] = df_data[col].astype(str).str.strip()
            
            return df_data
        
        return df_raw
    
    @staticmethod
    def _process_dados_tabela_din(df_raw: pd.DataFrame) -> pd.DataFrame:
        """Processa dados da aba Dados_Tabela_Din com comparações reais"""
        if df_raw.empty:
            return pd.DataFrame()
        
        # Encontrar cabeçalho
        header_row = None
        for idx, row in df_raw.iterrows():
            row_values = [str(v).strip() for v in row.values if pd.notna(v)]
            if any('ODS_Numero' in val or 'Goiana' in val for val in row_values):
                header_row = idx
                break
        
        if header_row is not None:
            new_header = df_raw.iloc[header_row].values
            df_data = df_raw.iloc[header_row + 1:].copy()
            df_data.columns = new_header
            df_data = df_data.dropna(how='all').reset_index(drop=True)
            
            # Converter colunas numéricas - TAREFA 3B: Removendo Valor_Ideal e Alcançar_Ideal da lista
            numeric_columns = ['ODS_Numero', 'Goiana_IDS', 'Media_3_Cidades_Mesma_Faixa',
                             'Media_Regiao', 'Media_5_Maiores_PIB_PE', 'Gap_Ideal']
            for col in numeric_columns:
                if col in df_data.columns:
                    df_data[col] = pd.to_numeric(df_data[col], errors='coerce')
            
            # Garantir que colunas de texto sejam tratadas como string
            string_columns = ['Valor_Ideal', 'Alcançar_Ideal']
            for col in string_columns:
                if col in df_data.columns:
                    df_data[col] = df_data[col].astype(str).str.strip()
            
            return df_data
        
        return df_raw
    
    @staticmethod
    def _process_ods_municipios(df_raw: pd.DataFrame) -> pd.DataFrame:
        """Processa dados da aba ODS_Municipios com tratamento de colunas variáveis"""
        if df_raw.empty:
            return pd.DataFrame()
        
        logger.info(f"Processando ODS_Municipios - Shape inicial: {df_raw.shape}")
        
        # Limpar dados completamente vazios
        df_raw = df_raw.dropna(how='all')
        
        if df_raw.empty:
            return pd.DataFrame()
        
        # Identificar a linha de cabeçalho
        header_row = None
        for idx, row in df_raw.iterrows():
            # Procurar por indicadores de cabeçalho
            row_values = [str(v).strip().lower() for v in row.values if pd.notna(v)]
            if any(indicator in ' '.join(row_values) for indicator in ['municipio', 'ods', 'indice', 'score', 'índice']):
                header_row = idx
                break
        
        # Se não encontrar cabeçalho, usar a primeira linha com dados
        if header_row is None:
            header_row = 0
        
        # Separar cabeçalho e dados
        header_data = df_raw.iloc[header_row:header_row+1].copy()
        data_rows = df_raw.iloc[header_row+1:].copy() if header_row+1 < len(df_raw) else pd.DataFrame()
        
        if data_rows.empty:
            return pd.DataFrame()
        
        # Processar dados com tratamento flexível de colunas
        processed_rows = []
        
        for idx, row in data_rows.iterrows():
            # Converter row para lista mantendo a ordem
            row_values = list(row.values)
            
            # Criar dicionário com valores disponíveis
            row_dict = {}
            
            # Mapear colunas conhecidas (até onde houver dados)
            column_names = ['Municipio', 'Estado', 'ODS_Numero', 'ODS_Nome', 'IDS_Atual',
                          'Status_Desenvolvimento', 'Populacao', 'Ano_Referencia', 'Icone_ODS', 'Imagem_ODS', 'Região_Municipio']
            
            for i, value in enumerate(row_values):
                if i < len(column_names):
                    row_dict[column_names[i]] = value
                else:
                    # Adicionar colunas extras com nomes genéricos
                    row_dict[f'Extra_Column_{i}'] = value
            
            processed_rows.append(row_dict)
        
        # Criar DataFrame com dados processados
        if processed_rows:
            df_data = pd.DataFrame(processed_rows)
        else:
            df_data = pd.DataFrame()
        
        if df_data.empty:
            return pd.DataFrame()
        
        logger.info(f"DataFrame criado com colunas: {list(df_data.columns)}")
        
        # Limpar dados - remover linhas sem município válido
        if 'Municipio' in df_data.columns:
            # Remover linhas onde Municipio é NaN ou vazio
            df_data = df_data.dropna(subset=['Municipio'])
            df_data = df_data[df_data['Municipio'].astype(str).str.strip() != '']
            df_data = df_data[df_data['Municipio'].astype(str).str.strip() != 'nan']
        
        # Preencher estados vazios
        if 'Estado' in df_data.columns:
            # Preencher baseado no nome do município
            mask_goiana = df_data['Municipio'].str.contains('Goiana', na=False, case=False)
            mask_sp = df_data['Municipio'].str.contains('São Paulo', na=False, case=False)
            mask_rj = df_data['Municipio'].str.contains('Rio de Janeiro', na=False, case=False)
            
            df_data.loc[mask_goiana & (df_data['Estado'].isna() | (df_data['Estado'] == '')), 'Estado'] = 'Pernambuco'
            df_data.loc[mask_sp & (df_data['Estado'].isna() | (df_data['Estado'] == '')), 'Estado'] = 'São Paulo'
            df_data.loc[mask_rj & (df_data['Estado'].isna() | (df_data['Estado'] == '')), 'Estado'] = 'Rio de Janeiro'
        
        # Garantir que Região_Municipio seja tratada como string
        if 'Região_Municipio' in df_data.columns:
            df_data['Região_Municipio'] = df_data['Região_Municipio'].astype(str).str.strip()
        
        # Converter tipos de dados para colunas conhecidas
        numeric_columns = ['IDS_Atual', 'ODS_Numero', 'Populacao', 'Ano_Referencia']
        for col in numeric_columns:
            if col in df_data.columns:
                df_data[col] = pd.to_numeric(df_data[col], errors='coerce')
        
        # Aplicar fórmula de classificação
        if 'IDS_Atual' in df_data.columns:
            def calcular_status(ids_atual):
                if pd.isna(ids_atual):
                    return 'Indefinido'
                elif ids_atual < 0.4:
                    return 'Crítico'
                elif ids_atual < 0.7:
                    return 'Regular'
                else:
                    return 'Bom'
            
            df_data['Status_Desenvolvimento'] = df_data['IDS_Atual'].apply(calcular_status)
        
        return df_data
    
    @staticmethod
    def _process_metodo_well(df_raw: pd.DataFrame) -> pd.DataFrame:
        """Processa dados da aba Método WELL"""
        if df_raw.empty:
            return pd.DataFrame()
        
        # Encontrar cabeçalho
        for idx, row in df_raw.iterrows():
            if any('Pilar_Well' in str(cell) for cell in row.values if pd.notna(cell)):
                new_header = df_raw.iloc[idx].values
                df_data = df_raw.iloc[idx + 1:].copy()
                df_data.columns = new_header
                return df_data.dropna(how='all').reset_index(drop=True)
        
        return df_raw
    
    @staticmethod
    def _process_well_ods_connection(df_raw: pd.DataFrame) -> pd.DataFrame:
        """Processa dados da aba Well_ODS_Connection"""
        if df_raw.empty:
            return pd.DataFrame()
        
        # Encontrar cabeçalho
        for idx, row in df_raw.iterrows():
            if any('ODS_Numero' in str(cell) for cell in row.values if pd.notna(cell)):
                new_header = df_raw.iloc[idx].values
                df_data = df_raw.iloc[idx + 1:].copy()
                df_data.columns = new_header
                return df_data.dropna(how='all').reset_index(drop=True)
        
        return df_raw
    
    @staticmethod
    def get_estados_list(data: Dict[str, Any]) -> List[str]:
        """Obtém lista de estados disponíveis"""
        if 'ods_municipios' not in data or data['ods_municipios'].empty:
            return []
        
        df = data['ods_municipios']
        if 'Estado' not in df.columns:
            return []
        
        estados = df['Estado'].dropna().unique().tolist()
        return sorted([str(e).strip() for e in estados if str(e).strip() and str(e).strip() != 'nan'])
    
    @staticmethod
    def get_municipios_by_estado(data: Dict[str, Any], estado: str) -> List[str]:
        """Obtém lista de municípios filtrada por estado"""
        if 'ods_municipios' not in data or data['ods_municipios'].empty:
            return []
        
        df = data['ods_municipios']
        if 'Estado' not in df.columns or 'Municipio' not in df.columns:
            return []
        
        municipios = df[df['Estado'] == estado]['Municipio'].dropna().unique().tolist()
        return sorted([str(m).strip() for m in municipios if str(m).strip() and str(m).strip() != 'nan'])
    
    @staticmethod
    def get_municipio_info(data: Dict[str, Any], municipio: str) -> Dict[str, Any]:
        """TAREFA 1: Obtém informações detalhadas do município usando dados reais - CORRIGIDO para atualização dinâmica"""
        if 'ods_municipios' not in data or data['ods_municipios'].empty:
            return {}
        
        df = data['ods_municipios']
        municipio_data = df[df['Municipio'] == municipio]
        
        if municipio_data.empty:
            return {}
        
        first_row = municipio_data.iloc[0]
        
        # Buscar PIB real na tabela geral
        pib_per_capita = 0
        if 'tabela_geral' in data and not data['tabela_geral'].empty:
            tabela_geral = data['tabela_geral']
            if 'Municipio' in tabela_geral.columns and 'PIB_per_Capita' in tabela_geral.columns:
                # CORREÇÃO 4: Busca exata em vez de contains
                municipio_match = tabela_geral[tabela_geral['Municipio'] == municipio]
                if not municipio_match.empty:
                    pib_per_capita = municipio_match['PIB_per_Capita'].iloc[0]
                    if pd.notna(pib_per_capita):
                        pib_per_capita = float(pib_per_capita)
        
        # Se não encontrou PIB na tabela geral, usar valor padrão
        if pib_per_capita == 0:
            pib_per_capita = 50000  # Valor padrão mais realista
        
        return {
            'nome': municipio,
            'estado': first_row.get('Estado', 'N/A'),
            'populacao': int(first_row.get('Populacao', 0)) if pd.notna(first_row.get('Populacao')) else 0,
            'ano_referencia': int(first_row.get('Ano_Referencia', 2024)) if pd.notna(first_row.get('Ano_Referencia')) else 2024,
            'total_ods': len(municipio_data),
            'pib_per_capita': pib_per_capita  # CORRIGIDO: Usar dados reais
        }
    
    @staticmethod
    def get_municipio_info_visao_geral(data: Dict[str, Any], municipio: str) -> Dict[str, Any]:
        """TAREFA 1: Obtém informações de classificação do município para a aba Visão Geral"""
        if 'ods_municipios' not in data or data['ods_municipios'].empty:
            return {
                'Classificacao_Estado': "-",
                'Classificacao_Brasil': "-",
                'Região_Municipio': "-"
            }
        
        # Buscar dados da tabela geral
        classificacao_estado = "-"
        classificacao_brasil = "-"
        regiao_municipio = "-"
        
        if 'tabela_geral' in data and not data['tabela_geral'].empty:
            tabela_geral = data['tabela_geral']
            if 'Municipio' in tabela_geral.columns:
                # CORREÇÃO 4: Busca exata em vez de contains
                municipio_match = tabela_geral[tabela_geral['Municipio'] == municipio]
                if not municipio_match.empty:
                    classificacao_estado_raw = municipio_match['Classificacao_Estado'].iloc[0] if 'Classificacao_Estado' in municipio_match.columns else None
                    classificacao_brasil_raw = municipio_match['Classificacao_Brasil'].iloc[0] if 'Classificacao_Brasil' in municipio_match.columns else None
                    regiao_raw = municipio_match['Região_Municipio'].iloc[0] if 'Região_Municipio' in municipio_match.columns else None
                    
                    # Tratar valores vazios
                    if pd.notna(classificacao_estado_raw) and str(classificacao_estado_raw).strip().lower() not in ['nan', 'none', '']:
                        classificacao_estado = str(classificacao_estado_raw).strip()
                    
                    if pd.notna(classificacao_brasil_raw) and str(classificacao_brasil_raw).strip().lower() not in ['nan', 'none', '']:
                        classificacao_brasil = str(classificacao_brasil_raw).strip()
                    
                    if pd.notna(regiao_raw) and str(regiao_raw).strip().lower() not in ['nan', 'none', '']:
                        regiao_municipio = str(regiao_raw).strip()
        
        return {
            'Classificacao_Estado': classificacao_estado,
            'Classificacao_Brasil': classificacao_brasil,
            'Região_Municipio': regiao_municipio
        }
    
    @staticmethod
    def get_comparacao_real(data: Dict[str, Any], ods_numero: int) -> Dict[str, Any]:
        """Obtém dados reais de comparação para um ODS específico - CORRIGIDO para retornar texto"""
        if 'dados_comparacao' not in data or data['dados_comparacao'].empty:
            return {}
        
        df_comp = data['dados_comparacao']
        ods_data = df_comp[df_comp['ODS_Numero'] == ods_numero]
        
        if ods_data.empty:
            return {}
        
        row = ods_data.iloc[0]
        
        return {
            'goiana_ids': row.get('Goiana_IDS', 0),
            'media_similares': row.get('Media_3_Cidades_Mesma_Faixa', 0),
            'media_regional': row.get('Media_Regiao', 0),
            'media_maiores_pib': row.get('Media_5_Maiores_PIB_PE', 0),
            'Valor_Ideal': row.get('Valor_Ideal', "-"),  # Retorna como string
            'gap_ideal': row.get('Gap_Ideal', 0),
            'Alcançar_Ideal': row.get('Alcançar_Ideal', "-")  # Retorna como string
        }
    
    @staticmethod
    def get_comparacao_dinamica(data: Dict[str, Any], municipio_selecionado: str, ods_numero: int) -> Dict[str, Any]:
        """NOVO: Gera comparação dinâmica "ao vivo" usando as novas colunas de categoria"""
        
        # Verificar se temos os dados necessários
        if ('ods_municipios' not in data or data['ods_municipios'].empty or 
            'tabela_geral' not in data or data['tabela_geral'].empty):
            return {}
        
        try:
            # 1. Juntar ODS_Municipios com TabelaGeral
            df_ods = data['ods_municipios'].copy()
            df_tabela = data['tabela_geral'].copy()
            
            # Fazer merge pelos municípios
            df_merged = pd.merge(
                df_ods, 
                df_tabela, 
                on='Municipio', 
                how='inner',
                suffixes=('_ods', '_tabela')
            )
            
            # Filtrar apenas o ODS específico
            df_ods_especifico = df_merged[df_merged['ODS_Numero'] == ods_numero].copy()
            
            if df_ods_especifico.empty:
                return {}
            
            # 2. Obter dados do município selecionado
            municipio_data = df_ods_especifico[df_ods_especifico['Municipio'] == municipio_selecionado]
            
            if municipio_data.empty:
                return {}
            
            municipio_row = municipio_data.iloc[0]
            municipio_score = municipio_row['IDS_Atual']
            
            # Obter categorias do município selecionado
            regiao_municipio = municipio_row.get('Região_Municipio', '')
            grande_regiao = municipio_row.get('Grande_Regiao', '')
            faixa_populacional = municipio_row.get('Faixa_Populacional', '')
            faixa_pib = municipio_row.get('Faixa_de_PIB', '')
            
            # 3. Calcular médias por categoria
            resultados = {
                'municipio_selecionado': {
                    'nome': municipio_selecionado,
                    'score': municipio_score,
                    'municipios': [municipio_selecionado]
                }
            }
            
            # Média da Região_Municipio
            if regiao_municipio and regiao_municipio.strip() and regiao_municipio.lower() != 'nan':
                regiao_data = df_ods_especifico[df_ods_especifico['Região_Municipio'] == regiao_municipio]
                if not regiao_data.empty:
                    regiao_scores = regiao_data['IDS_Atual'].dropna()
                    if not regiao_scores.empty:
                        resultados['media_regiao_municipio'] = {
                            'nome': f'Média {regiao_municipio}',
                            'score': regiao_scores.mean(),
                            'municipios': regiao_data['Municipio'].tolist()
                        }
            
            # Média da Grande_Regiao
            if grande_regiao and grande_regiao.strip() and grande_regiao.lower() != 'nan':
                grande_regiao_data = df_ods_especifico[df_ods_especifico['Grande_Regiao'] == grande_regiao]
                if not grande_regiao_data.empty:
                    grande_regiao_scores = grande_regiao_data['IDS_Atual'].dropna()
                    if not grande_regiao_scores.empty:
                        resultados['media_grande_regiao'] = {
                            'nome': f'Média {grande_regiao}',
                            'score': grande_regiao_scores.mean(),
                            'municipios': grande_regiao_data['Municipio'].tolist()
                        }
            
            # Média da Faixa_Populacional
            if faixa_populacional and faixa_populacional.strip() and faixa_populacional.lower() != 'nan':
                faixa_pop_data = df_ods_especifico[df_ods_especifico['Faixa_Populacional'] == faixa_populacional]
                if not faixa_pop_data.empty:
                    faixa_pop_scores = faixa_pop_data['IDS_Atual'].dropna()
                    if not faixa_pop_scores.empty:
                        resultados['media_faixa_populacional'] = {
                            'nome': f'Média {faixa_populacional}',
                            'score': faixa_pop_scores.mean(),
                            'municipios': faixa_pop_data['Municipio'].tolist()
                        }
            
            # Média da Faixa_de_PIB
            if faixa_pib and faixa_pib.strip() and faixa_pib.lower() != 'nan':
                faixa_pib_data = df_ods_especifico[df_ods_especifico['Faixa_de_PIB'] == faixa_pib]
                if not faixa_pib_data.empty:
                    faixa_pib_scores = faixa_pib_data['IDS_Atual'].dropna()
                    if not faixa_pib_scores.empty:
                        resultados['media_faixa_pib'] = {
                            'nome': f'Média {faixa_pib}',
                            'score': faixa_pib_scores.mean(),
                            'municipios': faixa_pib_data['Municipio'].tolist()
                        }
            
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao calcular comparação dinâmica: {str(e)}")
            return {}
    
    @staticmethod
    def get_justificativa_ods(data: Dict[str, Any], ods_numero: int) -> str:
        """ATUALIZADO: Obtém justificativa do ODS - primeiro da planilha, depois das definições"""
        
        # Tentar primeiro da planilha
        try:
            if 'ods_completo' in data and not data['ods_completo'].empty:
                df_completo = data['ods_completo']
                ods_data = df_completo[df_completo['ODS_Numero'] == ods_numero]
                
                if not ods_data.empty:
                    justificativa = ods_data['Justificativa_ODS'].iloc[0]
                    if pd.notna(justificativa) and str(justificativa).strip():
                        logger.info(f"Justificativa encontrada na planilha para ODS {ods_numero}")
                        return str(justificativa).strip()
        except Exception as e:
            logger.warning(f"Erro ao buscar justificativa na planilha: {str(e)}")
        
        # Se não encontrar na planilha, usar das definições
        ods_info = ODS_DEFINITIONS.get(ods_numero, {})
        justificativa = ods_info.get('justificativa', 'Justificativa não disponível')
        logger.info(f"Usando justificativa das definições para ODS {ods_numero}")
        return justificativa
    
    @staticmethod
    def get_justificativa_ods_direto(excel_file_path: str, ods_numero: int) -> str:
        """Método alternativo: leitura direta da planilha Excel"""
        try:
            # Ler diretamente o range específico da planilha
            df_range = pd.read_excel(
                excel_file_path, 
                sheet_name='ODS_Completo',
                skiprows=5,  # Pular as primeiras 5 linhas (para começar na linha 6)
                nrows=17,    # Ler apenas 17 linhas (linhas 6-22)
                usecols='K'  # Ler apenas a coluna K
            )
            
            if df_range.empty or len(df_range) < ods_numero:
                return "Justificativa não disponível"
            
            # ODS 1 = índice 0, ODS 2 = índice 1, etc.
            justificativa = df_range.iloc[ods_numero - 1, 0]
            
            if pd.notna(justificativa):
                return str(justificativa).strip()
            else:
                return "Justificativa não disponível"
                
        except Exception as e:
            logger.error(f"Erro na leitura direta: {str(e)}")
            return "Justificativa não disponível"
    
    @staticmethod
    def testar_justificativas(data: Dict[str, Any]):
        """Função para testar se as justificativas estão sendo lidas corretamente"""
        logger.info("=== TESTE DE JUSTIFICATIVAS ===")
        
        if 'ods_completo' in data and not data['ods_completo'].empty:
            df = data['ods_completo']
            logger.info(f"DataFrame ODS_Completo shape: {df.shape}")
            logger.info(f"Colunas: {list(df.columns)}")
            logger.info("Primeiras 5 justificativas:")
            
            for i in range(1, 6):
                justificativa = ODSDataManager.get_justificativa_ods(data, i)
                logger.info(f"ODS {i}: {justificativa[:100]}...")
        else:
            logger.info("Dados ODS_Completo não encontrados")
    
    @staticmethod
    def find_image_file(base_path: str, base_filename: str) -> Optional[str]:
        """
        Procura por arquivo de imagem com diferentes extensões
        Suporta: png, jpg, jpeg, jfif, gif
        """
        # Lista de extensões suportadas
        extensions = ['png', 'jpg', 'jpeg', 'jfif', 'gif']
        
        # Converter base_filename para string e limpar espaços
        base_filename = str(base_filename).strip()
        
        # Se for um caminho vazio ou inválido
        if not base_filename or base_filename.lower() in ['nan', 'none', 'null', '']:
            return None
        
        # Remover aspas se existirem
        base_filename = base_filename.strip('\"\'')
        
        # Determinar pasta de imagens
        excel_dir = os.path.dirname(base_path)
        images_folder = os.path.join(excel_dir, 'imagens')
        
        # Se o base_filename já é um caminho absoluto
        if os.path.isabs(base_filename):
            file_path = base_filename
            file_dir = os.path.dirname(base_filename)
            file_name = os.path.basename(base_filename)
        else:
            # Se é relativo, usar a pasta de imagens
            file_path = os.path.join(images_folder, base_filename)
            file_dir = images_folder
            file_name = base_filename
        
        # Remover extensão se existir
        name_without_ext = os.path.splitext(file_name)[0]
        
        # Primeiro tentar o caminho exato (caso já tenha extensão)
        if os.path.exists(file_path):
            return file_path
        
        # Tentar diferentes extensões
        for ext in extensions:
            # Caminho com extensão
            full_path = os.path.join(file_dir, f"{name_without_ext}.{ext}")
            if os.path.exists(full_path):
                return full_path
        
        # Se ainda não encontrou, tentar na pasta de imagens
        if file_dir != images_folder:
            for ext in extensions:
                full_path = os.path.join(images_folder, f"{name_without_ext}.{ext}")
                if os.path.exists(full_path):
                    return full_path
        
        # Se nada funcionar, retornar None
        return None
    
    @staticmethod
    def get_ods_image_info(data: Dict[str, Any], ods_numero: int) -> Dict[str, Any]:
        """Obtém informações da imagem do ODS da aba Imagens_ODS com detecção automática de extensão"""
        # Verificar se a aba de imagens existe
        if 'imagens_ods' not in data or data['imagens_ods'].empty:
            return {
                'ods_numero': ods_numero,
                'ods_nome': ODS_DEFINITIONS.get(ods_numero, {}).get('nome', f'ODS {ods_numero}'),
                'tem_imagem_configurada': False,
                'imagem_info': None,
                'imagem_path_real': None,
                'imagem_encontrada': False,
                'erro': 'Aba "Imagens_ODS" não encontrada'
            }
        
        df_imagens = data['imagens_ods']
        if 'ODS_Numero' not in df_imagens.columns:
            return {
                'ods_numero': ods_numero,
                'ods_nome': ODS_DEFINITIONS.get(ods_numero, {}).get('nome', f'ODS {ods_numero}'),
                'tem_imagem_configurada': False,
                'imagem_info': None,
                'imagem_path_real': None,
                'imagem_encontrada': False,
                'erro': 'Coluna "ODS_Numero" não encontrada na aba de imagens'
            }
        
        imagem_data = df_imagens[df_imagens['ODS_Numero'] == ods_numero]
        
        if imagem_data.empty:
            return {
                'ods_numero': ods_numero,
                'ods_nome': ODS_DEFINITIONS.get(ods_numero, {}).get('nome', f'ODS {ods_numero}'),
                'tem_imagem_configurada': False,
                'imagem_info': None,
                'imagem_path_real': None,
                'imagem_encontrada': False,
                'erro': f'ODS {ods_numero} não encontrado na aba "Imagens_ODS"'
            }
        
        first_row = imagem_data.iloc[0]
        
        # Obter informação da imagem da planilha
        imagem_info = first_row.get('Imagem_ODS', None)
        
        # Se tem informação de imagem, tentar encontrar o arquivo real
        real_image_path = None
        if pd.notna(imagem_info) and imagem_info:
            # Tentar encontrar arquivo com extensão automática
            real_image_path = ODSDataManager.find_image_file(EXCEL_FILE_PATH, str(imagem_info))
        
        return {
            'ods_numero': ods_numero,
            'ods_nome': first_row.get('ODS_Nome', ODS_DEFINITIONS.get(ods_numero, {}).get('nome', f'ODS {ods_numero}')),
            'tem_imagem_configurada': pd.notna(imagem_info) and bool(imagem_info),
            'imagem_info': imagem_info,
            'imagem_path_real': real_image_path,
            'imagem_encontrada': real_image_path is not None
        }

class DashboardComponents:
    """Classe responsável pelos componentes visuais da interface"""
    
    @staticmethod
    def inject_custom_css():
        """Injeta CSS customizado para estilização com paleta de cores personalizada"""
        st.markdown(f"""
        <style>
        /* TAREFA 5: Redesenho do cabeçalho principal com layout centralizado */
        .main-header {{
            background: {PRIMARY_GRADIENT};
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: {TEXT_DARK};
            box-shadow: 0 4px 15px rgba(255, 165, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .logo-container {{
            flex: 0 0 auto;
            margin-right: 2rem;
        }}
        
        .logo-container img {{
            max-height: 160px;
            width: auto;
        }}
        
        .header-text-container {{
            flex: 1;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .main-header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
            color: {TEXT_DARK};
        }}
        
        .main-header p {{
            margin: 0.5rem 0 0 0;
            font-size: 1.2rem;
            opacity: 0.9;
            color: {TEXT_DARK};
        }}
        
        /* CORREÇÃO: KPI Cards padronizados para Visão Geral - TODOS DO MESMO TAMANHO */
        .visao-geral-kpi {{
            background: {BACKGROUND_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            min-height: 150px;
            max-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        
        .visao-geral-kpi:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .visao-geral-kpi .kpi-title {{
            font-size: 1rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .visao-geral-kpi .kpi-value {{
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.3rem;
            color: {PRIMARY_COLOR};
            text-align: center;
        }}
        
        .visao-geral-kpi .kpi-subtitle {{
            font-size: 0.9rem;
            color: #888;
            text-align: center;
        }}
        
        /* CORREÇÃO: Badge de dados reais menor */
        .data-source-badge {{
            background: #16a34a;
            color: white;
            padding: 0.1rem 0.2rem;
            border-radius: 2px;
            font-size: 0.5rem;
            font-weight: bold;
            margin-left: 0.2rem;
            white-space: nowrap;
        }}
        
        .kpi-card {{
            background: {BACKGROUND_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .kpi-title {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .kpi-value {{
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.25rem;
            color: {PRIMARY_COLOR};
        }}
        
        .kpi-subtitle {{
            font-size: 1rem;
            color: #888;
        }}
        
        /* TAREFA 2: KPI Card especial para Projeto Bússola com melhorias visuais */
        .bussola-well-card {{
            background: {BACKGROUND_COLOR};
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            text-align: center;
        }}
        
        .bussola-well-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .bussola-well-title {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: {PRIMARY_COLOR};
            text-align: center;
        }}
        
        .bussola-well-subtitle {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            margin: 0;
        }}
        
        /* CORREÇÃO: KPI Cards simétricos para Vantagens Estratégicas */
        .vantagem-card {{
            background: {BACKGROUND_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            min-height: 200px;
            max-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .vantagem-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .vantagem-card .kpi-title {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .vantagem-card .kpi-value {{
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: {PRIMARY_COLOR};
        }}
        
        .vantagem-card .kpi-subtitle {{
            font-size: 0.95rem;
            color: #888;
            line-height: 1.4;
        }}
        
        .municipio-card {{
            background: {BACKGROUND_COLOR};
            color: {PRIMARY_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0, 95, 107, 0.3);
            border: 2px solid {PRIMARY_COLOR};
        }}
        
        .municipio-card h4 {{
            margin: 0 0 1rem 0;
            font-size: 1.2rem;
            color: {PRIMARY_COLOR};
        }}
        
        .municipio-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            font-size: 0.9rem;
        }}
        
        .municipio-info-item {{
            background: rgba(0, 95, 107, 0.1);
            padding: 0.5rem;
            border-radius: 5px;
            text-align: center;
            color: {PRIMARY_COLOR};
        }}
        
        .municipio-info-item strong {{
            color: {PRIMARY_COLOR};
        }}
        
        .image-container {{
            background: {BACKGROUND_LIGHT};
            border: 2px dashed #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .image-available {{
            background: #f0fdf4;
            border-color: #16a34a;
            color: #15803d;
        }}
        
        .image-missing {{
            background: #fffbeb;
            border-color: #d97706;
            color: #b45309;
        }}
        
        .image-not-found {{
            background: #fef2f2;
            border-color: #dc2626;
            color: #991b1b;
        }}
        
        /* CORREÇÃO: Cards ODS padronizados e alinhados */
        .ods-card {{
            background: {BACKGROUND_COLOR};
            border: 2px solid {PRIMARY_COLOR};
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        }}
        
        .ods-card:hover {{
            background: {PRIMARY_COLOR};
            color: {TEXT_LIGHT};
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 95, 107, 0.3);
        }}
        
        .ods-card img {{
            max-width: 100px;
            max-height: 100px;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            margin-top: 40px;
        }}
        
        /* CORREÇÃO: Botão único com gradiente amarelo/laranja - CLICÁVEL */
        .ods-card-button {{
            font-weight: bold;
            font-size: 0.9rem;
            color: {TEXT_DARK};
            background: {PRIMARY_GRADIENT};
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            border: none;
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 85%;
            z-index: 10;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .ods-card-button:hover {{
            transform: translateX(-50%) translateY(-2px);
            box-shadow: 0 2px 8px rgba(255, 165, 0, 0.4);
        }}
        
        .trend-positive {{ color: {STATUS_GREEN}; font-weight: bold; }}
        .trend-moderate {{ color: {STATUS_ORANGE}; font-weight: bold; }}
        .trend-stable {{ color: #6b7280; font-weight: bold; }}
        .trend-negative {{ color: {STATUS_RED}; font-weight: bold; }}
        
        /* CORREÇÃO: Painéis KPI padronizados - 2 em cima, 1 embaixo */
        .ods-detail-panel {{
            background: {BACKGROUND_COLOR};
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            min-height: 200px;
            max-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .ods-detail-panel:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .ods-detail-panel .kpi-title {{
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 0.8rem;
            font-weight: 600;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        
        .ods-detail-panel .kpi-value {{
            font-size: 2.8rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: {PRIMARY_COLOR};
            word-wrap: break-word;
        }}
        
        .ods-detail-panel .kpi-subtitle {{
            font-size: 1.1rem;
            color: #888;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }}
        
        /* TAREFA 3B: Novos KPI Cards pequenos para Valor Ideal e Alcançar Ideal - CORREÇÃO APLICADA */
        .ods-small-kpi {{
            background: {BACKGROUND_COLOR};
            padding: 0.7rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 3px solid {PRIMARY_COLOR};
            margin-bottom: 0.5rem;
            transition: transform 0.2s ease;
            min-height: 65px;
            max-height: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .ods-small-kpi:hover {{
            transform: translateY(-1px);
            box-shadow: 0 3px 12px rgba(0,0,0,0.15);
        }}
        
        .ods-small-kpi .kpi-title {{
            font-size: 0.75rem;
            color: #666;
            margin-bottom: 0.2rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .ods-small-kpi .kpi-value {{
            font-size: 1.1rem;
            font-weight: bold;
            color: {PRIMARY_COLOR};
            white-space: normal;
            line-height: 1.1;
        }}
        
        .ods-small-kpi .data-source-badge {{
            font-size: 0.4rem;
            padding: 0.05rem 0.1rem;
            margin-left: 0.1rem;
        }}
        
        /* CORREÇÃO: Painel da Meta - Altura menor e mais largo conforme especificação */
        .ods-meta-panel {{
            background: {BACKGROUND_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            min-height: 100px;
            max-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .ods-meta-panel:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .ods-meta-panel .kpi-title {{
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 0.8rem;
            font-weight: 600;
        }}
        
        .ods-meta-panel .kpi-subtitle {{
            font-size: 1rem;
            color: #888;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            line-height: 1.3;
            text-align: center;
            font-weight: bold;
        }}
        
        /* TAREFA 2: Painel da Justificativa - AJUSTES FINAIS */
        .ods-justificativa-panel {{
            background: {BACKGROUND_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
            min-height: 165px; /* Aumento de 10% conforme solicitado */
            max-height: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .ods-justificativa-panel:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .ods-justificativa-panel .kpi-title {{
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 0.8rem;
            font-weight: 600;
        }}
        
        .ods-justificativa-panel .kpi-subtitle {{
            font-size: 0.9rem; /* Redução de 1rem para 0.9rem conforme solicitado */
            color: #888;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            line-height: 1.4;
            text-align: center;
            font-weight: bold;
            white-space: normal;
            overflow: visible;
            max-height: none;
        }}
        
        /* TAREFA 1: Novo card para informações de classificação na Visão Geral */
        .visao-geral-info-card {{
            background: {BACKGROUND_COLOR};
            color: {PRIMARY_COLOR};
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0, 95, 107, 0.3);
            border: 2px solid {PRIMARY_COLOR};
        }}
        
        .visao-geral-info-card h4 {{
            margin: 0 0 1rem 0;
            font-size: 1.2rem;
            color: {PRIMARY_COLOR};
        }}
        
        .visao-geral-info {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr; /* Layout de 3 colunas */
            gap: 0.5rem;
            font-size: 0.9rem;
        }}
        
        .visao-geral-info-item {{
            background: rgba(0, 95, 107, 0.1);
            padding: 0.5rem;
            border-radius: 5px;
            text-align: center;
            color: {PRIMARY_COLOR};
        }}
        
        .visao-geral-info-item strong {{
            color: {PRIMARY_COLOR};
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """TAREFA 5: Renderiza o cabeçalho principal com logo à esquerda e texto centralizado"""
        # Tentar carregar logo da empresa
        logo_path = os.path.join(os.path.dirname(EXCEL_FILE_PATH), 'logo.png')
        logo_html = ""
        
        if os.path.exists(logo_path):
            try:
                logo_base64 = get_base64_of_bin_file(logo_path)
                logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo da Empresa">'
            except:
                logo_html = "🏢"
        else:
            logo_html = "🏢"
        
        st.markdown(f"""
        <div class="main-header">
            <div class="logo-container">
                {logo_html}
            </div>
            <div class="header-text-container">
                <h1>Projeto Bússola WELL</h1>
                <p><strong>📊 Monitoramento dos Objetivos de Desenvolvimento Sustentável</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_visao_geral_kpi_card(title: str, value: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """Renderiza um cartão KPI especial para a aba Visão Geral - TODOS DO MESMO TAMANHO"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="visao-geral-kpi">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_kpi_card(title: str, value: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """Renderiza um cartão KPI"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_bussola_well_card():
        """TAREFA 2: Renderiza o cartão especial do Projeto Bússola com melhorias visuais"""
        return f"""
        <div class="bussola-well-card">
            <div class="bussola-well-title">Projeto Bússola</div>
            <div class="bussola-well-subtitle">Toda gestão precisa de um norte. Viemos apresentar a bússola.</div>
        </div>
        """
    
    @staticmethod
    def render_vantagem_card(title: str, value: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """Renderiza um cartão KPI simétrico para vantagens estratégicas"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="vantagem-card">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_ods_detail_kpi_card(title: str, value: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """Renderiza um cartão KPI especial para a aba ODS detalhado com tamanhos padronizados"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="ods-detail-panel">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_ods_small_kpi_card(title: str, value: str, color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """TAREFA 3B: Renderiza um cartão KPI pequeno para Valor Ideal e Alcançar Ideal - CORREÇÃO APLICADA"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="ods-small-kpi">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
        </div>
        """
    
    @staticmethod
    def render_ods_meta_kpi_card(title: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """Renderiza um cartão KPI especial para a meta - Altura menor conforme especificação"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="ods-meta-panel">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_ods_justificativa_kpi_card(title: str, subtitle: str = "", color: str = PRIMARY_COLOR, show_real_data_badge: bool = False):
        """TAREFA 2: Renderiza um cartão KPI especial para a justificativa - AJUSTES FINAIS"""
        badge_html = f'<span class="data-source-badge">DADOS REAIS</span>' if show_real_data_badge else ''
        
        return f"""
        <div class="ods-justificativa-panel">
            <div class="kpi-title">{title}{badge_html}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_municipio_card(municipio_info: Dict[str, Any]):
        """TAREFA 1: Renderiza card com informações do município usando dados reais - CORRIGIDO para atualização dinâmica"""
        populacao_formatted = format_number(municipio_info['populacao'], 0)
        pib_formatted = format_currency(municipio_info['pib_per_capita'])
        
        st.markdown(f"""
        <div class="municipio-card">
            <h4>📍 {municipio_info['nome']} <span class="data-source-badge">DADOS REAIS</span></h4>
            <div class="municipio-info">
                <div class="municipio-info-item">
                    <strong>Estado</strong><br>
                    {municipio_info['estado']}
                </div>
                <div class="municipio-info-item">
                    <strong>População</strong><br>
                    {populacao_formatted}
                </div>
                <div class="municipio-info-item">
                    <strong>PIB per capita</strong><br>
                    {pib_formatted}
                </div>
                <div class="municipio-info-item">
                    <strong>Total ODS</strong><br>
                    {municipio_info['total_ods']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_visao_geral_info_card(municipio_info: Dict[str, Any]):
        """TAREFA 1: Renderiza card com informações de classificação para a aba Visão Geral"""
        st.markdown(f"""
        <div class="visao-geral-info-card">
            <h4>📋 Classificação do Município <span class="data-source-badge">DADOS REAIS</span></h4>
            <div class="visao-geral-info">
                <div class="visao-geral-info-item">
                    <strong>Classificação Estadual</strong><br>
                    {municipio_info['Classificacao_Estado']}
                </div>
                <div class="visao-geral-info-item">
                    <strong>Classificação Brasil</strong><br>
                    {municipio_info['Classificacao_Brasil']}
                </div>
                <div class="visao-geral-info-item">
                    <strong>Região</strong><br>
                    {municipio_info['Região_Municipio']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# CORREÇÃO 1: Função render_sidebar modificada para usar session_state corretamente
def render_sidebar(data: Dict[str, Any]) -> Tuple[str, str]:
    """Renderiza a barra lateral com controles simplificada"""
    st.sidebar.header("🎛️ Controles do Dashboard")
    
    # Botão de atualização
    if st.sidebar.button("🔄 Atualizar Dados", type="primary"):
        st.session_state.dashboard_data = None
        st.rerun()
    
    # Seleção de Estado
    estados = ODSDataManager.get_estados_list(data)
    if not estados:
        st.sidebar.error("❌ Nenhum estado encontrado")
        return "", ""
    
    # CORREÇÃO 1: Usar session_state para manter seleção
    selected_estado = st.sidebar.selectbox(
        "🗺️ Selecione o Estado:",
        estados,
        index=estados.index(st.session_state.get('selected_estado', estados[0])) if st.session_state.get('selected_estado') in estados else 0,
        key="selected_estado_selectbox"
    )
    
    # Seleção de Município (filtrado por estado)
    municipios = ODSDataManager.get_municipios_by_estado(data, selected_estado)
    if not municipios:
        st.sidebar.error(f"❌ Nenhum município encontrado para {selected_estado}")
        return selected_estado, ""
    
    # CORREÇÃO 1: Usar session_state para manter seleção
    # Verificar se o município selecionado ainda é válido para o estado
    previous_municipio = st.session_state.get('selected_municipio', municipios[0])
    default_index = municipios.index(previous_municipio) if previous_municipio in municipios else 0
    
    selected_municipio = st.sidebar.selectbox(
        "🏙️ Selecione o Município:",
        municipios,
        index=default_index,
        key="selected_municipio_selectbox"
    )
    
    # TAREFA 1: Informações do Município - CORRIGIDO para atualização dinâmica
    if selected_municipio:
        municipio_info = ODSDataManager.get_municipio_info(data, selected_municipio)
        if municipio_info:
            st.sidebar.markdown("### 📊 Informações do Município")
            DashboardComponents.render_municipio_card(municipio_info)
    
    return selected_estado, selected_municipio

def render_ids_ods_tab():
    """Renderiza a aba IDS e ODS"""
    st.header("🧭 IDS e ODS")
    
    # TAREFA 2: KPI Card especial - Projeto Bússola com melhorias visuais
    st.markdown(DashboardComponents.render_bussola_well_card(), unsafe_allow_html=True)
    
    # KPI Card - Agenda Global ONU 2030
    st.markdown(DashboardComponents.render_kpi_card(
        "🌐 Agenda Global ONU - 2030",
        "",
        "A Metodologia WELL se baseia em uma Agenda Global, estabelecida pela ONU e da qual o Brasil é membro. Ao aderir à Agenda, o município sinaliza para o mercado e para a sociedade que está aberto a todo tipo de parceria (com empresas, ONGs, universidades), que facilita a viabilização de todos os objetivos e captação de recursos. O Compromisso Global funciona com duas frentes complementares ODS e IDS, e que em essência um mostra a Direção e o outro, o Resultado.",
        PRIMARY_COLOR
    ), unsafe_allow_html=True)
    
    # CORREÇÕES APLICADAS: Grade 2x2 de KPI Cards - Linha 1
    col1, col2 = st.columns(2)
    
    # CORREÇÃO 1: Card IDS - Mudança do valor principal
    with col1:
        st.markdown(DashboardComponents.render_kpi_card(
            "📊 IDS (Indicadores de Desenvolvimento Sustentável)",
            "Painel de Controle",  # CORREÇÃO 1: DE "Painel de guerrilha" PARA "Painel de Controle"
            "Função: Painel de Controle<br>Objetivo: Medir e comprovar avanços<br>Pergunta-chave: \"Onde estamos ?\"",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
    
    # CORREÇÃO 2: Card ODS - Subtítulo completo e correto
    with col2:
        st.markdown(DashboardComponents.render_kpi_card(
            "🎯 ODS (Objetivos de Desenvolvimento Sustentável)",
            "Plano Estratégico",
            "Função: Plano Estratégico Municipal<br>Objetivo: Definir visão de futuro<br>Pergunta-chave: \"Aonde queremos chegar?\"",  # CORREÇÃO 2: Subtítulo completo
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
    
    # Grade 2x2 de KPI Cards - Linha 2
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(DashboardComponents.render_kpi_card(
            "📈 M-DLIS (Monitoramento de Desenvolvimento Local Integrado e Sustentável)",
            "Sistema de Avaliação",
            "Função: Avaliação contínua<br>Objetivo: Monitorar indicadores-chave<br>Pergunta-chave: \"Como provamos nosso progresso?\"",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
    
    # CORREÇÃO 3: Card SDS - Mudança do valor principal
    with col4:
        st.markdown(DashboardComponents.render_kpi_card(
            "🌱 SDS (Soluções de Desenvolvimento Sustentável)",
            "Ferramentas Práticas",  # CORREÇÃO 3: DE "Ferramentas" PARA "Ferramentas Práticas"
            "Função: Implementação de soluções<br>Objetivo: Converter teoria em prática<br>Pergunta-chave: \"Como fazer acontecer?\"",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)

def render_vantagens_estrategicas_tab():
    """Renderiza a aba Vantagens Estratégicas com KPIs simétricos"""
    st.header("💡 Vantagens Estratégicas")
    
    # 4 KPI Cards simétricos - 2x2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(DashboardComponents.render_vantagem_card(
            "🎯 Governança de Alta Performance",
            "Gestão Baseada em Dados",
            "Menos 'achismo', mais gestão: transforme sua prefeitura em uma máquina de resultados com um plano claro e dados que comprovam o progresso.",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
        
        st.markdown(DashboardComponents.render_vantagem_card(
            "🗳️ Fortalecimento do Capital Político",
            "Marca Positiva da Cidade",
            "Comunique realizações de forma clara e construa uma marca positiva para a cidade, aumentando a confiança do cidadão e o seu capital político.",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(DashboardComponents.render_vantagem_card(
            "💰 Acesso a Capital e Novos Investimentos",
            "Atração de Investidores",
            "Coloque seu município no radar dos grandes investidores: quem se alinha aos ODS atrai mais recursos, empresas e empregos.",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
        
        st.markdown(DashboardComponents.render_vantagem_card(
            "🏗️ Construção de uma Cidade Resiliente",
            "Legado de Qualidade",
            "Governe hoje pensando no amanhã: prepare sua cidade para os desafios do futuro e deixe um legado de qualidade de vida e segurança.",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)

def render_visao_geral_tab(data: Dict[str, Any], selected_municipio: str):
    """TAREFA 1: Renderiza a aba de Visão Geral com KPIs padronizados - CORRIGIDO para atualização dinâmica"""
    st.header(f"📊 Visão Geral - {selected_municipio}")
    
    if 'ods_municipios' not in data or data['ods_municipios'].empty:
        st.error("❌ Dados não disponíveis")
        return
    
    # Filtrar dados do município
    municipio_data = data['ods_municipios'][data['ods_municipios']['Municipio'] == selected_municipio].copy()
    
    if municipio_data.empty:
        st.error(f"❌ Dados não encontrados para o município: {selected_municipio}")
        return
    
    # TAREFA 1: Card de informações de classificação na aba Visão Geral
    municipio_info_classificacao = ODSDataManager.get_municipio_info_visao_geral(data, selected_municipio)
    if municipio_info_classificacao:
        DashboardComponents.render_visao_geral_info_card(municipio_info_classificacao)
    
    # CORREÇÃO: KPIs principais - TODOS DO MESMO TAMANHO E ALINHADOS
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ods = len(municipio_data)
        st.markdown(DashboardComponents.render_visao_geral_kpi_card(
            "📈 Total de ODS",
            str(total_ods),
            "Objetivos monitorados",
            PRIMARY_COLOR
        ), unsafe_allow_html=True)
    
    with col2:
        if 'IDS_Atual' in municipio_data.columns:
            valid_scores = municipio_data['IDS_Atual'].dropna()
            if not valid_scores.empty:
                media_desempenho = valid_scores.mean()
                if media_desempenho <= 1:
                    media_desempenho = media_desempenho * 100
                
                st.markdown(DashboardComponents.render_visao_geral_kpi_card(
                    "📊 Média Geral",
                    format_percentage(media_desempenho/100),
                    "Desempenho médio",
                    PRIMARY_COLOR,
                    show_real_data_badge=True
                ), unsafe_allow_html=True)
            else:
                st.markdown(DashboardComponents.render_visao_geral_kpi_card(
                    "📊 Média Geral",
                    "N/A",
                    "Sem dados válidos",
                    PRIMARY_COLOR
                ), unsafe_allow_html=True)
    
    with col3:
        if 'Status_Desenvolvimento' in municipio_data.columns:
            ods_criticos = len(municipio_data[municipio_data['Status_Desenvolvimento'] == 'Crítico'])
            st.markdown(DashboardComponents.render_visao_geral_kpi_card(
                "⚠️ ODS Críticos",
                str(ods_criticos),
                "Necessitam atenção",
                STATUS_RED
            ), unsafe_allow_html=True)
    
    with col4:
        # Buscar população real da tabela geral
        populacao = 0
        if 'tabela_geral' in data and not data['tabela_geral'].empty:
            tabela_geral = data['tabela_geral']
            if 'Municipio' in tabela_geral.columns and 'Populacao' in tabela_geral.columns:
                # CORREÇÃO 4: Busca exata em vez de contains
                municipio_match = tabela_geral[tabela_geral['Municipio'] == selected_municipio]
                if not municipio_match.empty:
                    populacao = municipio_match['Populacao'].iloc[0]
        
        if populacao == 0 and 'Populacao' in municipio_data.columns and not municipio_data['Populacao'].isna().all():
            populacao = municipio_data['Populacao'].iloc[0]
        
        if populacao > 0:
            st.markdown(DashboardComponents.render_visao_geral_kpi_card(
                "👥 População",
                format_number(populacao, 0),
                "Habitantes",
                PRIMARY_COLOR,
                show_real_data_badge=True
            ), unsafe_allow_html=True)
    
    # Gráfico de desempenho com número do ODS
    st.subheader("📊 Desempenho por ODS")
    
    if 'ODS_Nome' in municipio_data.columns and 'IDS_Atual' in municipio_data.columns and 'ODS_Numero' in municipio_data.columns:
        # Filtrar apenas dados válidos
        chart_data = municipio_data[['ODS_Numero', 'ODS_Nome', 'IDS_Atual', 'Status_Desenvolvimento']].copy()
        chart_data = chart_data.dropna(subset=['IDS_Atual'])
        
        if not chart_data.empty:
            if chart_data['IDS_Atual'].max() <= 1:
                chart_data['IDS_Atual_Pct'] = chart_data['IDS_Atual'] * 100
            else:
                chart_data['IDS_Atual_Pct'] = chart_data['IDS_Atual']
            
            # Criar label com número e nome do ODS
            chart_data['ODS_Label'] = chart_data.apply(lambda x: f"ODS {int(x['ODS_Numero'])}: {x['ODS_Nome']}", axis=1)
            
            chart_data = chart_data.sort_values('IDS_Atual_Pct', ascending=True)
            
            colors = []
            for status in chart_data['Status_Desenvolvimento']:
                if status == 'Crítico':
                    colors.append(STATUS_RED)
                elif status == 'Regular':
                    colors.append(STATUS_ORANGE)
                elif status == 'Bom':
                    colors.append(STATUS_GREEN)
                else:
                    colors.append('#6b7280')
            
            fig = go.Figure(data=[
                go.Bar(
                    y=chart_data['ODS_Label'],
                    x=chart_data['IDS_Atual_Pct'],
                    orientation='h',
                    marker_color=colors,
                    text=[format_percentage(v/100) for v in chart_data['IDS_Atual_Pct']],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="📊 Desempenho por ODS (Dados Reais da Planilha)",
                xaxis_title="Score (%)",
                yaxis_title="Objetivos de Desenvolvimento Sustentável",
                height=600,
                paper_bgcolor=BACKGROUND_COLOR,
                plot_bgcolor=BACKGROUND_COLOR
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum dado válido encontrado para gerar o gráfico")

def render_ods_detalhado_tab(data: Dict[str, Any], selected_municipio: str):
    """NOVO: Renderiza a aba de ODS Detalhado com gráfico dinâmico automático"""
    st.header("📊 ODS Detalhado")
    
    # Grade de 17 botões ODS COM IMAGENS MAIORES - ALINHAMENTO CORRIGIDO
    st.subheader("🎯 Selecione um ODS para Análise Detalhada")
    
    # Obter dados do município
    municipio_data = data['ods_municipios'][data['ods_municipios']['Municipio'] == selected_municipio].copy()
    
    # CORREÇÃO: Layout em 6 colunas com alinhamento perfeito
    # Primeira linha: ODS 1-6
    cols1 = st.columns(6)
    for i in range(6):
        ods_num = i + 1
        with cols1[i]:
            # Obter informações da imagem
            image_info = ODSDataManager.get_ods_image_info(data, ods_num)
            
            # Criar HTML do card com imagem
            image_html = ""
            if image_info.get('imagem_encontrada'):
                imagem_path = image_info.get('imagem_path_real')
                if imagem_path and os.path.exists(imagem_path):
                    try:
                        image_base64 = get_base64_of_bin_file(imagem_path)
                        image_html = f'<img src="data:image/png;base64,{image_base64}" alt="ODS {ods_num}">'
                    except:
                        image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
                else:
                    image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            else:
                image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            
            # Renderizar card customizado
            st.markdown(f"""
            <div class="ods-card">
                {image_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Botão único com gradiente - CLICÁVEL
            if st.button(f"ODS {ods_num}", key=f"ods_btn_{ods_num}", 
                        help=f"Selecionar ODS {ods_num}", 
                        use_container_width=True):
                st.session_state.selected_ods = ods_num
    
    # Segunda linha: ODS 7-12
    cols2 = st.columns(6)
    for i in range(6):
        ods_num = i + 7
        with cols2[i]:
            # Obter informações da imagem
            image_info = ODSDataManager.get_ods_image_info(data, ods_num)
            
            # Criar HTML do card com imagem
            image_html = ""
            if image_info.get('imagem_encontrada'):
                imagem_path = image_info.get('imagem_path_real')
                if imagem_path and os.path.exists(imagem_path):
                    try:
                        image_base64 = get_base64_of_bin_file(imagem_path)
                        image_html = f'<img src="data:image/png;base64,{image_base64}" alt="ODS {ods_num}">'
                    except:
                        image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
                else:
                    image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            else:
                image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            
            # Renderizar card customizado
            st.markdown(f"""
            <div class="ods-card">
                {image_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Botão único com gradiente - CLICÁVEL
            if st.button(f"ODS {ods_num}", key=f"ods_btn_{ods_num}", 
                        help=f"Selecionar ODS {ods_num}", 
                        use_container_width=True):
                st.session_state.selected_ods = ods_num
    
    # CORREÇÃO: Terceira linha: ODS 13-17 - ALINHAMENTO PERFEITO
    # Usar espaçamento para centralizar os 5 botões
    col_empty1, col13, col14, col15, col16, col17, col_empty2 = st.columns([0.5, 1, 1, 1, 1, 1, 0.5])
    
    for i, col in enumerate([col13, col14, col15, col16, col17]):
        ods_num = i + 13
        with col:
            # Obter informações da imagem
            image_info = ODSDataManager.get_ods_image_info(data, ods_num)
            
            # Criar HTML do card com imagem
            image_html = ""
            if image_info.get('imagem_encontrada'):
                imagem_path = image_info.get('imagem_path_real')
                if imagem_path and os.path.exists(imagem_path):
                    try:
                        image_base64 = get_base64_of_bin_file(imagem_path)
                        image_html = f'<img src="data:image/png;base64,{image_base64}" alt="ODS {ods_num}">'
                    except:
                        image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
                else:
                    image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            else:
                image_html = f'<div style="width: 100px; height: 100px; background: {PRIMARY_COLOR}; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {TEXT_LIGHT}; font-weight: bold; margin-top: 40px;">ODS<br>{ods_num}</div>'
            
            # Renderizar card customizado
            st.markdown(f"""
            <div class="ods-card">
                {image_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Botão único com gradiente - CLICÁVEL
            if st.button(f"ODS {ods_num}", key=f"ods_btn_{ods_num}", 
                        help=f"Selecionar ODS {ods_num}", 
                        use_container_width=True):
                st.session_state.selected_ods = ods_num
    
    # CORREÇÃO: Espaço maior na análise detalhada
    if 'selected_ods' in st.session_state and st.session_state.selected_ods:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço maior
        
        selected_ods = st.session_state.selected_ods
        ods_info = ODS_DEFINITIONS.get(selected_ods, {})
        ods_data = municipio_data[municipio_data['ODS_Numero'] == selected_ods]
        
        if not ods_data.empty and pd.notna(ods_data['IDS_Atual'].iloc[0]):
            st.markdown("---")
            st.subheader(f"📈 Análise Detalhada - ODS {selected_ods}: {ods_info.get('nome', 'N/A')}")
            
            # Layout com imagem e KPIs lado a lado
            col_img, col_kpis = st.columns([1, 2])
            
            with col_img:
                # TAREFA 3A: Seção de imagem do ODS (simplificada - removidos textos estáticos)
                image_info = ODSDataManager.get_ods_image_info(data, selected_ods)
                
                if image_info.get('imagem_encontrada'):
                    imagem_path = image_info.get('imagem_path_real')
                    if imagem_path and os.path.exists(imagem_path):
                        st.image(imagem_path, width=200)
                    else:
                        st.info("Imagem não disponível")
                
                # TAREFA 3B: Novos KPI Cards pequenos abaixo da imagem - CORRIGIDO para exibir texto
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Buscar dados reais de comparação para os novos KPIs
                comparacao_real = ODSDataManager.get_comparacao_real(data, selected_ods)
                
                if comparacao_real:
                    # KPI Card 1: Valor Ideal (TEXTO)
                    valor_ideal_texto = str(comparacao_real.get('Valor_Ideal', '-')).strip()
                    valor_ideal_texto = valor_ideal_texto if valor_ideal_texto and valor_ideal_texto.lower() != 'nan' else '-'
                    st.markdown(DashboardComponents.render_ods_small_kpi_card(
                        "Valor Ideal",
                        valor_ideal_texto,  # Passa o TEXTO diretamente
                        PRIMARY_COLOR,
                        show_real_data_badge=True
                    ), unsafe_allow_html=True)
                    
                    # KPI Card 2: Alcançar o Ideal (TEXTO)
                    alcancar_ideal_texto = str(comparacao_real.get('Alcançar_Ideal', '-')).strip()
                    alcancar_ideal_texto = alcancar_ideal_texto if alcancar_ideal_texto and alcancar_ideal_texto.lower() != 'nan' else '-'
                    st.markdown(DashboardComponents.render_ods_small_kpi_card(
                        "Alcançar Ideal",
                        alcancar_ideal_texto,  # Passa o TEXTO diretamente
                        PRIMARY_COLOR,
                        show_real_data_badge=True
                    ), unsafe_allow_html=True)
            
            with col_kpis:
                # TAREFA 3C: KPIs do ODS selecionado - 2 em cima (MANTIDOS INALTERADOS)
                score = ods_data['IDS_Atual'].iloc[0]
                if score <= 1:
                    score_pct = score * 100
                
                status = ods_data['Status_Desenvolvimento'].iloc[0]
                
                # Primeira linha: 2 painéis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(DashboardComponents.render_ods_detail_kpi_card(
                        "📊 Pontuação",
                        format_percentage(score),
                        "Score atual",
                        ods_info.get('cor', PRIMARY_COLOR),
                        show_real_data_badge=True
                    ), unsafe_allow_html=True)
                
                with col2:
                    status_colors = {"Crítico": STATUS_RED, "Regular": STATUS_ORANGE, "Bom": STATUS_GREEN}
                    st.markdown(DashboardComponents.render_ods_detail_kpi_card(
                        "🏆 Classificação",
                        status,
                        "Status atual",
                        status_colors.get(status, '#6b7280')
                    ), unsafe_allow_html=True)
                
                # CORREÇÃO: Meta ONU 2030 embaixo (ocupando toda a largura)
                st.markdown(DashboardComponents.render_ods_meta_kpi_card(
                    "🎯 Meta ONU 2030",
                    ods_info.get('meta', 'Meta oficial da ONU'),
                    ods_info.get('cor', PRIMARY_COLOR)
                ), unsafe_allow_html=True)
                
                # ATUALIZADO: Justificativa ODS com texto completo em negrito sem cortar
                justificativa = ODSDataManager.get_justificativa_ods(data, selected_ods)
                
                # Verificar se veio da planilha ou das definições
                is_from_spreadsheet = False
                try:
                    if 'ods_completo' in data and not data['ods_completo'].empty:
                        df_completo = data['ods_completo']
                        ods_data_check = df_completo[df_completo['ODS_Numero'] == selected_ods]
                        if not ods_data_check.empty:
                            justificativa_planilha = ods_data_check['Justificativa_ODS'].iloc[0]
                            if pd.notna(justificativa_planilha) and str(justificativa_planilha).strip():
                                is_from_spreadsheet = True
                except:
                    pass
                
                st.markdown(DashboardComponents.render_ods_justificativa_kpi_card(
                    "📋 Justificativa ODS",
                    justificativa,
                    ods_info.get('cor', PRIMARY_COLOR),
                    show_real_data_badge=is_from_spreadsheet
                ), unsafe_allow_html=True)
            
            # CORREÇÃO: Espaço maior antes da comparação e Método WELL
            st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço maior
            
            # NOVO: Gráfico comparativo DINÂMICO COM DADOS "AO VIVO"
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📊 Comparação Dinâmica com Médias Automáticas")
                
                # Buscar dados dinâmicos de comparação
                comparacao_dinamica = ODSDataManager.get_comparacao_dinamica(data, selected_municipio, selected_ods)
                
                if comparacao_dinamica:
                    # Preparar dados para o gráfico
                    categorias = []
                    scores = []
                    municipios_por_categoria = {}
                    
                    for key, info in comparacao_dinamica.items():
                        categorias.append(info['nome'])
                        score = info['score']
                        # Converter para percentual se necessário
                        if score <= 1:
                            score = score * 100
                        scores.append(score)
                        municipios_por_categoria[info['nome']] = info['municipios']
                    
                    # Criar gráfico de barras
                    fig = px.bar(
                        x=scores,
                        y=categorias,
                        orientation='h',
                        title=f"Comparação Dinâmica - ODS {selected_ods} (Calculado ao Vivo)",
                        color=scores,
                        color_continuous_scale='Viridis',
                        text=[format_percentage(v/100) for v in scores]
                    )
                    
                    fig.update_traces(textposition='auto')
                    fig.update_layout(
                        height=300,
                        xaxis_title="Score (%)",
                        yaxis_title="Categorias de Comparação",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # NOVO: Mostrar quais municípios foram comparados
                    with st.expander("🔍 Ver municípios da comparação", expanded=False):
                        st.markdown("**Municípios usados para calcular cada média:**")
                        
                        for categoria, municipios_lista in municipios_por_categoria.items():
                            if len(municipios_lista) > 1:  # Só mostrar se tem mais de 1 município
                                municipios_str = ", ".join(municipios_lista)
                                st.markdown(f"**{categoria}** ({len(municipios_lista)} cidades): {municipios_str}")
                            else:
                                st.markdown(f"**{categoria}**: {municipios_lista[0]}")
                
                else:
                    st.warning("⚠️ Não foi possível calcular a comparação dinâmica. Verifique se as novas colunas de categoria estão disponíveis na planilha.")
            
            with col2:
                st.subheader("🏗️ Método WELL")
                
                # Buscar conexão com Método WELL
                if 'well_ods_connection' in data and not data['well_ods_connection'].empty:
                    well_connection = data['well_ods_connection'][
                        data['well_ods_connection']['ODS_Numero'] == selected_ods
                    ]
                    
                    if not well_connection.empty:
                        pilar = well_connection['Pilar_Well'].iloc[0]
                        descricao = well_connection['Descricao_Pilar'].iloc[0]
                        
                        st.markdown(f"""
                        <div style="background: {BACKGROUND_LIGHT}; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
                            <h4 style="color: #2d3748; margin-top: 0;">🏛️ {pilar}</h4>
                            <p>{descricao}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Conexão com Método WELL não encontrada")
                else:
                    st.info("Dados do Método WELL não disponíveis")
        else:
            st.warning(f"❌ Dados não encontrados ou inválidos para ODS {selected_ods} em {selected_municipio}")
    else:
        st.info("👆 Clique em um dos botões ODS acima para ver a análise detalhada")

def render_analise_comparativa_tab(data: Dict[str, Any]):
    """CORRIGIDO: Renderiza a aba de Análise Comparativa"""
    st.header("🔄 Análise Comparativa")
    
    # Filtros
    st.subheader("🎛️ Filtros")
    
    # Seleção de múltiplas cidades
    todos_municipios = []
    if 'ods_municipios' in data and not data['ods_municipios'].empty:
        todos_municipios = data['ods_municipios']['Municipio'].dropna().unique().tolist()
    
    selected_municipios = st.multiselect(
        "🏙️ Selecione os municípios para comparação:",
        todos_municipios,
        default=todos_municipios[:3] if len(todos_municipios) >= 3 else todos_municipios
    )
    
    if len(selected_municipios) < 2:
        st.warning("⚠️ Selecione pelo menos 2 municípios para comparação")
        return
    
    # Gráfico de barras comparativo
    st.subheader("📊 Comparação de Desempenho Médio")
    
    comparison_data = []
    for municipio in selected_municipios:
        municipio_data = data['ods_municipios'][data['ods_municipios']['Municipio'] == municipio]
        if not municipio_data.empty and 'IDS_Atual' in municipio_data.columns:
            scores = municipio_data['IDS_Atual'].dropna()
            if not scores.empty:
                media = scores.mean()
                if media <= 1:
                    media = media * 100
                comparison_data.append({'Município': municipio, 'Média (%)': media})
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        
        fig = px.bar(
            df_comparison,
            x='Município',
            y='Média (%)',
            title="📊 Comparação de Desempenho Médio entre Municípios (Dados Reais)",
            color='Média (%)',
            color_continuous_scale='Viridis',
            text=[format_percentage(v/100) for v in df_comparison['Média (%)']]
        )
        
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada com todos os 17 ODS
        st.subheader("📋 Tabela Detalhada - Todos os ODS")
        
        if selected_municipios:
            # Criar tabela comparativa
            tabela_comparativa = []
            
            for ods_num in range(1, 18):  # CORRIGIDO: usar ods_num em vez de ods_numero
                row = {'ODS': f"ODS {ods_num}", 'Nome': ODS_DEFINITIONS.get(ods_num, {}).get('nome', f'ODS {ods_num}')}
                
                for municipio in selected_municipios:
                    municipio_data = data['ods_municipios'][
                        (data['ods_municipios']['Municipio'] == municipio) &
                        (data['ods_municipios']['ODS_Numero'] == ods_num)  # CORRIGIDO: usar ods_num
                    ]
                    
                    if not municipio_data.empty and pd.notna(municipio_data['IDS_Atual'].iloc[0]):
                        score = municipio_data['IDS_Atual'].iloc[0]
                        row[municipio] = format_percentage(score)
                    else:
                        row[municipio] = "N/A"
                
                tabela_comparativa.append(row)
            
            df_tabela = pd.DataFrame(tabela_comparativa)
            st.dataframe(df_tabela, use_container_width=True, hide_index=True)

def render_metodo_well_tab(data: Dict[str, Any]):
    """TAREFA 4: Renderiza a aba do Método WELL com nomenclatura padronizada"""
    st.header("🏗️ Método WELL")
    
    if 'metodo_well' not in data or data['metodo_well'].empty:
        st.warning("⚠️ Dados do Método WELL não disponíveis")
        return
    
    well_data = data['metodo_well']
    
    st.subheader("🏛️ Pilares Estratégicos")
    
    for _, row in well_data.iterrows():
        if pd.isna(row.get('Pilar_Well')):
            continue
        
        with st.expander(f"🏛️ {row['Pilar_Well']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("📝 Descrição:")
                st.write(row.get('Descricao_Pilar', 'N/A'))
                
                st.markdown("🎯 ODS Relacionados:")
                st.write(row.get('ODS_Relacionados', 'N/A'))
            
            with col2:
                st.markdown("📋 Estratégias de Implementação:")
                st.write(row.get('Estrategias_Implementacao', 'N/A'))
                
                st.markdown("⚡ Ações Práticas:")
                st.write(row.get('Ações_Práticas', 'N/A'))

# CORREÇÃO 1: Função main modificada para usar session_state corretamente
def main():
    """Função principal da aplicação"""
    
    # Injeta CSS customizado
    DashboardComponents.inject_custom_css()
    
    # TAREFA 5: Renderiza cabeçalho redesenhado
    DashboardComponents.render_header()
    
    # CORREÇÃO 1: Inicializar estado da sessão
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = None
    if 'selected_ods' not in st.session_state:
        st.session_state.selected_ods = None
    if 'selected_estado' not in st.session_state:
        st.session_state.selected_estado = None
    if 'selected_municipio' not in st.session_state:
        st.session_state.selected_municipio = None
    
    # Carregar dados
    if st.session_state.dashboard_data is None:
        with st.spinner("🔄 Carregando dados reais da planilha..."):
            st.session_state.dashboard_data = ODSDataManager.load_data()
    
    data = st.session_state.dashboard_data
    
    if not data:
        st.stop()
    
    # CORREÇÃO 1: Renderizar sidebar e obter seleções do session_state
    selected_estado, selected_municipio = render_sidebar(data)
    
    # Atualizar session_state com as seleções atuais (sem modificar diretamente)
    # Em vez de modificar st.session_state.selected_estado, usamos as variáveis locais
    # O estado é mantido pelos widgets com keys únicas
    
    if not selected_municipio:
        st.error("❌ Selecione um município na barra lateral")
        st.stop()
    
    # CORREÇÃO 1: Lógica inteligente para verificar se o município é válido para o estado
    municipios_do_estado = ODSDataManager.get_municipios_by_estado(data, selected_estado)
    if selected_municipio not in municipios_do_estado:
        # Se o município não é válido para o estado, selecionar o primeiro da lista
        if municipios_do_estado:
            st.session_state.selected_municipio = municipios_do_estado[0]
            st.rerun()
    
    # Criar abas principais - NOVAS ABAS ADICIONADAS
    tab_names = ["🧭 IDS e ODS", "💡 Vantagens Estratégicas", "🎯 Visão Geral", "📊 ODS Detalhado", "🔄 Análise Comparativa", "🏗️ Método WELL"]
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        render_ids_ods_tab()
    
    with tabs[1]:
        render_vantagens_estrategicas_tab()
    
    with tabs[2]:
        render_visao_geral_tab(data, selected_municipio)
    
    with tabs[3]:
        render_ods_detalhado_tab(data, selected_municipio)
    
    with tabs[4]:
        render_analise_comparativa_tab(data)
    
    with tabs[5]:
        render_metodo_well_tab(data)

if __name__ == "__main__":
    main()