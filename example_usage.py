"""Example usage for EnterpriseSlideDeckNarrativeCompiler."""
import json
from client import EnterpriseSlideDeckNarrativeCompiler

def main():
    print("=== Enterprise Slide Deck Narrative Compiler Demo (Tencent WorkBuddy Goal-to-PPT) ===")
    compiler = EnterpriseSlideDeckNarrativeCompiler()

    meeting_doc = """
    Q3 Enterprise Autonomous Agent Strategy Report:
    - WorkBuddy managed agents adoption expanded by 310% quarter-over-quarter across finance and legal divisions.
    - Average time to deliver consolidated financial reports reduced from 4.5 days to 38 minutes.
    - Security audits passed 100% compliance with zero cross-tenant boundary leakage.
    - Action required: Executive committee approval for Q4 GPU inference budget allocation.
    """

    print("\n--- Compiling Executive Slide Deck Deliverable ---")
    deck = compiler.compile_deck_structure(
        deck_title="WorkBuddy Autonomous Agent Deployment & ROI",
        raw_document_text=meeting_doc,
        target_audience="EXECUTIVE_BOARD",
        target_slide_count=5
    )
    print(f"Generated Deck ID: {deck['deck_id']}")
    print(f"Total Slides: {deck['total_slides']} (Estimated Speech Duration: {deck['estimated_presentation_time_minutes']} min)")

    print("\nSlide 2 Outline Snapshot:")
    print(json.dumps(deck["slides"][1], indent=2))

    print("\n--- Presentation Timing Budget Breakdown ---")
    timing = compiler.estimate_presentation_timing(deck)
    for s in timing["slide_breakdown"]:
        print(f"Slide {s['slide_index']}: '{s['title']}' -> {s['allocated_seconds']}s")

if __name__ == "__main__":
    main()
