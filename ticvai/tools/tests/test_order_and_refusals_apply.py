"""Tests for tools/fix-order-and-refusals.py (CHG-R10GEN-004, CHG-R10GEN-005): the sentence it appends, in
every scalar style the contracts use, and only once.

    python -m pytest ticvai/tools/tests/test_order_and_refusals_apply.py -q
"""
import importlib.util
from pathlib import Path

import pytest
import yaml

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("oar", TOOLS / "fix-order-and-refusals.py")
oar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oar)

CONTRACT = """paths:
  /a:
    get:
      description: 'Lists the things. It''s paged.'
      operationId: listA
      summary: List A
  /b:
    get:
      operationId: listB
      summary: List B
      description: >
        Folded text
        over two lines.
      tags: [b]
  /c:
    get:
      operationId: listC
      summary: List C
      responses:
        '200': {description: ok}
  /d:
    get:
      operationId: listD
      description: Plain text
        continued.
      summary: List D
  /e:
    post:
      operationId: doE
      responses:
        '409':
          description: "The thing is already `done`."
          x-ticvai-problem-types: [thing-done]
"""
S = "Where `x` is null the row sorts after the rows that have it (NULLS LAST), and `id` breaks every tie."


def _op(text, path, verb="get"):
    return yaml.safe_load(text)["paths"][path][verb]


@pytest.mark.parametrize("op,path", [("listA", "/a"), ("listB", "/b"), ("listC", "/c"), ("listD", "/d")])
def test_the_sentence_is_appended_once_in_every_style(op, path):
    out, changed = oar.add_description(CONTRACT, op, S)
    assert changed
    d = _op(out, path)["description"]
    assert d.rstrip().endswith(S)
    assert oar.add_description(out, op, S) == (out, False)
    # nothing else in the operation moved
    before = {k: v for k, v in _op(CONTRACT, path).items() if k != "description"}
    assert {k: v for k, v in _op(out, path).items() if k != "description"} == before


def test_a_quoted_description_keeps_its_own_text():
    out, _ = oar.add_description(CONTRACT, "listA", "It's `y`.")
    assert _op(out, "/a")["description"] == "Lists the things. It's paged. It's `y`."


def test_a_plain_scalar_refuses_a_colon():
    with pytest.raises(SystemExit):
        oar.add_description(CONTRACT, "listD", "Also refused: `x`.")


def test_the_409_gains_the_sentence():
    s = "Also refused when the thing is `voided`; states/thing.yaml moves this call only from `open`."
    out, changed = oar.add_409(CONTRACT, "doE", s)
    assert changed
    assert _op(out, "/e", "post")["responses"]["409"]["description"] == "The thing is already `done`. " + s
    assert oar.add_409(out, "doE", s) == (out, False)


def test_tick_list():
    assert oar.tick_list(["a"]) == "`a`"
    assert oar.tick_list(["a", "b", "c"]) == "`a`, `b` or `c`"
