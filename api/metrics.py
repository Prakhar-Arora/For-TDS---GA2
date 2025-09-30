import json
import numpy as np

# Example data (same as before)
DATA = {
    "apac": {
        "latency": [100, 150, 200, 180, 170, 160, 190, 210],
        "uptime": [99.9, 99.7, 99.8, 99.6, 99.9, 99.85, 99.7, 99.8]
    },
    "amer": {
        "latency": [120, 130, 125, 140, 150, 160, 170, 180],
        "uptime": [99.8, 99.9, 99.7, 99.85, 99.9, 99.95, 99.6, 99.7]
    }
}

def calculate_metrics(latencies, uptimes, threshold):
    latencies_np = np.array(latencies)
    uptimes_np = np.array(uptimes)
    
    avg_latency = float(np.mean(latencies_np))
    p95_latency = float(np.percentile(latencies_np, 95))
    avg_uptime = float(np.mean(uptimes_np))
    breaches = int(np.sum(latencies_np > threshold))
    
    return {
        "avg_latency": avg_latency,
        "p95_latency": p95_latency,
        "avg_uptime": avg_uptime,
        "breaches": breaches
    }

def handler(request, context):
    try:
        body = json.loads(request.body)
        regions = body.get("regions", [])
        threshold_ms = body.get("threshold_ms")

        if threshold_ms is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "threshold_ms is required"}),
                "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST"}
            }

        response = {}
        for region in regions:
            if region not in DATA:
                response[region] = None
                continue
            metrics = calculate_metrics(DATA[region]["latency"], DATA[region]["uptime"], threshold_ms)
            response[region] = metrics

        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }
