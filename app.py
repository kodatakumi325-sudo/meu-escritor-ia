import streamlit as st
import google.generativeai as genai

# Configuração visual do site
st.set_page_config(page_title="Editor de RP Profissional (Grátis)", page_icon="📖")
st.title("📖 De Roleplay a Livro (Modo Grátis)")
st.markdown("---")

# Barra Lateral
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("1. Cole sua Chave do Google aqui:", type="password")
    genero = st.text_input("2. Gênero da Obra:", "Fantasia Romântica")
    st.info("O Google Gemini está sendo usado como motor de escrita.")

# O Prompt (Regras de ouro do seu Ghostwriter)
PROMPT_SISTEMA = f"""
Atue como meu Editor e Ghostwriter Profissional. 
Sua missão: Converter o log de diálogos e ações de um Roleplay (RP) em uma narrativa literária fluida em formato de livro.

Regras de Estilo:
1. Transformação Narrativa: Não apenas copie o texto. Transforme descrições de ações em parágrafos narrativos ricos e sensoriais.
2. Diálogos Naturais: Use a pontuação literária padrão (Travessão: — ). Remova as aspas das falas e retire os nomes dos personagens antes das falas.
3. Fidelidade ao Personagem: Preserve a personalidade dos personagens.
4. Foco Sensorial: Mantenha cheiros, sons e o clima.
5. Ritmo: Escreva com calma, permitindo que os momentos emocionantes respirem.
6. Extensão: Escreva exatamente uma página de livro (aproximadamente 500 a 600 palavras).

O gênero desta obra é: {genero}. Adapte o vocabulário para esse estilo.
"""

# Área de entrada
log_input = st.text_area("Cole o Registro de RP (Log) aqui:", height=300, placeholder="Cole os diálogos e ações aqui...")

if st.button("Transformar em Página"):
    if not api_key:
        st.error("Ops! Você esqueceu de colocar a Chave do Google na barra lateral esquerda.")
    elif not log_input:
        st.warning("Por favor, cole o texto do seu RP primeiro.")
    else:
        try:
            # Configura o "motor" do Google
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('O Ghostwriter está redigindo sua página...'):
                # Envia o comando para a inteligência do Google
                # Aqui o prompt mestre e o log são unidos
                conteudo_total = PROMPT_SISTEMA + "\n\nRegistro de Roleplay (Log):\n" + log_input
                response = model.generate_content(conteudo_total)
                
                st.markdown("---")
                st.subheader("📚 Sua Página Literária")
                # Exibe o texto em uma caixa fácil de copiar
                st.text_area("Resultado pronto (Copie abaixo):", value=response.text, height=600)
                st.success("Pronto! Agora é só copiar e colar no seu documento.")
                
        except Exception as e:
            st.error(f"Erro técnico: {e}. Verifique se sua chave está correta.")

st.markdown("---")
st.caption("Ferramenta de uso privado para tradução literária de Roleplays.")
