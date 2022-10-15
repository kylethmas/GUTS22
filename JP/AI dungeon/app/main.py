from kobold_ai import generate_response, process_prompt
from stable_diffusion import get_image

def main(user_input, image_style):

    correct_prompt = process_prompt(user_input)

    kobold_response = generate_response(correct_prompt, "http://nasty-ravens-stare-104-198-213-42.loca.lt/api/v1/")

    image_prompt = correct_prompt + kobold_response + image_style

    #print(correct_prompt + kobold_response)

    image_url = get_image(image_prompt)

    #rint(image_url)

    return [image_url,correct_prompt,kobold_response]