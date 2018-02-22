clean:
	rm -f conglomerator.db && python3 makeDB.py

run:
	python3 app.py
