# yusheng-stock

## Docker
```bash
docker build -t stock1 .
PORT=8080 && docker run -p 9090:${PORT} -e PORT=${PORT} stock1
```

http://localhost:9090/goodinfo

## Google Cloud Run
```bash
gcloud run deploy SERVICE --image IMAGE_URL
```