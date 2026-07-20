# FastAPI Lesson 2

A FastAPI application configured for serverless deployment on Vercel.

## Endpoints

- `GET /`: Welcome root endpoint
- `GET /health`: Health status check endpoint
- `GET /items/{item_id}`: Query item demo endpoint
- `POST /items`: Create item demo endpoint
- `GET /docs`: Interactive Swagger UI documentation

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run local server:
   ```bash
   python main.py
   ```
   Or with Uvicorn:
   ```bash
   uvicorn api.index:app --reload
   ```

3. Open in browser: `http://127.0.0.1:8000`

## Vercel Deployment

Deploy directly using Vercel CLI:
```bash
npx vercel
```

To deploy to production:
```bash
npx vercel --prod
```