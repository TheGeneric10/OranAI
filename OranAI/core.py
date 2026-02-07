from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, List, Tuple
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
    if any(greet in prompt_lower for greet in ("hello", "hi", "hey")):
      base_response.append("Hello! I'm OranAI, running fully locally.")

    if "plan" in prompt_lower:
      base_response.append("Plan: clarify goal, list steps, execute, review.")

    if not base_response:
      base_response.append(f"Answer: {prompt}")

    if self.config.model == "oran-t1":
      base_response.append("Mode: Oran-t1 delivers thorough reasoning and speed.")
      base_response.append(f"Timestamp: {now}")
    else:
      base_response.append("Mode: Oran-0.7 prioritizes rapid responses.")

    if self.history:
      recent = " | ".join(item[0] for item in list(self.history)[-3:])
      base_response.append(f"Context memory: {recent}")

    return "\n".join(base_response)
