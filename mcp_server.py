"""MCP Server for Enterprise Slide Deck Narrative Compiler."""
import sys
import json
import time
from client import EnterpriseSlideDeckNarrativeCompiler

compiler = EnterpriseSlideDeckNarrativeCompiler()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "compile_slide_deck_narrative":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "compile_deck_structure")
    if action == "compile_deck_structure":
        return compiler.compile_deck_structure(
            deck_title=args.get("deck_title", "Executive Strategy Sync"),
            raw_document_text=args.get("raw_document_text", "Meeting concluded with unanimous sign-off."),
            target_audience=args.get("target_audience", "EXECUTIVE_BOARD"),
            target_slide_count=int(args.get("target_slide_count", 6))
        )
    elif action == "estimate_presentation_timing":
        deck = compiler.compile_deck_structure(
            deck_title=args.get("deck_title", "Presentation"),
            raw_document_text=args.get("raw_document_text", "Sample notes.")
        )
        return compiler.estimate_presentation_timing(deck)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        res = compiler.compile_deck_structure("Q3 Financial Performance", "Revenue up 42%. Customer acquisition cost reduced by 18%.", "EXECUTIVE_BOARD", 5)
        assert res["total_slides"] >= 4
        timing = compiler.estimate_presentation_timing(res)
        assert timing["total_estimated_duration_minutes"] > 0
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "EnterpriseSlideDeckNarrativeCompiler", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "compile_slide_deck_narrative",
                            "description": "Compile enterprise goal-to-presentation deliverables: generate executive narrative outlines, assign slide layout archetypes, format card callouts, and compute presentation timing budgets.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["compile_deck_structure", "estimate_presentation_timing"]},
                                    "deck_title": {"type": "string"},
                                    "raw_document_text": {"type": "string"},
                                    "target_audience": {"type": "string"},
                                    "target_slide_count": {"type": "integer"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
