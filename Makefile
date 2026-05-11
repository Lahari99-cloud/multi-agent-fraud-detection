install:
	pip install -r requirements.txt

generate:
	python data/generate_transactions.py --num-transactions 10000

train:
	python agents/detection_agent.py --train --input data/transactions.csv

run:
	python pipeline/run_pipeline.py --input data/transactions.csv --limit 20

api:
	uvicorn api.main:app --reload --port 8000

test:
	pytest -q

eval:
	python evaluation/fraud_eval.py --input data/transactions.csv --limit 1000
