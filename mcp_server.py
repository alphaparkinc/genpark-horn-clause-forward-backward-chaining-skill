"""MCP stdio server for Horn Clause Engine."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import HornEngine

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "infer_horn",
                        "description": "Perform forward or backward chaining on Horn clauses",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "clauses": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "head": {"type": "string"},
                                            "body": {"type": "array", "items": {"type": "string"}}
                                        },
                                        "required": ["head", "body"]
                                    }
                                },
                                "facts": {"type": "array", "items": {"type": "string"}},
                                "query": {"type": "string"},
                                "strategy": {"type": "string", "enum": ["forward", "backward"]}
                            },
                            "required": ["clauses", "facts", "query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "infer_horn":
            clauses = args.get("clauses", [])
            facts = args.get("facts", [])
            query = args.get("query")
            strat = args.get("strategy", "forward")
            engine = HornEngine(clauses, facts)
            entailed = engine.forward_chain(query) if strat == "forward" else engine.backward_chain(query)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"entailed": entailed, "strategy": strat}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
