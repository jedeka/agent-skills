# Media

When to leave prose, and what a figure must do.

## Contents

- [Choosing the form](#choosing-the-form)
- [Rules for every figure](#rules-for-every-figure)
- [Tables](#tables)
- [Diagrams](#diagrams)
- [Pages](#pages)
- [Video](#video)

## Choosing the form

| The content is | Use |
|----------------|-----|
| A reason, a cause, an argument | Prose |
| Several items compared on the same attributes | Table |
| Steps in order | Numbered list |
| Parts and how they connect | Box-and-arrow diagram |
| Messages between parties over time | Sequence diagram |
| States and the moves between them | State diagram |
| A hierarchy | Tree |
| A shape or a position in space | Geometric drawing |
| Quantities, a trend, a distribution | Chart |
| Behavior that depends on an input the reader should vary | Interactive page |

A figure replaces the paragraphs that would describe a shape. It does not replace the reasons, so the point, the mechanism, and the limits stay in prose.

For a reader who wants to understand, a figure beats a paragraph that describes a shape. An interactive page beats a static figure when a quantity must be varied. A narrated animation beats a page when the idea is a process in time. Each step up costs more to build and more to check, so climb only as far as the content needs.

## Rules for every figure

1. One message per figure. State the message in the caption as a full sentence: "A read during a partition returns stale data."
2. Use the same terms as the text. A label that differs from the prose reads as a new thing.
3. Label the parts directly. A legend makes the eye travel.
4. Keep to about seven elements. Past that, group the parts or split the figure.
5. Give each mark one meaning. If one arrow means "sends data to", every arrow means that.
6. Set the reading order left to right or top to bottom, in the order of the mechanism.
7. Say in prose what the figure shows. Some readers are on a terminal or use a screen reader.
8. Check every number and label in the figure against the ledger, as you would a sentence.

## Tables

- Rows are the items and columns are the attributes.
- A column holds one unit, named in the header.
- Place the items to compare in adjacent rows, so that the eye compares down a column.
- Two items with two attributes fit in a sentence. Use a table from three items up.

## Diagrams

Draw the concrete case first: the two replicas in Paris and Tokyo, before the general architecture.

The place where the output appears decides the format.

| Host | Format |
|------|--------|
| A terminal or plain chat | A text diagram in a code block, for five nodes or fewer. For more, a numbered list that names each connection. |
| A host that renders Mermaid | Mermaid. |
| A host that publishes HTML | Inline SVG in a page. |

If the host has its own skill or guide for diagrams, charts, or pages, load it first. That guide owns the visual craft. This file owns what the figure says.

## Pages

Build a page for `--as page`, or when the reader must vary an input to understand.

- Put the point at the top, in one or two sentences.
- Make the running case the interactive element. Give each variable one control. The controls start at the values used in the text.
- Show the precise statement beside the interaction, with the live values filled in.
- Let a control reach the region where the rule fails, and label the failure. A page teaches the limits that way.
- Add no motion or decoration that carries no message.
- Check every state the page can show. Test each control at both extremes; a page that is right only in its default view fails the ledger test.

## Video

A narrated explainer follows the same route, with one scene per stage. This skill ends at the script and the storyboard: a table with one row per scene that gives the narration, what is on screen, and what changes. The narration obeys the sentence rules. Rendering needs tools outside this skill, such as an animation library and a text-to-speech service.
