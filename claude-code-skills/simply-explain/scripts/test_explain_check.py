#!/usr/bin/env python3
"""Run: python3 scripts/test_explain_check.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from explain_check import check, split_sentences  # noqa: E402


def names(text, **kw):
    return [f["check"] for f in check(text, **kw)["findings"]]


class Acronyms(unittest.TestCase):
    def test_never_defined(self):
        self.assertIn("undefined_acronym", names("The TTL controls how long the entry lives."))

    def test_long_form_then_parenthesis(self):
        self.assertNotIn("undefined_acronym",
                         names("Each entry has a time to live (TTL). The TTL is 60 seconds."))

    def test_acronym_then_long_form(self):
        self.assertNotIn("undefined_acronym",
                         names("Each entry has a TTL (time to live) of 60 seconds."))

    def test_used_before_definition(self):
        found = check("The TTL is 60 seconds. It is short. A time to live (TTL) is a lifetime.")["findings"]
        self.assertTrue(any("before its definition" in f["message"] for f in found))

    def test_definition_in_next_sentence_is_in_time(self):
        self.assertNotIn("undefined_acronym",
                         names("The TTL is 60 seconds. TTL stands for time to live."))

    def test_named_for(self):
        self.assertNotIn("undefined_acronym",
                         names("The CAP theorem, named for three properties, limits databases."))

    def test_defined_by_genus(self):
        self.assertNotIn("undefined_acronym", names("A TTL is a number of seconds."))

    def test_known_flag_and_reader(self):
        self.assertNotIn("undefined_acronym", names("The TTL expires.", known={"TTL"}))
        self.assertIn("undefined_acronym", names("The API returns a list."))
        self.assertNotIn("undefined_acronym", names("The API returns a list.", reader="technical"))

    def test_version_suffix_on_known_acronym(self):
        self.assertNotIn("undefined_acronym", names("The spec is ASD-STE100.", known={"ASD", "STE"}))
        self.assertIn("undefined_acronym", names("The spec is ASD-STE100."))

    def test_code_and_capitalized_words_ignored(self):
        self.assertNotIn("undefined_acronym", names("Set `MAX_TTL` first. NOTE: this is required."))

    def test_definition_in_heading_counts(self):
        self.assertNotIn("undefined_acronym",
                         names("## Time to live (TTL)\n\nThe TTL is 60 seconds."))


class Sentences(unittest.TestCase):
    def test_abbreviations_and_decimals_do_not_split(self):
        got = split_sentences("Use a small rate, e.g. 0.01, not 1.5. Then train.")
        self.assertEqual(len(got), 2)

    def test_sentence_may_open_with_code(self):
        got = split_sentences("All flags are optional. code names the reader. code sets length.")
        self.assertEqual(len(got), 3)

    def test_long_sentence_is_fix(self):
        long = "The cache " + "stores the value and " * 9 + "returns it."
        result = check(long)
        self.assertEqual(result["verdict"], "fix")
        self.assertIn("long_sentence", [f["check"] for f in result["findings"]])

    def test_length_share(self):
        mid = "The server reads the request and then checks every single header field " \
              "against the list of rules that the operator wrote in the main configuration file today."
        self.assertIn("length_share", names(" ".join([mid] * 6)))

    def test_long_paragraph(self):
        self.assertIn("long_paragraph", names(" ".join(["The node sends one message."] * 31)))
        self.assertNotIn("long_paragraph", names(" ".join(["The node sends one message."] * 9)))

    def test_list_items_are_separate(self):
        text = "\n".join(f"- The node sends message {i}." for i in range(40))
        self.assertNotIn("long_paragraph", names(text))


class Wording(unittest.TestCase):
    def test_skipped_step_words(self):
        for s in ("Obviously the sum converges.", "Clearly, the loop ends.",
                  "You simply call the function.", "It is easy to see that x is even.",
                  "The proof is straightforward."):
            self.assertIn("skipped_step", names(s), s)

    def test_legitimate_uses_pass(self):
        for s in ("State the claim more clearly.", "The space is simply connected.",
                  "The kernel has only the trivial solution."):
            self.assertNotIn("skipped_step", names(s), s)

    def test_quoted_and_code_mentions_pass(self):
        self.assertEqual(names('Cut "obviously" and `simply call` from the draft.'), [])

    def test_minimizer(self):
        self.assertIn("minimizer", names("A tensor is just a grid of numbers."))

    def test_analogy_needs_a_limit(self):
        self.assertIn("analogy_without_limit",
                      names("Think of voltage as water pressure in a pipe."))
        self.assertNotIn("analogy_without_limit",
                         names("Think of voltage as water pressure in a pipe. "
                               "Unlike water, charge does not spill from an open wire."))

    def test_talking_about_analogies_is_not_using_one(self):
        self.assertNotIn("analogy_without_limit",
                         names("An analogy is a different thing with the same structure."))
        self.assertIn("analogy_without_limit",
                      names("By analogy with heat, charge flows from high potential to low."))

    def test_vague_magnitude(self):
        self.assertIn("vague_magnitude", names("The index makes the query much faster."))
        self.assertNotIn("vague_magnitude", names("The index makes the query much faster: 3 ms."))

    def test_bare_this(self):
        self.assertIn("bare_this", names("The lock is held. This causes a delay."))
        self.assertNotIn("bare_this", names("The lock is held. This delay costs 5 ms."))
        self.assertNotIn("bare_this", names("The lock is held. This is why the call waits."))

    def test_hedge_stack(self):
        self.assertIn("hedge_stack", names("The drug may possibly lower the risk."))
        self.assertNotIn("hedge_stack", names("The drug may lower the risk."))

    def test_forward_reference(self):
        self.assertIn("forward_reference", names("As we will see, the bound is tight."))

    def test_passive_with_actor(self):
        self.assertIn("passive_with_actor", names("The result is stored by the cache."))
        self.assertNotIn("passive_with_actor", names("The total is divided by the count."))
        self.assertNotIn("passive_with_actor", names("The zero vector is excluded by definition."))

    def test_as_if_is_not_an_analogy(self):
        self.assertNotIn("analogy_without_limit",
                         names("Every read returns the latest write, as if one copy existed."))

    def test_term_variants(self):
        self.assertIn("term_variants",
                      names("Load the dataset first. Each data set has a label column."))
        self.assertNotIn("term_variants", names("We do it every day. It is an everyday task."))
        self.assertNotIn("term_variants",
                         names("A real-time system answers fast. It answers in real time."))

    def test_chat_filler(self):
        self.assertIn("chat_filler", names("Great question! A hash maps keys to slots."))
        self.assertIn("chat_filler", names("A hash maps keys to slots. I hope this helps!"))


class Shape(unittest.TestCase):
    def test_clean_text(self):
        text = ("A hash table stores each key in a numbered slot. A hash function turns the key "
                "into the slot number, so a lookup goes to one slot and skips the rest.")
        result = check(text)
        self.assertEqual(result["verdict"], "clean")
        self.assertEqual(result["findings"], [])

    def test_line_numbers(self):
        text = "First line is fine.\n\nSecond block.\nObviously this line is flagged."
        found = [f for f in check(text)["findings"] if f["check"] == "skipped_step"]
        self.assertEqual(found[0]["line"], 4)

    def test_contents_links_are_labels(self):
        text = "- [The TTL field](#the-ttl-field)\n\nA time to live (TTL) is a lifetime."
        self.assertEqual(names(text), [])

    def test_fenced_code_and_frontmatter_ignored(self):
        text = "---\nname: x\n---\n\nRun it:\n\n```\nobviously TTL simply\n```\n\nThe run ends."
        self.assertEqual(names(text), [])

    def test_non_english_declined(self):
        text = "El gato come pescado todos los días y duerme mucho por la tarde. " * 4
        self.assertTrue(check(text).get("non_english"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
