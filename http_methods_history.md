# HTTP Methods History

## HTTP/0.9 — 1991
Only one method existed:
- **GET** — fetch a document by URL. No headers, no status codes, just raw HTML back.

## HTTP/1.0 — 1996 (RFC 1945)
Three methods introduced:
- **GET** — retrieve a resource
- **POST** — send data to the server (forms, submissions)
- **HEAD** — like GET but returns only headers, no body (useful for checking if a resource exists)

## HTTP/1.1 — 1997 (RFC 2068), updated 1999 (RFC 2616)
The big expansion. Five new methods added:
- **PUT** — upload/replace a resource at a specific URL
- **DELETE** — remove a resource
- **OPTIONS** — ask the server what methods it supports
- **TRACE** — diagnostic tool, echoes the request back
- **CONNECT** — establish a tunnel (used for HTTPS through proxies)

This set of 8 methods stayed largely unchanged for over a decade.

## HTTP/1.1 update — 2010 (RFC 5789)
- **PATCH** — partial update to a resource (PUT replaces fully, PATCH modifies partially)

## HTTP/2 — 2015 (RFC 7540)
No new methods. HTTP/2 was about performance (multiplexing, compression, binary framing) not new semantics.

## HTTP/3 — 2022 (RFC 9114)
Again, no new methods. HTTP/3 moved to QUIC transport but kept the same method semantics.

## QUERY — 2023–present (IETF Draft)
A new method currently going through IETF standardization:
- **QUERY** — a safe, idempotent read request that allows a body

### Why it was needed
| Problem | Existing workaround | Why it is not ideal |
|---------|---------------------|---------------------|
| Complex search filters | PUT them in URL query string | URLs have length limits |
| Rich query body | Use POST | POST is not cacheable, not idempotent |
| Read with body | Use GET with body | GET body has no defined semantics, many servers and proxies ignore it |

QUERY fills the gap: read-only like GET, but with a proper request body like POST, and cacheable like GET.

### How the internet standardizes things

**IETF** (Internet Engineering Task Force) is the organization that defines how the internet works. They write the rules for HTTP, DNS, TLS, email, and most other internet protocols. Anyone can propose a new rule.

The process goes like this:

```
Someone has an idea
       ↓
Writes an Internet Draft (I-D)  ← informal, expires after 6 months, can change anytime
       ↓
IETF working group reviews and debates it
       ↓
Revised, updated, argued over (can take years)
       ↓
Published as an RFC  ← official standard, permanent, has a number (e.g. RFC 9110)
```

**RFC** stands for "Request for Comments" — a permanently published document that defines an internet standard. Once something becomes an RFC it gets a number and never changes. All major HTTP versions are RFCs:
- HTTP/1.0 → RFC 1945
- HTTP/1.1 → RFC 9110
- HTTP/2   → RFC 9113
- HTTP/3   → RFC 9114

**What this means for QUERY:**

`draft-ietf-httpbis-safe-method-w-body` is the draft name for the QUERY proposal. It is still in the debate/review stage — not yet an RFC, so technically not an official standard. This means:

- Browsers are not required to support it
- Proxies and CDNs may not cache it yet
- The spec could still change before becoming final

But the core idea is stable enough that curl supports it and servers like Python can implement it today — which is why we can already use it.

### Current status
- IETF draft: `draft-ietf-httpbis-safe-method-w-body`
- Not yet an RFC as of 2025
- Already supported by curl and can be implemented in any server (as shown — Python handles it natively via `do_QUERY`)

## Try it yourself

### Requirements
- Python 3 (no extra packages needed)
- curl

### Files
- `server.py` — the HTTP server that handles the QUERY method

### Step 1 — Start the server

Open a terminal and run:

```bash
python3 server.py
```

You should see:
```
Server listening on http://localhost:3000
Supports: QUERY /products
```

### Step 2 — Call it with curl

Open a second terminal and try these:

**Get all products:**
```bash
curl -X QUERY http://localhost:3000/products -H "Content-Type: application/json" -d '{}'
```

**Filter by category:**
```bash
curl -X QUERY http://localhost:3000/products -H "Content-Type: application/json" -d '{"category": "electronics"}'
```

**Filter by category + max price:**
```bash
curl -X QUERY http://localhost:3000/products -H "Content-Type: application/json" -d '{"category": "electronics", "maxPrice": 300}'
```

**Filter by category + max price + in stock only:**
```bash
curl -X QUERY http://localhost:3000/products -H "Content-Type: application/json" -d '{"category": "electronics", "maxPrice": 300, "inStock": true}'
```

**Pretty-print the response** (add `| python3 -m json.tool` at the end of any command):
```bash
curl -X QUERY http://localhost:3000/products -H "Content-Type: application/json" -d '{"category": "furniture"}' | python3 -m json.tool
```

**Try a wrong method to see 501:**
```bash
curl -v -X POST http://localhost:3000/products -H "Content-Type: application/json" -d '{}'
```

### Step 3 — Stop the server

Press `Ctrl+C` in the terminal where the server is running.

### What the server logs

Every QUERY request prints to the server terminal:
```
Received method: QUERY
[QUERY] filter: {"category": "electronics"} → 4 result(s)
```

### Available filters

| Filter | Type | Example |
|--------|------|---------|
| `category` | string | `"electronics"` or `"furniture"` |
| `maxPrice` | number | `300` |
| `inStock` | boolean | `true` or `false` |

---

## Timeline Summary

```
1991  GET
1996  GET  POST  HEAD
1997  GET  POST  HEAD  PUT  DELETE  OPTIONS  TRACE  CONNECT
2010  GET  POST  HEAD  PUT  DELETE  OPTIONS  TRACE  CONNECT  PATCH
2023+ GET  POST  HEAD  PUT  DELETE  OPTIONS  TRACE  CONNECT  PATCH  QUERY (draft)
```
