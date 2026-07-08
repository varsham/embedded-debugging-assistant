from pydantic import BaseModel

class Explanation(BaseModel):
    error_summary: str
    what_happened: str
    common_causes: list[str] = []
    how_to_fix: str