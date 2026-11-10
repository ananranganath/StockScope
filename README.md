   # StockScope

   A web app that estimates what a company is worth using a discounted cash flow (DCF) model and compares it with the current stock price.

   Built with React, TypeScript and FastAPI. Stock data comes from Yahoo Finance via yfinance.

   > For learning and research only. Not investment advice.

   ## Features so far
    - Search any stock ticker to see its price, sector, industry, market cap, and P/E ratio.
    - Price history chart (1 month, 6 months, 1 year, 5 years)
    - DCF valuation API: estimated value per share, upside vs. price, and a verdict, with adjustable growth, terminal growth, and discount rate

    ## Coming next

    - Valution section on the page, with sliders for the assumptions
    - Separate rabs for overview, chart, and valuation
    - Key metrics and recent news
    - AI-written investor summary
    - Deploying it as a public webite

    ## Running it locally

      You need Python 3.14 and Node.js.

      **Backend**

      ```
      cd backend
      py -3.14 -m venv .venv
      .venv\Scripts\activate
      pip install -r requirements.txt
      uvicorn main:app --reload
      ```

      The API runs at http://127.0.0.1:8000. Open http://127.0.0.1:8000/docs to try the endpoints.

      **Frontend** (in a second terminal)

      ```
      cd frontend
      npm install
      npm run dev
      ```

      Create `frontend/.env` containing `VITE_API_URL=http://127.0.0.1:8000`, then open http://localhost:5173.

      **Tests**

      ```
      cd backend
      python -m pytest
      ```