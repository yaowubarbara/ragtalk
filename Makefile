.PHONY: backend frontend scrape ingest setup dev

# Install all dependencies
setup:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Run scrapers to collect data
scrape:
	cd backend && python3 -m scrapers.run_all

# Ingest scraped data into ChromaDB
ingest:
	cd backend && python3 -m ingestion.ingest

# Run scrapers + ingest in one step
data: scrape ingest

# Run backend development server
backend:
	cd backend && python3 -m uvicorn app.main:app --reload --port 8000

# Run frontend development server
frontend:
	cd frontend && npm run dev

# Run both backend and frontend (use two terminals, or run this in background)
dev:
	@echo "Run in two separate terminals:"
	@echo "  make backend"
	@echo "  make frontend"
