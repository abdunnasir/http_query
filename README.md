# http_query

A minimal Python server demonstrating the HTTP `QUERY` method — a new IETF draft method that enables safe, idempotent, cacheable requests with a body. Includes a reference on the full history of HTTP methods from 1991 to present.

## What is QUERY?

`QUERY` fills a gap in HTTP: a read-only request that can carry a body.

| Method | Has body? | Read-only? | Cacheable? |
|--------|-----------|------------|------------|
| GET    | No        | Yes        | Yes        |
| POST   | Yes       | No         | No         |
| QUERY  | Yes       | Yes        | Yes        |

It is currently an IETF draft (`draft-ietf-httpbis-safe-method-w-body`) — not yet an official RFC, but already usable with curl and Python today.

## Requirements

- Python 3 (no extra packages)
- curl

## Usage

### Start the server

```bash
python3 server.py
```

Output:
```
Server listening on http://localhost:3000
Supports: QUERY /products
```

### Query with curl

**Get all products:**
```bash
curl -X QUERY http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Filter by category:**
```bash
curl -X QUERY http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{"category": "electronics"}'
```

**Filter by category + max price:**
```bash
curl -X QUERY http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{"category": "electronics", "maxPrice": 300}'
```

**Filter by category + max price + in stock only:**
```bash
curl -X QUERY http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{"category": "electronics", "maxPrice": 300, "inStock": true}'
```

**Pretty-print the response:**
```bash
curl -X QUERY http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{"category": "furniture"}' | python3 -m json.tool
```

### Available filters

| Filter      | Type    | Example          |
|-------------|---------|------------------|
| `category`  | string  | `"electronics"` or `"furniture"` |
| `maxPrice`  | number  | `300`            |
| `inStock`   | boolean | `true` or `false` |

### Sample response

```json
{
  "count": 2,
  "results": [
    {"id": 4, "name": "Headphones", "category": "electronics", "price": 199, "inStock": true},
    {"id": 6, "name": "Keyboard",   "category": "electronics", "price": 89,  "inStock": true}
  ]
}
```

### Server logs

Every request prints to the server terminal:
```
Received method: QUERY
[QUERY] filter: {"category": "electronics", "maxPrice": 300} → 2 result(s)
```

## Files

- `server.py` — HTTP server implementing the QUERY method
- `http_methods_history.md` — history of HTTP methods from 1991 to present

## Further Reading

- IETF Draft: `draft-ietf-httpbis-safe-method-w-body`
- See `http_methods_history.md` for the full timeline and IETF standardization process
