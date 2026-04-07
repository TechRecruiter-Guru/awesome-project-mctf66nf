# NotebookLM Video Script — SafetyCase.AI Demo
## Replaces: "2-Minute Loom Video Goes Here" Placeholder
## Runtime: ~2 minutes | Style: Conversational founder walkthrough

---

## SPEAKER NOTES (for NotebookLM source input)

Paste the sections below into NotebookLM as your source document, then use
"Generate Audio Overview" (podcast format) for a conversational two-host
deep dive, or feed it to your screen recording workflow as a teleprompter script.

---

## SCRIPT

**[OPENING — 0:00–0:15]**

Hi, I'm John Polhill — U.S. Air Force veteran, 27-year technical recruiting
veteran, and founder of SafetyCase.AI.

If you build Physical AI — humanoid robots, drones, cobots, autonomous
forklifts — you know the deal: your technology is ready, but your safety
documentation is a 6-month, $50,000 bottleneck that's blocking your funding
round and your first enterprise contract.

I built SafetyCase.AI to eliminate that bottleneck in minutes, not months.

---

**[THE PROBLEM — 0:15–0:35]**

Here's what I kept seeing after placing 1,000+ engineers at Microsoft, Intel,
Boston Dynamics-era companies, and 12+ Series A/B robotics startups:

Founders would close their seed round, build an incredible robot, then get
stuck for 6 months waiting on a compliance firm to produce a safety case
website — a $30K to $50K engagement — before the enterprise customer would
even sign an NDA.

Investors want it. Customers require it. But nobody had a fast, affordable way
to get it done.

---

**[THE SOLUTION — 0:35–1:05]**

SafetyCase.AI changes that. Here's the 5-step workflow:

**Step 1 — Choose your robot type.**
We have 8 industry-specific templates: humanoids, AMRs, cobots, drones,
inspection robots, construction equipment, healthcare robots, and autonomous
forklifts. Every template is pre-formatted for VC due diligence, OSHA
compliance, and regulatory submissions.

**Step 2 — Create your order and pay.**
$2,000 flat. No monthly fees. No subscriptions. One payment via PayPal or
Venmo, and your Order ID is generated instantly.

**Step 3 — Upload your safety PDF.**
Got an existing spec sheet, test report, or technical brief? Upload it.
Our Claude AI engine reads it and extracts every relevant safety data point
automatically.

**Step 4 — Review and edit.**
The AI populates your full safety case website — risk matrices, test validation
reports, hazard logs, mitigation strategies. You review it in the browser and
make any edits you need.

**Step 5 — Download your site.**
One click. You get a complete, self-contained HTML file with zero external
dependencies. Host it anywhere — Vercel, GitHub Pages, your own server — in
under 5 minutes.

---

**[SOCIAL PROOF — 1:05–1:25]**

Why trust SafetyCase.AI?

I spent 15 years helping build the safety engineering teams at companies like
NVIDIA and Boston Dynamics-era robotics firms. The templates in this product
were built by people who've shipped real robots into real industrial
environments — not generic web developers who learned about robots last year.

We also built this with military precision. Same philosophy I used to build
recruiting pipelines that deliver elite talent in 7 to 14 days: define the
standard, eliminate the waste, deliver on time.

98% placement success rate. 1,000+ engineers placed. 27+ years experience.
That same discipline is baked into every SafetyCase.AI template.

---

**[CALL TO ACTION — 1:25–2:00]**

Your Physical AI company deserves a safety case that matches the quality of
your technology.

Scroll down, pick your robot type, and have your investor-ready safety case
website in your hands today — not in 6 months, not for $50K.

If you have questions, email me directly at john@physicalaipros.com or connect
with me on LinkedIn. I personally review every order.

SafetyCase.AI — Military precision. AGI-powered execution.

Let's build.

---

## NOTEBOOKLLM PRODUCTION NOTES

### To generate the Audio Overview (podcast format):
1. Paste this entire document as a source in NotebookLM
2. Click "Generate" → "Audio Overview"
3. In the customization prompt, specify:
   - *"Make this a confident, direct founder pitch — not overly salesy. One
     narrator, conversational but authoritative. Emphasize the 5-step workflow
     and the $2,000 flat price as the key differentiators."*
4. Download the MP3 and pair with a screen recording of the SafetyCase.AI
   demo flow for the final video

### To record a screen-capture Loom instead:
- Use this script as teleprompter text
- Screen-record the live site: template selection → order page → upload flow →
  preview editor → download
- Target runtime: 90–120 seconds
- Upload to Loom and replace the placeholder embed in `app/page.tsx` at line 952

### Replacing the placeholder in code:
In `app/page.tsx` around line 950–962, replace the gray placeholder `<div>`
with a `<iframe>` (Loom) or `<video>` tag pointing to the finished video asset.
