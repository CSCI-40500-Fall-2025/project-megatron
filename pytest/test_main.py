import pytest
from fastapi import HTTPException

import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server.main as m

@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setattr(m, "API_KEY", "fake-key")

class TestTranslate:
    def test_translate_success_no_nouns_verbs(self, monkeypatch):
        """Basic successful translation when no nouns/verbs provided."""

        def fake_post(url, data):
            class FakeResp:
                status_code = 200

                def json(self):
                    return {
                        "data": {
                            "translations": [
                                {"translatedText": "hola", "detectedSourceLanguage": "es"}
                            ]
                        }
                    }

                text = "OK"

            return FakeResp()

        monkeypatch.setattr(m.requests, "post", fake_post)

        req = m.TranslateRequest(text="hello", target="es")
        res = m.translate_text(req)

        assert res["input"] == "hello"
        assert res["translatedText"] == "hola"
        assert res["detectedSourceLanguage"] == "es"
        assert res["translatedNouns"] == []
        assert res["translatedVerbs"] == []

    def test_translate_missing_detected_source_defaults_unknown(self, monkeypatch):

        def fake_post(url, data):
            class FakeResp:
                status_code = 200

                def json(self):
                    return {
                        "data": {"translations": [{"translatedText": "bonjour"}]}
                    }

                text = "OK"

            return FakeResp()

        monkeypatch.setattr(m.requests, "post", fake_post)

        req = m.TranslateRequest(text="hello", target="fr")
        res = m.translate_text(req)

        assert res["translatedText"] == "bonjour"
        assert res["detectedSourceLanguage"] == "unknown"

    def test_translate_with_nouns_and_verbs(self, monkeypatch):

        calls = []

        def fake_post(url, data):
            # record what was asked to translate
            calls.append(data.get("q"))

            class FakeResp:
                status_code = 200

                def json(self):
                    q = data.get("q")
                    # return translation that includes original text so we can assert
                    return {"data": {"translations": [{"translatedText": f"{q}_translated"}]}}

                text = "OK"

            return FakeResp()

        monkeypatch.setattr(m.requests, "post", fake_post)

        req = m.TranslateRequest(text="good morning", target="zh", nouns=["cat", "dog"], verbs=["run"])
        res = m.translate_text(req)

        # main text + 2 nouns + 1 verb -> 4 calls
        assert len(calls) == 4
        assert res["translatedText"] == "good morning_translated"
        # translatedNouns and translatedVerbs should preserve original items and translated results
        assert res["translatedNouns"] == [
            {"original": "cat", "translated": "cat_translated"},
            {"original": "dog", "translated": "dog_translated"},
        ]
        assert res["translatedVerbs"] == [{"original": "run", "translated": "run_translated"}]

    def test_translate_api_error_raises_http_exception(self, monkeypatch):

        def fake_post(url, data):
            class FakeResp:
                status_code = 500
                text = "Server error"

                def json(self):
                    return {}

            return FakeResp()

        monkeypatch.setattr(m.requests, "post", fake_post)

        req = m.TranslateRequest(text="will fail", target="zh")

        with pytest.raises(HTTPException) as excinfo:
            m.translate_text(req)

        assert excinfo.value.status_code == 500

    def test_translate_noun_api_error_bubbles_up(self, monkeypatch):

        # First call (main text) succeeds
        def fake_post(url, data):
            q = data.get("q")
            class FakeResp:
                text = ""

                def __init__(self, code):
                    self.status_code = code

                def json(self):
                    return {"data": {"translations": [{"translatedText": f"{q}_translated"}]}}

            if q == "will fail noun":
                return FakeResp(500)
            return FakeResp(200)

        monkeypatch.setattr(m.requests, "post", fake_post)

        req = m.TranslateRequest(text="ok", target="zh", nouns=["will fail noun"])

        with pytest.raises(HTTPException):
            m.translate_text(req)

    def test_translate_logs_messages(self, monkeypatch, caplog):

        # Make the HTTP call succeed
        def fake_post(url, data):
            class FakeResp:
                status_code = 200
                text = "OK"

                def json(self):
                    return {
                        "data": {
                            "translations": [{"translatedText": f"{data.get('q')}_translated"}]
                        }
                    }
            return FakeResp()

        monkeypatch.setattr(m.requests, "post", fake_post)

        # Capture logs at DEBUG level (lowest granularity level)
        caplog.set_level(logging.DEBUG, logger=m.logger.name)

        # Call translate_text
        req = m.TranslateRequest(
            text="hello world", 
            target="es",
            nouns=["cat", "dog"],
            verbs=["run"],
        )
        res = m.translate_text(req)

        # Assertions: make sure DEBUG logs captured main text, nouns, verbs
        messages = [record.getMessage().replace("'", "") for record in caplog.records]

        assert any("hello world" in msg for msg in messages)
        assert any("translatedText" in msg or "translations" in msg for msg in messages)
        assert any("Translating noun: cat" in msg for msg in messages)
        assert any("Translating noun: dog" in msg for msg in messages)
        assert any("Translating verb: run" in msg for msg in messages)