import streamlit as st
import google.generativeai as genai

# Configuração visual do site
st.set_page_config(page_title="Editor de RP Profissional", page_icon="📖")
st.title("📖 De Roleplay a Livro")
st.markdown("---")

# Barra Lateral
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("1. Cole sua Chave do Google aqui:", type="password")
    genero = st.text_input("2. Gênero da Obra:", "Fantasia Romântica")
    st.info("Usando a tecnologia do Google Gemini.")

# O Prompt Mestre
PROMPT_SISTEMA = f"""
Atue como meu Editor e Ghostwriter Profissional. 
Sua missão: Converter o log de diálogos e ações de um Roleplay em uma narrativa literária fluida.

Regras:
1. Transformação: Mude descrições secas para parágrafos ricos e sensoriais.
2. Diálogos: Use apenas travessões (—). Remova nomes antes das falas.
3. Ritmo: Mantenha um fluxo de livro (aprox. 500 palavras).
Gênero: {genero}.
"""

# Entrada do Log
log_input = st.text_area("Cole o Registro de RP aqui:", height=300)

if st.button("Transformar em Página"):
    if not api_key:
        st.error("Cole a Chave API na esquerda!")
    elif not log_input:
        st.warning("O log está vazio.")
    else:
        try:
            # AJUSTE AQUI: Mudamos o nome para gemini-1.5-flash
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('O Ghostwriter está trabalhando...'):
                response = model.generate_content(PROMPT_SISTEMA + "\n\nLog:\n" + log_input)
                
                st.markdown("---")
                st.subheader("📚 Sua Página Literária")
                st.text_area("Resultado:", value=response.text, height=600)
                st.success("Pronto! Copie para o seu Doc.")
                
        except Exception as e:
            # Se o erro 404 persistir, vamos tentar o modelo Pro como reserva
            st.error(f"Erro ao acessar o modelo. Tente novamente em instantes.")
            st.info("Dica: Verifique se sua chave API não tem espaços sobrando ao colar.")
