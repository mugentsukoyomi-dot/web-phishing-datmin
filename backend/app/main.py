from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.request_schema import URLRequest, PredictionResponse
from app.services.url_validator import check_url_exists
from app.services.predictor import predict

app = FastAPI(title="Phishing Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://phishing-detector-lake.vercel.app",  # ✅ tanpa "/" di akhir
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Phishing Detector API is running"}

@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: URLRequest):
    is_reachable, normalized_url, error_msg = check_url_exists(request.url)

    if not is_reachable:
        return PredictionResponse(
            url=normalized_url,
            reachable=False,
            message=error_msg,
        )

    result = predict(normalized_url)    

    return PredictionResponse(
        url=normalized_url,
        reachable=True,
        prediction=result["prediction"],
        confidence=result["confidence"],
        model_used=result["model_used"],
    )
