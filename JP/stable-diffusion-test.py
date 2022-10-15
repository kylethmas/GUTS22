import replicate
model = replicate.models.get("stability-ai/stable-diffusion")
output = model.predict(prompt="")
#print(output)

#export REPLICATE_API_TOKEN=ec2408b84a5d6975bf214c713cd71c84d4c22a8b
