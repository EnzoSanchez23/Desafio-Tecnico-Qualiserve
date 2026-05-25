import streamlit as st
from agent import executar_agente

#Aba do navegador
st.set_page_config(
    page_title="NotícIAs Tech",
    page_icon="📰",
    layout="centered"
)

#Título e Subtítulo
st.title("📰 NotícIAs Tech")
st.caption("Agente Inteligente com busca em tempo real para o processo seletivo da Qualiserve.")

#Mensagem inicial ao abrir pagina
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Eu sou o seu Curador Tech. Pode me perguntar sobre qualquer lançamento, evento ou tendência tecnológica recente!"}
    ]

#Balão de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Input na parte inferior
if prompt := st.chat_input("Digite sua mensagem ou pergunta..."):
    
    #Mostra a mensagem do USUARIO
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    #Mostra a mensagem do AGENTE com animações
    with st.chat_message("assistant"):
        #Caixa de logs
        with st.status("Agente pensando...", expanded=True) as status:
            # Atualiza texto de forma dinamica
            resposta_final = executar_agente(prompt, callback_status=status)
            status.update(label="Processamento concluído!", state="complete", expanded=False)
        
        #Resposta final
        st.markdown(resposta_final)
        
    #Salva a resposta do assistente no histórico da sessão
    st.session_state.messages.append({"role": "assistant", "content": resposta_final})