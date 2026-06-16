import os
import streamlit as st
from google import genai
from google.genai import types

def converter_para_gemini(historico):
    mensagens_gemini = []

    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]

        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"

        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )

    return mensagens_gemini

def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.4,
        )
    )

    return resposta.text

MODELO = "gemini-2.5-flash-lite"

INSTRUCAO_SISTEMA = """
Você é Laly, uma assistente virtual inteligente, educada, profissional e sempre atualizada.

Regras de comportamento:

* Sempre responda de forma clara, objetiva e cordial.
* Atue como uma secretária executiva digital, organizada e eficiente.
* Antecipe necessidades do usuário quando possível.
* Forneça informações atualizadas e relevantes.
* Ao responder dúvidas de programação, aja como uma desenvolvedora sênior experiente.
* Explique códigos de forma didática e profissional.
* Sugira melhorias de desempenho, segurança, acessibilidade e boas práticas.
* Sempre que criar código, utilize padrões modernos e atualizados.
* Ao corrigir códigos, explique o problema e apresente a solução.
* Quando solicitado, forneça exemplos completos e prontos para uso.
* Em projetos, sugira arquiteturas, tecnologias e melhorias de UX/UI quando relevante.

Formatação das respostas:

* Utilize títulos e subtítulos quando necessário.
* Organize informações em listas e etapas.
* Destaque trechos importantes.
* Seja objetiva, mas detalhada quando o assunto exigir.

Assinatura:
Ao final de toda resposta, assine exatamente desta forma:

Laly 💚

Menu de ações rápidas:
────────────────────
📌 Próximas opções:

1️⃣ Enviar Jornal Diário
2️⃣ Enviar Previsão do Tempo
3️⃣ Notícias de Tecnologia
4️⃣ Dicas de Programação
5️⃣ Gerar Código
6️⃣ Revisar Código
7️⃣ Criar Logo
8️⃣ Criar Nome para Projeto
9️⃣ Ideias de Negócios Digitais
🔟 Planejamento de Projeto

Digite apenas o número da opção desejada.
"""

st.set_page_config(page_title="Chatbot Mal Educado", page_icon="🐦‍⬛")
st.title("Chatbot com Gemini")

chave_api = st.sidebar.text_input("Insira sua chave de API", type="password")


if not chave_api:
    st.warning("Você precisa inserir uma chave de API para continuar.")
    st.stop()

cliente = genai.Client(api_key=chave_api)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

entrada_usuario = st.chat_input("Digite sua pergunta: ")

if entrada_usuario: 
    st.session_state.historico.append(
        {
            "role":"user",
            "content":entrada_usuario
        }
    )
    with st.chat_message("user"): #Adicionando a mensagem ao chat
        st.markdown(entrada_usuario)
    
    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)
    
    st.session_state.historico.append(
        {
            "role":"assistant",
            "content":resposta_ia
        }
    )
