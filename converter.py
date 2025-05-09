from cohere_client import transform_text


# A function that checks what tone is selected and sends the text to Cohere for transformation
def convert_text_to_tone(input_text, selected_tone):
    tones = {
        "Formal": "Rewrite the following text in a formal tone:",
        "Academic": "Rewrite the following text in an academic tone suitable for a research paper or scholarly article:",
        "Sarcastic": "Rewrite the following text in a sarcastic and witty tone:",
        "Angry": "Rewrite the following text to express anger, without using offensive language:",
        "Friendly": "Rewrite the following text in a friendly and conversational tone:",
    }

    # If tone is valid, call the Cohere client
    if selected_tone in tones:
        return transform_text(input_text, tones[selected_tone])
    else:
        return "Invalid tone selected."
