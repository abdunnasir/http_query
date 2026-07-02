from http.server import HTTPServer, BaseHTTPRequestHandler
import json

products = [
    {"id": 1, "name": "Laptop",     "category": "electronics", "price": 999, "inStock": True},
    {"id": 2, "name": "Phone",      "category": "electronics", "price": 699, "inStock": False},
    {"id": 3, "name": "Desk Chair", "category": "furniture",   "price": 299, "inStock": True},
    {"id": 4, "name": "Headphones", "category": "electronics", "price": 199, "inStock": True},
    {"id": 5, "name": "Bookshelf",  "category": "furniture",   "price": 149, "inStock": False},
    {"id": 6, "name": "Keyboard",   "category": "electronics", "price": 89,  "inStock": True},
]

class Handler(BaseHTTPRequestHandler):
    def do_QUERY(self):  # Python just needs a method named do_<METHOD>
        print(f"Received method: {self.command}")  # self.command holds the HTTP method
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        f = json.loads(body) if body else {}

        results = [p for p in products if
            (f.get("category") is None or p["category"] == f["category"]) and
            (f.get("maxPrice") is None or p["price"] <= f["maxPrice"]) and
            (f.get("inStock") is None or p["inStock"] == f["inStock"])
        ]

        print(f"[QUERY] filter: {f} → {len(results)} result(s)")
        response = json.dumps({"count": len(results), "results": results}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, *args): pass  # silence default access logs

print("Server listening on http://localhost:3000")
print("Supports: QUERY /products")
HTTPServer(("", 3000), Handler).serve_forever()
