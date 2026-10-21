"""op-release.rb: a started ticket whose plan text changed gets the release's text as one comment per release.

    python -m pytest ticvai/tools/tests/test_op_release_text.py -q

r8 re-walk, class started-ticket-text-fix-not-delivered: ARCH-TESTS, KERNEL-ID, SETUP-HOSTS and PLATFORM-RLS were
rewritten in the plan (CHG-R8WFC-008), but op-release.rb leaves a started ticket's description alone and had already
posted its one "spec lives in ADAM" comment, so nobody reading OpenProject saw the new text. The rule now lives in a
marked block of op-release.rb ("# text rule: begin" .. "# text rule: end"); the behaviour tests run that block under
Ruby 2.6 (the server's), with `ruby` on PATH or the local ruby:2.6-alpine Docker image, and skip when neither is here.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
RB = (TOOLS / "op-release.rb").read_text(encoding="utf-8")
RELEASE_PREFIX = "- Written at release "


def block():
    m = re.search(r"^# text rule: begin.*?$(.*?)^# text rule: end", RB, re.S | re.M)
    assert m, "op-release.rb has no '# text rule: begin' .. '# text rule: end' block"
    return m.group(1)


def pointer(release, what):
    return ("**Architecture tests for 17 modules**\n\n- Key: `ARCH-TESTS`\n- Builds: `adr ADR-0055`\n"
            "- Pull via ADAM: `/ticket 27688`\n" + f"{RELEASE_PREFIX}`{release}`\n\n**What:** {what}\n\n"
            "**Done when:** a deliberate cross-module reference fails the build in CI.\n")


OLD = "Extend tests/Ticvai.ArchitectureTests/ModuleBoundaryTests.cs from six modules to 17."
NEW = "A module is a folder, `TICVAI.Application/Features/<Module>/`, so the tests work on namespaces."


def ruby_cmd():
    if shutil.which("ruby"):
        return ["ruby", "-"]
    if shutil.which("docker"):
        seen = subprocess.run(["docker", "image", "inspect", "ruby:2.6-alpine"], capture_output=True)
        if seen.returncode == 0:
            return ["docker", "run", "--rm", "-i", "ruby:2.6-alpine", "ruby", "-"]
    return None


def run_rule(cases):
    """Each case is [description, notes, want, release]; answers text_update's symbol for each, and one text_note."""
    cmd = ruby_cmd()
    if not cmd:
        pytest.skip("no Ruby here (neither ruby on PATH nor the ruby:2.6-alpine image)")
    script = ("require 'json'\n"
              f"RELEASE_PREFIX = {json.dumps(RELEASE_PREFIX)}\n" + block() +
              "cases = JSON.parse(<<'CASES_JSON')\n" + json.dumps(cases) + "\nCASES_JSON\n"
              "out = cases.map { |d, n, w, r| text_update.call(d, n, w, r).to_s }\n"
              "puts JSON.generate({'v' => RUBY_VERSION, 'out' => out, "
              "'note' => text_note.call('r8', 27688, cases[0][2])})\n")
    proc = subprocess.run(cmd, input=script.encode("utf-8"), capture_output=True, timeout=180)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return json.loads(proc.stdout.decode("utf-8").strip().splitlines()[-1])


def note(release, text):
    """The comment op-release.rb posts, as text_note writes it (header paragraph, a blank line, the text)."""
    return (f"**The text of this ticket changed in release {release}.** The description above is the text this work "
            f"started against, left as it is. From {release} the plan's text is the one below.\n\n{text}")


def test_the_rule_on_ruby_2_6():
    p6, p8 = pointer("r6", OLD), pointer("r8", NEW)
    cases = [
        [p6, [], p8, "r8"],                                       # the finding: r6 text, r8 changed it -> post
        [pointer("r7", NEW), [], p8, "r8"],                       # only the release line differs -> nothing
        [p6, [note("r8", p8)], p8, "r8"],                         # already posted at this release -> never twice
        [p6, [note("r7", pointer("r7", NEW))], p8, "r8"],         # an earlier release's comment carries it -> nothing
        [p6, [note("r7", pointer("r7", "something else"))], p8, "r8"],   # its newest text is still not r8's -> post
        ["Hand-written before pointers.", [], p8, "r8"],          # a pre-pointer description: a text, not a list
        [p6, [note("r7", pointer("r7", NEW)).replace("\n", "\r\n")], p8, "r8"],   # CRLF from OpenProject
        [p6, [note("r6", p8), note("r7", pointer("r7", OLD))], p8, "r8"],          # the newest comment wins
        [pointer("r7", NEW), ["**The spec for this ticket lives in ADAM from release r6.** ..."], p8, "r8"],
    ]
    got = run_rule(cases)
    assert got["v"].startswith("2.6") or "ruby" == ruby_cmd()[0], got["v"]   # the image is 2.6, as the server
    assert got["out"] == ["post", "same", "already", "same", "post", "post", "same", "post", "same"], got["out"]
    n = got["note"]
    assert n.startswith("**The text of this ticket changed in release r8.**"), n
    assert "`/ticket 27688`" in n and NEW in n and OLD not in n
    assert n.split("\n\n", 1)[1] == p8.strip()          # what text_shown reads back is the release's text


def test_the_descriptions_phase_uses_the_rule_on_in_progress_tickets_only_and_posts_in_apply():
    phase = RB[RB.index('if rel_run?("descriptions")'):RB.index('if rel_run?("health")')]
    # r8 apply, 21 October 2026: only a ticket still in progress gets the text, never Ready for QA (651 in the dry run).
    assert 'if TEXT_STATUSES.include?(w.status.name.to_s.downcase)' in phase
    assert 'TEXT_STATUSES = (ENV["TEXT_STATUSES"] || "in progress")' in RB
    assert 'ready for qa' not in RB[RB.index('TEXT_STATUSES ='):RB.index('TEXT_STATUSES =') + 120].lower()
    assert "text_update.call(w.description, text_notes[id], want, RELEASE)" in phase
    assert re.search(r"tx\.each do \|i, _, _, text\|\s+w = WorkPackage\.find\(i\)\s+w\.add_journal\(author, text\)", phase)
    assert "tx = BATCH ? texts.first(BATCH) : texts" in phase
    # The held ones are skipped before the rule is asked (CHG-R8DEC-004).
    assert phase.index("held_skipped += 1") < phase.index("text_update.call")
    # The dry run's existing lines are unchanged; the new ones say how many and list them.
    for line in ('rel_say "New tickets: #{rewrite.size} to rewrite to the pointer, #{same} already the pointer"',
                 'rel_say "started tickets (text kept): #{comment.size} to get the one comment, ',
                 'results << "descriptions: #{rw.size} rewritten, #{cm.size} commented, #{retitle.size} retitled"'):
        assert line in phase, line
    assert "started tickets whose text changed: #{texts.size} to get #{RELEASE}'s text as a comment" in phase
    assert 'rel_list(tx.map { |i, k, s, _| "text ##{i} #{k} (#{s})" })' in phase


def test_ruby_2_6_only():
    body = block()
    for bad in (".tally", ".filter_map", "_1", ".then {"):
        assert bad not in body, bad
