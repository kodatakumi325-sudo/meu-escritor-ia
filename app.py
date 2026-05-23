import streamlit as st
from openai import OpenAI

# Título do seu Aplicativo
st.set_page_config(page_title="Editor de RP Profissional", page_icon="📖")
st.title("📖 De Roleplay a Livro Profissional")
st.markdown("---")

# Barra Lateral para Configurações
with st.sidebar:
    st.header("Configurações de Escrita")
    api_key = st.text_input("1. Cole sua Chave da OpenAI aqui:", type="password")
    genero = st.text_input("2. Gênero da Obra:", "Fantasia Romântica")
    st.info("A chave API você pega no site da OpenAI.")

# O Prompt mestre (Suas regras de ouro)
PROMPT_SISTEMA = f"""
Sou um autor e concluímos um Roleplay (RP). Você é meu Editor e Ghostwriter Profissional.
Sua Missão: Converter o log de RP em uma narrativa literária fluida em formato de livro.

Regras de Estilo:
1. Transformação Narrativa: Transforme descrições em parágrafos narrativos ricos e sensoriais.
2. Diálogos Naturais: Use a pontuação literária padrão (Travessão: — ). Remova nomes antes das falas.
3. Fidelidade: Preserve a personalidade dos personagens.
4. Ritmo: Escreva com calma, permitindo que os momentos respirem.
5. Volume: Escreva aproximadamente uma página (400 a 600 palavras).

Gênero: {genero}.
"""

# Área de entrada do LOG
st.subheader("Entrada de Dados")
log_input = st.text_area("Cole o Registro de Roleplay (Log) aqui:", height=300, placeholder="Cole aqui os diálogos e ações do seu RP...")

# Botão de ação
if st.button("Transformar em Página"):
    if not api_key:
        st.error("Ops! Você esqueceu de colocar a Chave API na barra lateral esquerda.")
    elif not log_input:
        st.warning("Por favor, cole o texto do seu RP primeiro.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('O Ghostwriter está redigindo sua página...'):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": PROMPT_SISTEMA},
                        {"role": "user", "content": log_input}
                    ],
                    temperature=0.7
                )
                
                texto_final = response.choices[0].message.content
                
                st.markdown("---")
                st.subheader("📚 Sua Página Literária")
                # Exibe o resultado em uma caixa fácil de copiar
                st.text_area("Texto pronto para seu Doc (Copie abaixo):", value=texto_final, height=600)
                st.success("Pronto! Agora é só copiar e colar no seu documento.")
                
        except Exception as e:
            st.error(f"Ocorreu um erro técnico: {e}")

st.markdown("---")
st.caption("Dica: Use logs que rendam uma cena completa para melhores resultados.")
