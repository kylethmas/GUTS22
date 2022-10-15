from app.kobold_ai import generate_response, process_prompt
from app.stable_diffusion import get_image

def main(user_input):

    kobold_response = generate_response(user_input, "http://nasty-ravens-stare-104-198-213-42.loca.lt/api/v1/")

    image_prompt = correct_prompt + kobold_response + " - van gogh"

    print(correct_prompt + kobold_response)

    image_url = get_image(image_prompt)

    print(image_url)

    return [image_url]