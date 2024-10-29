import streamlit as st
from openai import OpenAI
import time

# Configuración de la página con tema oscuro personalizado
st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="🤖",
    layout="wide"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    /* Estilo general */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Estilo para el contenedor principal */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Estilo para el título */
    .custom-title {
        font-family: 'Arial', sans-serif;
        color: #ffffff;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #2c3e50, #3498db);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Estilo para los mensajes */
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .user-message {
        background-color: #2c3e50;
        margin-left: 20%;
    }
    
    .bot-message {
        background-color: #34495e;
        margin-right: 20%;
    }
    
    /* Estilo para el input */
    .stTextInput > div > div > input {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Estilo para la sidebar */
    .css-1d391kg {
        background-color: #2c3e50;
    }
    
    /* Estilo para botones */
    .stButton > button {
        width: 100%;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }
    
    /* Estilo para el loader */
    .typing-loader {
        display: inline-block;
        margin-left: 1rem;
    }
    
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #ffffff;
        margin-right: 4px;
        animation: typing 1s infinite ease-in-out;
    }
    
    @keyframes typing {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* Estilo para el selector de modelo */
    .stSelectbox > div > div {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título personalizado
st.markdown("""
    <div class="custom-title">
        <h1>🤖 ChatGPT Clone</h1>
    </div>
""", unsafe_allow_html=True)

# Configuración de la sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Configuración</h2>", unsafe_allow_html=True)
    
    # API Key input
    api_key = st.text_input(
        "API Key de OpenAI",
        type="password",
        placeholder="Ingresa tu API key aquí...",
        help="Tu API key será usada de forma segura"
    )
    
    # Selector de modelo
    model = st.selectbox(
        "Selecciona el modelo",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0,
        help="Elige el modelo de lenguaje a utilizar"
    )
    
    # Ajustes avanzados
    with st.expander("🛠️ Ajustes avanzados"):
        temperature = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controla la creatividad de las respuestas"
        )
        
        max_tokens = st.slider(
            "Máximo de tokens",
            min_value=50,
            max_value=4000,
            value=2000,
            step=50,
            help="Límite de tokens por respuesta"
        )
    
    # Botón para limpiar chat
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = []
        st.experimental_rerun()

# Inicializar mensajes si no existen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor principal para el chat
chat_container = st.container()

# Mostrar mensajes
with chat_container:
    for message in st.session_state.messages:
        message_class = "user-message" if message["role"] == "user" else "bot-message"
        st.markdown(f"""
            <div class="chat-message {message_class}">
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Input del usuario
user_input = st.text_input(
    "",
    placeholder="Escribe tu mensaje aquí...",
    key="user_input"
)

# Procesar input del usuario
if user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostrar mensaje del usuario
    st.markdown(f"""
        <div class="chat-message user-message">
            {user_input}
        </div>
    """, unsafe_allow_html=True)
    
    # Simular respuesta del bot (aquí conectarías con OpenAI)
    with st.spinner('Pensando...'):
        if not api_key:
            st.error("Por favor, ingresa tu API key de OpenAI")
        else:
            try:
                client = OpenAI(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)
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                bot_response = response.choices[0].message.content
                
                # Agregar respuesta del bot
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                # Mostrar respuesta del bot
                st.markdown(f"""
                    <div class="chat-message bot-message">
                        {bot_response}
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #2c3e50; border-radius: 10px;'>
        <p>Desarrollado con ❤️ usando Streamlit</p>
    </div>
""", unsafe_allow_html=True)
