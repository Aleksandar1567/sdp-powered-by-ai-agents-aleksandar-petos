from social_network.posting.message_parser import MessageParser


def test_parser_extracts_mention_usernames():
    # POSTING-BE-001.3-S1
    # GIVEN
    text = "Hey @alice and @bob!"

    # WHEN
    result = MessageParser.parse(text)

    # THEN
    assert result.mentions == ["alice", "bob"]
    assert result.links == []
