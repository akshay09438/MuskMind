from unittest.mock import MagicMock


def make_fake_retriever(chunks):
    r = MagicMock()
    r.retrieve.return_value = chunks
    return r


def make_fake_anthropic(stream_texts):
    mock_client = MagicMock()
    events = []
    for text in stream_texts:
        evt = MagicMock()
        evt.type = "content_block_delta"
        evt.delta = MagicMock()
        evt.delta.text = text
        events.append(evt)
    mock_stream = MagicMock()
    mock_stream.__iter__ = lambda self: iter(events)
    mock_stream.__enter__ = lambda self: self
    mock_stream.__exit__ = MagicMock(return_value=False)
    mock_client.messages.stream.return_value = mock_stream
    return mock_client


def test_yields_text_chunks():
    from backend.pipeline import stream_response
    retriever = make_fake_retriever([
        {"content": "rockets cost too much", "source": "book_a", "layer": "first", "score": 0.8}
    ])
    client = make_fake_anthropic(["Well,", " the thing is..."])
    result = list(stream_response("How do you think about cost?", [], retriever, client))
    assert result == ["Well,", " the thing is..."]


def test_calls_retrieve_with_correct_args():
    from backend.pipeline import stream_response
    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["ok"])
    list(stream_response("What about Mars?", [], retriever, client))
    retriever.retrieve.assert_called_once_with("What about Mars?", top_k=3, threshold=0.35)


def test_includes_history_in_messages():
    from backend.pipeline import stream_response
    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["sure"])
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello."},
    ]
    list(stream_response("Follow-up", history, retriever, client))
    call_kwargs = client.messages.stream.call_args.kwargs
    messages_sent = call_kwargs["messages"]
    assert any(m["content"] == "Hi" for m in messages_sent)
    assert any(m["content"] == "Follow-up" for m in messages_sent)


def test_skips_non_delta_events():
    from backend.pipeline import stream_response
    retriever = make_fake_retriever([])
    mock_client = MagicMock()
    good_evt = MagicMock()
    good_evt.type = "content_block_delta"
    good_evt.delta = MagicMock()
    good_evt.delta.text = "hello"
    bad_evt = MagicMock()
    bad_evt.type = "message_start"
    mock_stream = MagicMock()
    mock_stream.__iter__ = lambda self: iter([bad_evt, good_evt])
    mock_stream.__enter__ = lambda self: self
    mock_stream.__exit__ = MagicMock(return_value=False)
    mock_client.messages.stream.return_value = mock_stream
    result = list(stream_response("hi", [], retriever, mock_client))
    assert result == ["hello"]


def test_trims_history_to_last_6_turns():
    from backend.pipeline import stream_response
    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["ok"])
    history = []
    for i in range(10):
        history.append({"role": "user", "content": f"user msg {i}"})
        history.append({"role": "assistant", "content": f"assistant msg {i}"})
    list(stream_response("new question", history, retriever, client))
    call_kwargs = client.messages.stream.call_args.kwargs
    messages_sent = call_kwargs["messages"]
    assert len(messages_sent) <= 13
