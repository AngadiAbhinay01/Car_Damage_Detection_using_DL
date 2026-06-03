from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from model_helper import predict
import os

app = FastAPI(
    title="Car Damage Detection API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Car Damage Detection API Running"
    }


@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    temp_file = "temp_file.jpg"

    try:
        contents = await file.read()

        with open(temp_file, "wb") as f:
            f.write(contents)

        prediction = predict(temp_file)

        return JSONResponse(
            status_code=200,
            content={
                "prediction": prediction
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)