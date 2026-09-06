from social_network.posting.message_parser import MessageParser


def test_posting_be_001_3_s1_given_at_mentions_when_parsed_then_extracted_in_order():
    # POSTING-BE-001.3-S1
    # GIVEN
    text = "Hey @alice and @bob!"

    # WHEN
    result = MessageParser.parse(text)

    # THEN
    assert result.mentions == ["alice", "bob"]
    assert result.links == []


def test_posting_be_001_3_s2_given_urls_when_parsed_then_links_extracted():
    # POSTING-BE-001.3-S2
    # GIVEN
    text = "Read this: https://example.com and http://foo.org"

    # WHEN
    result = MessageParser.parse(text)

    # THEN
    assert result.links == ["https://example.com", "http://foo.org"]
    assert result.mentions == []


def test_posting_be_001_3_s3_given_same_input_when_parsed_twice_then_identical_output():
    # POSTING-BE-001.3-S3
    # GIVEN
    text = "Hello @alice https://x.com"

    # WHEN
    result_one = MessageParser.parse(text)
    result_two = MessageParser.parse(text)

    # THEN
    assert result_one.mentions == result_two.mentions
    assert result_one.links == result_two.links
