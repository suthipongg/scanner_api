module.exports = {
    "apps": [{
        "name": "service-python-feature-extractor",
        "script": "uvicorn app:app --workers 2 --host 0.0.0.0 --port 4445 --log-level critical",
        "instances": "1",
    }]
}
