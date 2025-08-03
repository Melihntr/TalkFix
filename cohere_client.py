import cohere

# Initialize Cohere Client with your API key
co = cohere.Client('')


# Function to get transformed text
import cohere

co = cohere.Client("hA3uR4xVJtQC95Mc8gxXCOr0ubywWMmBxs8NQSSF")  # your API key

def transform_text(input_text, instruction):
    prompt = f"{instruction}\n\n{input_text}"
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    return response.generations[0].text.strip()

