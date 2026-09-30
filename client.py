"""
Enterprise Presentation & Slide Deck Narrative Structure Compiler (Zero External Dependencies)
Provides structured narrative decomposition, slide archetype selection, and presentation timing budgets.
"""
import time
import math
import hashlib
import re
import json
from typing import Dict, Any, List, Optional

SLIDE_ARCHETYPES = [
    "TITLE_HERO",
    "EXECUTIVE_SUMMARY_CARDS",
    "METRICS_3_COLUMN",
    "ARCHITECTURE_FLOW",
    "CHALLENGE_VS_SOLUTION",
    "STRATEGIC_ROADMAP_TIMELINE",
    "CONCLUSION_NEXT_STEPS"
]

class EnterpriseSlideDeckNarrativeCompiler:
    def __init__(self, words_per_minute_speech: int = 130):
        self.wpm = words_per_minute_speech

    def _extract_bullet_points(self, text: str, max_points: int = 4) -> List[str]:
        """Extracts key sentences as concise executive bullet points."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        bullets = []
        for line in lines:
            cleaned = re.sub(r"^[-*•\d.]+\s*", "", line)
            if len(cleaned) > 10:
                bullets.append(cleaned[:120])
            if len(bullets) >= max_points:
                break
        if not bullets:
            bullets = ["Key milestone delivered according to enterprise plan.", "Operational metrics aligned with strategic targets."]
        return bullets

    def compile_deck_structure(
        self,
        deck_title: str,
        raw_document_text: str,
        target_audience: str = "EXECUTIVE_BOARD",
        target_slide_count: int = 6
    ) -> Dict[str, Any]:
        """
        Transforms raw text or meeting summaries into an executive-grade structured slide deck.
        Assigns standard layout templates, structured card bodies, and speaker notes.
        """
        # Split text into sections or thematic blocks
        paragraphs = [p.strip() for p in raw_document_text.split("\n\n") if len(p.strip()) > 20]
        if not paragraphs:
            paragraphs = [raw_document_text]

        slides = []

        # 1. Slide 1: Title Hero
        slides.append({
            "slide_index": 1,
            "archetype": "TITLE_HERO",
            "title": deck_title,
            "subtitle": f"Prepared for {target_audience} • Strategic Execution Deliverable",
            "cards": [],
            "speaker_notes": f"Welcome everyone. Today we are presenting '{deck_title}' tailored for our {target_audience}.",
            "target_duration_seconds": 60
        })

        # 2. Slide 2: Executive Summary
        summary_points = self._extract_bullet_points(paragraphs[0] if paragraphs else "Strategic summary", max_points=3)
        slides.append({
            "slide_index": 2,
            "archetype": "EXECUTIVE_SUMMARY_CARDS",
            "title": "Executive Summary & Core Takeaways",
            "subtitle": "High-level strategic impact and operational outcomes",
            "cards": [{"heading": f"Priority {i+1}", "content": pt} for i, pt in enumerate(summary_points)],
            "speaker_notes": "To summarize up front: here are the three primary strategic takeaways requiring decision today.",
            "target_duration_seconds": 120
        })

        # 3. Intermediate Slides (Archetype rotation)
        archetype_cycle = ["METRICS_3_COLUMN", "CHALLENGE_VS_SOLUTION", "ARCHITECTURE_FLOW", "STRATEGIC_ROADMAP_TIMELINE"]
        remaining_slides = max(1, target_slide_count - 3)

        for i in range(remaining_slides):
            p_idx = min(i + 1, len(paragraphs) - 1)
            arch = archetype_cycle[i % len(archetype_cycle)]
            p_text = paragraphs[p_idx]
            pts = self._extract_bullet_points(p_text, max_points=3)

            slide_title = f"Operational Domain Analysis: Part {i+1}"
            if arch == "METRICS_3_COLUMN":
                slide_title = "Key Performance Indicators & Growth Vectors"
            elif arch == "CHALLENGE_VS_SOLUTION":
                slide_title = "Friction Points & Mitigation Architecture"
            elif arch == "ARCHITECTURE_FLOW":
                slide_title = "System Architecture & Cross-System Workflows"
            elif arch == "STRATEGIC_ROADMAP_TIMELINE":
                slide_title = "Phased Rollout Milestones & Deliverables"

            slides.append({
                "slide_index": len(slides) + 1,
                "archetype": arch,
                "title": slide_title,
                "subtitle": "Systemic breakdown and data validation",
                "cards": [{"heading": f"Dimension {j+1}", "content": b} for j, b in enumerate(pts)],
                "speaker_notes": f"On this slide, we dive into {slide_title.lower()}. Notice the specific metrics and flow dependencies.",
                "target_duration_seconds": 150
            })

        # 4. Final Slide: Next Steps & Immediate Decisions
        slides.append({
            "slide_index": len(slides) + 1,
            "archetype": "CONCLUSION_NEXT_STEPS",
            "title": "Decisions Required & Next Milestones",
            "subtitle": "Immediate actionable next steps for team sign-off",
            "cards": [
                {"heading": "Immediate Decision", "content": "Approve resource allocation and pilot rollout timeline."},
                {"heading": "Next 14 Days", "content": "Complete integration testing and security review sign-off."},
                {"heading": "Accountability Owner", "content": "Assigned to Lead Work Agent and Enterprise Project PM."}
            ],
            "speaker_notes": "To wrap up: here are the exact decisions required from the leadership team today to maintain schedule.",
            "target_duration_seconds": 90
        })

        total_duration_sec = sum(s["target_duration_seconds"] for s in slides)

        return {
            "deck_id": "GP-DECK-" + hashlib.sha256(deck_title.encode("utf-8")).hexdigest()[:12],
            "deck_title": deck_title,
            "target_audience": target_audience,
            "total_slides": len(slides),
            "estimated_presentation_time_minutes": round(total_duration_sec / 60.0, 1),
            "slides": slides
        }

    def estimate_presentation_timing(self, deck: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates speaking cadence and time allocations per slide."""
        slides = deck.get("slides", [])
        breakdown = []
        total_sec = 0

        for s in slides:
            notes = s.get("speaker_notes", "")
            words = len(notes.split())
            spoken_duration_sec = int((words / self.wpm) * 60) + 30 # buffer
            total_sec += spoken_duration_sec
            breakdown.append({
                "slide_index": s.get("slide_index"),
                "title": s.get("title"),
                "words_in_notes": words,
                "allocated_seconds": spoken_duration_sec
            })

        return {
            "total_estimated_duration_minutes": round(total_sec / 60.0, 1),
            "words_per_minute_pace": self.wpm,
            "slide_breakdown": breakdown
        }
