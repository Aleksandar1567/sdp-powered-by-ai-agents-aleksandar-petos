import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParsedMessage:
    mentions: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)


class MessageParser:
    """Pure utility for extracting @mentions and links from post text."""

    _MENTION_RE = re.compile(r"@(\w+)")
    _LINK_RE = re.compile(r"https?://\S+")

    @staticmethod
    def parse(text: str) -> ParsedMessage:
        mentions = MessageParser._MENTION_RE.findall(text)
        links = MessageParser._LINK_RE.findall(text)
        return ParsedMessage(mentions=mentions, links=links)
