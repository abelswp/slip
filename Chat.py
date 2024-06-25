import requests
import openai
import time

# Tu clave de API de OpenAI
openai.api_key = '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'
AUTHORIZATION = 'APP_USR-3279067117760088-062116-e9dfe84e415f2ae4c815c0e6385f66a9-234547054'

#url para tener acceso a los mensajes recibidos de mercado libre
url = "https://api.mercadolibre.com/my/received_questions/search"

payload = {}
headers = {
  'Authorization': 'Bearer ' + AUTHORIZATION,
}

# Función para obtener respuestas de ChatGPT
def obtener_respuesta(pregunta):
    response = openai.completions.create(
        model="gpt-3.5-turbo",
        prompt=pregunta,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def enviar_respuesta(question_id, respuesta):
    url_respuesta = "https://api.mercadolibre.com/answers"
    headers = {
        'Authorization': f'Bearer {AUTHORIZATION}',
        'Content-Type': 'application/json'
    }
    payload = {
        'question_id': question_id,
        'text': respuesta
    }
    response = requests.post(url_respuesta, json=payload, headers=headers)
    return response.status_code, response.json()

# Monitorea continuamente el endpoint para nuevas preguntas
def monitorear_preguntas():
    preguntas_procesadas = set()

    while True:
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json().get('questions', [])
            print(data)
            for pregunta in data:
                print(pregunta)
                pregunta_id = pregunta['id']
                print(pregunta_id)
                if pregunta_id not in preguntas_procesadas:
                    preguntas_procesadas.add(pregunta_id)
                    texto_pregunta = pregunta['text']
                    print(texto_pregunta)
                    respuesta = obtener_respuesta(texto_pregunta)

                    print(f"Pregunta: {texto_pregunta}")
                    print(f"Respuesta: {respuesta}")
                    print()

                    # Enviar la respuesta de vuelta a Mercado Libre
                    status_code, respuesta_api = enviar_respuesta(pregunta_id, respuesta)
                    if status_code == 201:
                        print(f"Respuesta enviada correctamente a la pregunta {pregunta_id}.")
                    else:
                        print(f"Error al enviar la respuesta a la pregunta {pregunta_id}: {respuesta_api}")

        else:
            print("Error al realizar la solicitud:", response.status_code)

        # Espera un intervalo de tiempo antes de la siguiente consulta
        time.sleep(30)  # Espera 30 segundos antes de volver a consultar


# Inicia la monitorización
monitorear_preguntas()
