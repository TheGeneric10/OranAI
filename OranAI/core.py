from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, Dict, List, Tuple
from collections import deque


@dataclass
class OranAIConfig:
  model: str = "oran-t1"
  max_history: int = 6
  temperature: float = 1.0


@dataclass
class OranAI:
  config: OranAIConfig = field(default_factory=OranAIConfig)
  history: Deque[Tuple[str, str]] = field(default_factory=lambda: deque(maxlen=6))
  knowledge_base: Dict[str, List[str]] = field(
    default_factory=lambda: {
      "greeting": [
        "Hello! I'm OranAI, running fully locally.",
        "Hi! OranAI here, ready to help.",
        "Hey there — OranAI is online."
      ],
      "plan": [
        "Clarify the goal, list steps, execute in order, then review.",
        "Define scope, break into tasks, do the work, and verify.",
        "Start with the outcome, gather inputs, run the steps, and validate."
      ],
      "explain": [
        "Let's break it down into key parts and explain each one clearly.",
        "Here's the concept with a concise explanation and an example.",
        "I'll outline the idea and then add a quick illustration."
      ],
      "fallback": [
        "Here is a quick take:",
        "Here is a simple answer:",
        "Here is a thoughtful response:"
      ]
    }
  )

  def set_model(self, model: str) -> None:
    if model not in {"oran-t1", "oran-0.7"}:
      raise ValueError("Unsupported model. Use 'oran-t1' or 'oran-0.7'.")
    self.config.model = model

  def chat(self, prompt: str) -> str:
    prompt = prompt.strip()
    if not prompt:
      return "Please provide a prompt so I can respond."

    response = self._generate(prompt)
    self.history.append((prompt, response))
    return response

  def _generate(self, prompt: str) -> str:
    now = datetime.utcnow().strftime("%H:%M UTC")
    prompt_lower = prompt.lower()

    base_response: List[str] = []
    if self._matches(prompt_lower, ("hello", "hi", "hey", "yo")):
      base_response.append(self._pick("greeting"))

    if self._matches(prompt_lower, ("plan", "steps", "strategy", "roadmap")):
      base_response.append(f"Plan: {self._pick('plan')}")

    if self._matches(prompt_lower, ("explain", "why", "how does", "what is")):
      base_response.append(self._pick("explain"))

    if not base_response:
      base_response.append(f"{self._pick('fallback')} {prompt}")

    if self.config.model == "oran-t1":
      base_response.append("Mode: Oran-t1 delivers thorough reasoning and speed.")
      base_response.append(f"Timestamp: {now}")
    else:
      base_response.append("Mode: Oran-0.7 prioritizes rapid responses.")

    if self.history:
      recent = " | ".join(item[0] for item in list(self.history)[-3:])
      base_response.append(f"Context memory: {recent}")

    return "\n".join(base_response)

  def _matches(self, prompt_lower: str, keywords: Tuple[str, ...]) -> bool:
    return any(keyword in prompt_lower for keyword in keywords)

  def _pick(self, key: str) -> str:
    options = self.knowledge_base.get(key, [])
    if not options:
      return ""
    index = len(self.history) % len(options)
    return options[index]
