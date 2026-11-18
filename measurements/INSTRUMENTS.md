# What each instrument can see, and how it can be fooled

A running list, started on 17 November 2026. Every measurement in this folder leans on a counter that someone else runs. This file records what each one counts, how it has already misled us, and how someone could make it mislead on purpose. It holds no measurements of its own. Add to it whenever an instrument surprises us.

The reason it exists: Dan asked by voice on 17 November whether these statistics could themselves be manipulated as an attack. They can, so the plan for a personal "am I in a wave" tool was shelved, and this list is kept instead. The framing we agreed on is at the end: the metrics do not detect a lie. They narrow what kind of lie is still possible.

## Names

The piece calls it a **news wave** when coverage rises and events do not. `PROTOCOL-3.md` sets out the three rates. The idea is old and has several names.

| Name | From | What it says | How far it was checked |
| --- | --- | --- | --- |
| Key events | Kepplinger and Habermeier, *European Journal of Communication* 10(3), 1995, pp. 371 to 390 | After a key event the media report more on earlier events of the kind, give new ones more coverage and present both as like the key event. The impression is of more events "even if their actual number remains unchanged". Studied on AIDS, earthquakes and truck accidents. | Abstract read, through [Scilit](https://scilit.com/publications/15815f49b0a76bc33dea5606a5aaa533). Paper not opened. |
| Crime wave | Fishman, "Crime Waves as Ideology", first published in *Social Problems* in 1978 | A seven-week wave of reported crimes against the elderly in New York in late 1976, carried by three papers and five television stations and then nationally. Police statistics suggest there was probably no real wave. | Abstract of the 1984 reprint read, through [NCJRS](https://www.ncjrs.gov/App/Publications/abstract.aspx?ID=95776). The 1978 journal reference is from memory. |
| Media hype, news wave | Vasterman, "Media-Hype: Self-Reinforcing News Waves, Journalistic Standards and the Construction of Social Problems", 2005 | Coverage that feeds on itself after a trigger. | Title confirmed by search. Not opened. |
| Availability cascade | Kuran and Sunstein, 1999 | A vivid event makes a risk feel common, which draws more coverage, which makes it feel more common. | From memory. |
| Issue-attention cycle | Downs, 1972 | Public attention to a problem rises sharply and fades whether or not the problem changes. | From memory. |
| Frequency illusion | Zwicky, on Language Log, 2005 | Once something has your attention you notice it more and conclude it has become more common. Also called the Baader-Meinhof phenomenon. | From memory. This is the reader's side only: nothing in the world or in the coverage has to change. |

## The instruments

### 1. The operator's own account

A status page, a statement, a post-incident report.

- **Counts:** what the operator chooses to say, when it chooses to say it.
- **Has already misled us:** Amtrak gave two different explanations for the same evening. The Weather Service's denial covers its radars and one website, not its communications in general. Both are in `RESULTS.md`.
- **On purpose:** the operator can understate. That is the "account stays wrong" state in the model draft, and nothing the operator says later can rule it out. An outsider cannot forge this instrument without taking over the operator's own channel.
- **What catches it:** a party with direct sight and no stake, or a regulator.

### 2. Crowd reports (Downdetector)

- **Counts:** people saying they have a problem with a named service. How it turns reports into an "outage" is from memory and was not read: a count well above what is usual for that hour.
- **Has already misled us:** on 16 November the wires named up to six other banks beside Chase from user reports, and three of those said they had no problem (`RESULTS.md`, addendum). People report the brand they were using when something failed, not the system that failed.
- **On purpose:** a report costs nothing to file. Whether scripted reports are filtered out is not known to us. A spike with nothing behind it became a headline on the 16th with no attacker involved, so the route from fake reports to a real story is short.
- **What catches it:** the operator says it is fine and a probe-based counter is flat.
- **Also:** it publishes no archive that a script can read, so it cannot give us past weeks. The piece's footnote cannot use it as the event counter.

### 3. Probes (ThousandEyes, read through Network World)

- **Counts:** outage events seen on network paths from its own vantage points.
- **Has already misled us:** it reads high in 26% of past weeks, its level drifts through the year, and it did not rise in the weeks of the AWS, Azure or Cloudflare outages of late 2025 (`RESULTS.md`, part A). A bank's internal bug or a classified network never appears on it.
- **On purpose:** hard to inflate from outside, since that takes real failures on real paths. Easy to stay under: fail something it does not watch.
- **Also:** we read it at two removes, from a trade publication's running page, through a reader that returns summaries.

### 4. The news archive (GDELT)

- **Counts:** pages its crawlers saw that contain the words asked for.
- **Has already misled us:** not yet, because it has barely answered. Of 26 logged requests in the second round, 2 were answered.
- **Honest inflation:** syndication. One wire story on two hundred station sites is two hundred articles.
- **On purpose:** anyone who can publish pages that it crawls can add stories. This is the cheapest attack on the list. It needs no failure anywhere, only text.
- **What catches it:** counting distinct newsrooms, not pages, and holding to a list of outlets fixed beforehand.
- **A correction to something said by voice on 17 November.** It was suggested that the code planted on news sites through the marketing tool that week could alter what the archive sees. That code ran in the visitor's browser. An archive that reads the page as served, without running its scripts, would not see what the script drew. So that kind of compromise reaches readers, not the count, unless the crawler runs scripts. Whether GDELT's does is not established here.

### 5. Web search

- **Has already misled us:** it does not search by date and it returns whatever is prominent now. Asked about a week in March 2025 it returned eleven stories about 13 November 2026 (`RESULTS.md`, part B).
- **Standing:** not usable as a counter. Usable for finding a page whose date is then read from the page.

### 6. A single news story

- **Counts:** nothing. It is testimony.
- **Has already misled us:** a stale notice on one weather office's page was reported as a second federal outage within two hours of the ground stop.
- **On purpose, at the source:** the NSA story rests on one newsroom and six unnamed people. Copies on other sites are the same six people.
- **On purpose, at the page:** on 16 November a third party's script was live on 178 organisations' sites, three of an assumed ten large U.S. news sites among them, for at most 18 hours 50 minutes. It was built to steal, and nothing we have read says it altered an article. It shows that the route exists.
- **What catches it:** a second newsroom with its own sources. A copy published elsewhere after the window closed, as with the wire copy 17.5 hours later, rules out one thing only: that the story is an artefact of that compromise.

### 7. One reader's feed

- **Counts:** what was served to one person. Nobody else can see it.
- **Standing:** not measured, and the tool to measure it is shelved, for three reasons. Its verdict would compare the reader's count with the public coverage count, which is instrument 4 and can be padded. It would need a record of everything a person reads. And a single meter that tells people "it is only you" is worth attacking: whoever controls its baseline can make a real wave read as an illusion.

## What the instruments can settle between them

A wave can be made in four places: in the systems (a real failure, accidental or caused), in the counters (a report of a failure that did not happen), in the press (more stories per failure, or stories with no failure), and in one reader's feed. Each check below sets two instruments with different owners against each other.

| What is observed | What it rules out | What it leaves open |
| --- | --- | --- |
| The operator publishes a mechanism, and someone with direct sight agrees | A phantom: the failure happened | Accident or caused. That is the model's question, not this file's |
| Crowd reports spike, the operator says it is fine, probes are flat | A failure in the system | Honest misattribution or planted reports. The public count cannot tell them apart |
| Coverage rises and the event counters do not | A real cluster as the whole explanation | Whether the wave was pushed or grew by itself |
| Within the coverage: many pages, one newsroom | Independent confirmation | Whether that newsroom's sources are right |
| The story also ran where a known compromise could not reach, after it ended | The story as an artefact of that compromise | Everything about its sources |
| The page readers saw differs from the page as archived | An honest page | Who changed it, and for how many readers |
| One reader's count rises and public coverage is flat | A wave in the press | Noticing more, a feed that serves more, or a feed aimed at that reader |

**Signs that a wave was pushed, and their innocent twins.**

- Many outlets within minutes. A wire service does exactly this by design, so the timing means nothing until syndicated copies are collapsed to one.
- One origin. Most true stories also start in one place.
- A headline that claims more than the article under it supports. Headline writers do this unprompted. `PROTOCOL-3.md`, part N2, counts headlines for that reason.
- The shape of the curve. Crane and Sornette (2008) sorted bursts of attention into classes by how they decay, and their abstract reports three classes of exponent across nearly five million videos' daily views ([arXiv](https://arxiv.org/abs/0803.2189), abstract read). As recalled from the paper, not the abstract, the split is between bursts set off from outside and bursts that build from within. A real ground stop is a shock from outside too, so the shape separates "something happened" from "it spread by itself". It does not separate a true trigger from a planted one.

## What no public instrument separates

- A caused failure with an account that stays wrong. The model draft keeps this state on purpose and says the operator's own statements cannot remove it.
- A few real, small failures caused deliberately, followed by a wave that is entirely organic. From the first story outward nothing is forged. Only the root cause of each failure, and the base rate of small failures in a window, bear on it.
- A nudge to the first "is it a cyberattack?" story. It looks like an editor's ordinary judgment.

## This week, read through the table

As of 17 November. Every item is from the README, chapter 2 or `RESULTS.md`. Nothing here is new.

- **Microsoft and the FAA:** each has published a mechanism. Real failures. Whether the accounts are complete is the model's question.
- **Chase:** a mechanism from the bank itself, in one sentence, unverified by anyone else.
- **NSA Net:** one newsroom, unnamed sources. No instrument on this list can see a classified network.
- **Amtrak:** a knock-on of the ground stop, filed in our own table as a separate event three days later.
- **The Weather Service and Chase's neighbours:** phantoms, each with an innocent explanation on the record.
- **The marketing-tool compromise:** a real attack on the pages of news sites, with no report that it touched the news.
- **Coverage against events:** not measured. That is `PROTOCOL-3.md`.

Three of the week's reported failures turn out to be a knock-on or a phantom, and none of the three needed an attacker. Nothing measured so far says the wave was pushed. Nothing measured so far could have said so.

## Open questions about the instruments

1. Does GDELT's crawler run scripts on the pages it reads?
2. How does Downdetector decide a spike is an outage, and does it filter scripted reports? Its method page has not been read.
3. Is there any archive of crowd-report counts for past weeks?
4. Which domains are one newsroom? Without that map, counts of "distinct outlets" and any timing test are counts of syndication.
