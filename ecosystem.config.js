module.exports = {
    "apps": [{
        "name": "service-python-feature-extractor",
        "script": "uvicorn app:app --workers 2 --host 0.0.0.0 --port 4446 --log-level critical",
        "instances": "1",
        "error_file" : "Logs/err.log",
        "out_file" : "Logs/out.log",
        "combine_logs": true,
        "timestamp": true,
        "log_date_format": "YYYY-MM-DD HH:mm:ss.SSS",
    }]
}
