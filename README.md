# The vibe-code index — open data

For each of the most-used **premium WordPress plugins**: how much of it is code
you could get a coding agent to write, and how much is something a vendor is
*running* on your behalf.

Rendered at **[wp.md/vibe-code](https://wp.md/vibe-code/)**. This repo is the data
behind it, and the method used to produce it.

## Why this exists

"Can I just vibe-code it?" is a reasonable question to ask before renewing a
licence. For most SaaS the answer is a straight yes or no. For WordPress plugins
it usually isn't, because a premium licence is rarely paying for source code
alone.

Ask an agent for a security plugin and you'll get a firewall and a file scanner
in an evening. What you won't get is the rule that shipped this morning for the
vulnerability disclosed last night — that's a research team, and it's the entire
reason the product works.

So every plugin here is split in two: the share an agent could plausibly build,
and the share that only exists because somebody is running a data feed, a
server, a legal review, or an integration matrix kept alive against other
companies' breaking changes.

## Layout

| Path | What it is |
|---|---|
| `data/<slug>.json` | One record per plugin. 40 so far. |
| `data/schema.json` | JSON Schema for those records. CI validates against it. |
| [METHODOLOGY.md](METHODOLOGY.md) | How a score becomes a verdict. The money model. Stated limitations. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to argue with a number. |

Editorial fields are hand-written and open to pull requests. Everything under
`derived` is regenerated from wp.md's live tracking data and shouldn't be edited
by hand.

## The short version of the method

`moat` is 0–100: the share that is **not** code you could commission. The verdict
is a pure function of it, so the two can never drift apart:

| moat | verdict |
|---|---|
| 0–33 | Vibe-code it |
| 34–57 | Kinda |
| 58–74 | Not really |
| 75–100 | You're renting a service |

Build time is a bucket (`sitting` / `weekend` / `weekends` / `months`) calibrated
to 2026 agent tooling, not to hand-writing PHP. The money model counts
**maintenance only** — the build has stopped being the expensive part; owning the
thing forever hasn't.

Full detail, including what the model deliberately ignores, is in
[METHODOLOGY.md](METHODOLOGY.md).

## These are judgement calls

They're meant to be argued with. That's why the reasoning is written out in
`couldBuild` and `stillMissing` rather than hidden behind the number, and why the
whole dataset is here rather than in a database somebody else owns.

Verdicts are independent of sponsorship. wp.md sells sponsor slots; sponsors
appear in a labelled rail and have no influence on any score in this repo. If a
score ever looks bought, open an issue — that accusation should be cheap to make
and easy to check, which is most of the point of this repo existing.

## Prior art & credit

This index exists because of **[canivibecodeit.com](https://canivibecodeit.com/)**
by [Rob Hallam](https://github.com/canivibecodeit/canivibecodeit) ([MIT](https://github.com/canivibecodeit/canivibecodeit/blob/main/LICENSE)).
That project worked out the shape of this idea first, and three things here are
straightforwardly borrowed from it:

- **one JSON record per item, in public, with the pull request as the whole
  interface** — no forms, no accounts, no admin
- **a verdict as a small vocabulary** rather than a score nobody can read
- **shipping the actual prompt**, on the grounds that a page telling you
  something is buildable without telling you how is just an opinion

No code or data was copied — the schema, the scoring model and every record here
are our own — so nothing in the MIT licence is triggered. The credit is here
because it's deserved, not because it's required.

**Where this deliberately diverges.** canivibecodeit asks a binary question of
SaaS apps: can AI replace this. For WordPress plugins that question is the wrong
shape, because a premium licence is rarely paying for source code alone. So
instead of a yes/no we score the **split** — the share that is code, and the
share that is somebody running a data feed, a server, a legal review or an
integration matrix. The verdict is then derived from that number rather than
typed by hand, so the two can never drift apart. Our money model also counts
maintenance instead of build time, because with a 2026 coding agent the build
has stopped being the expensive part.

Different question, different answers, same conviction: the reasoning should be
public and arguable.

## Licence

Data is [CC BY 4.0](LICENSE) — use it, just say where it came from. If you build
something on top of it, we'd rather you did that than asked permission.
