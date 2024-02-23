# To activate venv
# source /venv/bin/activate
# To Run python server locally with reload on change
# uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import keras
import base64
from io import BytesIO
from pydantic import BaseModel

loadModel = "FinalModel.keras"

app = FastAPI()

origins = [
    "http://localhost",
    "https://classificationofnumbers.onrender.com/",
    "https://classificationofnumbers.onrender.com/items",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000/items",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ImageObj(BaseModel):
    imageLink:str

@app.post("/items")
async def uploadItem(image: ImageObj):
    imageLink = image.imageLink
    # Extract the base64-encoded data from the data URL
    base64_data = imageLink.split(',')[1]
    # Decode the base64 data using base64 Library
    binary_data = base64.b64decode(base64_data)
    # Create a PIL Image object from binary data
    imageToProcess = Image.open(BytesIO(binary_data))
    # Convert to grayscale (i.e only excluding alpa channel)
    imageToProcess = imageToProcess.convert('L')
    # Resize the image to 28 x 28 Pixels
    imageToProcess = imageToProcess.resize((28, 28))
    # Convert image to NumPy array
    image_array = np.array(imageToProcess)
    # Inverting the image black and white pixels
    image_array = 255 - image_array
    # Creating image Object from numpy array to visualize the image
    image_test = Image.fromarray(image_array)
    # Saving the image to check if the image is ok to feed the model
    image_test.save('image.png', 'PNG')
    # Flatten the image array into a 1D array
    flattened_array = image_array.flatten()
    # Normalize pixel values to the range [0, 1]
    flattened_array = flattened_array / 255.0
    # Reshaping the array to match the input of the training data 
    flattened_array = flattened_array.reshape(1, 784)
    # Load Trained model to predict the number
    model = keras.models.load_model(loadModel)
    
    predictions = model.predict(flattened_array)
    
    print(list(predictions[0].astype(float)))
    max = 0
    # Simple Program to check which number or nueron is most activated
    for i in range(10):
        if(predictions[0][i] > predictions[0][max]):
            max = i
    # Return list of activations and the final output to frontend
    return {"prediction": list(predictions[0].astype(float)), "max": max}