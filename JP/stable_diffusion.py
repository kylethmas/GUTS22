import replicate
#pip install replicate
#export REPLICATE_API_TOKEN=ec2408b84a5d6975bf214c713cd71c84d4c22a8b

def getImage(image_prompt):
    model = replicate.models.get("stability-ai/stable-diffusion")
    image_output = model.predict(prompt=image_prompt)
    return image_output
