---
name: organize_links_to_journal
description: Organizes tagged links from a source file into the daily journal structure.
---

# Organize Links To Journal

This skill sorts and categorizes news links (typically from `TempLinks.md`) into the appropriate sections of a daily journal file (e.g., `journals/2026_02_09.md`).

## Execution Instructions for AI
1.  **Read Source**: Read the list of links from the source file (`TempLinks.md`).
2.  **Read Target**: Read the target journal file. Identify existing sections (headers like `### ...`).
3.  **Categorize**: Assign each link to a section based on its hashtags and content.
4.  **Sort & Group**: Within each section, group links by company/topic and sort by importance.
5.  **Merge**: Append the organized links to the corresponding sections in the target file.
    - *Note*: Do not duplicate links if they already exist.
    - *Note*: Keep the original link format (`- [Title](URL) #Tags`).

## Categorization Rules (Priority Order)

1.  **### Tesla & SpaceX; Vehicle**
    - Tags: `#TSLA`, `#SpaceX`, `#EV`, `#FSD`, `#Robotaxi`, `#Waymo`.
    - *Note*: Even if it has `#AI`, if it's about Tesla/Waymo, it goes here.

2.  **### Taiwan**
    - Tags: `#TW`, `#TSM` (TSMC), `#MTK` (MediaTek), `#鴻海`, `#Foxconn`, and other Taiwan companies (#智邦, #中美晶, #創見 etc).
    - *Exception*: If it's purely about a global product launch, it might go to Tech, but usually Taiwan-specific news stays here.

3.  **### Crypto**
    - Tags: `#Crypto`, `#BTC`, `#ETH`, `#MSTR`, `#ETF` (if Bitcoin ETF), `#Stablecoin`, `#BlackRock` (if crypto related).

4.  **### Finance**
    - Tags: `#Finance`, `#Gold`, `#Silver`, `#stock` (General market news like Dow Jones, S&P 500), `#Fed`, `#Economy`.
    - *Note*: Individual tech stock news usually goes to "Tech Industry", but general market trends go here.

5.  **### Health & Food**
    - Tags: `#Health`, `#Food`, `#medicine`, `#LLY` (Eli Lilly), `#NVO`.

6.  **### Science & Technology**
    - Tags: `#science`, `#universe` (astronomy), `#biology` (if not medical), `#physics`, `#environment`, `#energy` (if scientific breakthrough).

7.  **### IT**
    - Tags: `#AI` (Research papers, Model releases, Open Source, Developer tools), `#LLM`, `#Agent`, `#OpenAI`, `#Claude`, `#Gemini` (the model, not the stock), `#Coding`, `#GitHub`.
    - *Distinction*: **Tech Industry** is for *Business/Stock/Corporate* news. **IT** is for *Technology/Product/Research* news.
    - Example: "Google stock falls" -> `Tech Industry`. "Google releases Gemini 1.5 paper" -> `IT`.

8.  **### Tech Industry** (Default for major tech)
    - Tags: `#NVDA`, `#MSFT`, `#GOOG`, `#AMZN`, `#AAPL`, `#META`, `#AMD`, `#INTC`, `#ORCL`, `#semicon`, `#Chips`.
    - *Fallback*: If it fits nowhere else but is tech news.

## Sorting Rules (Within Sections)

- **Grouping**: Always group links about the same company/topic together.
- **Ordering (Importance)**:
    - **Tech Industry**: `#NVDA` > `#MSFT` > `#GOOG`/`#Alphabet` > `#AMZN` > `#AAPL` > `#META` > `#AMD` > `#INTC` > Others.
    - **Taiwan**: `#TSM` (TSMC) > `#MTK` > `#鴻海` > Others.
    - **Crypto**: `#BTC` > `#ETH` > Others.

## Example
**Input:**
`- [NVIDIA stock jumps](...) #NVDA`
`- [New LLM method released](...) #AI #LLM`
`- [TSMC revenue up](...) #TSM #TW`

**Output (in Journal):**

### Tech Industry
- [NVIDIA stock jumps](...) #NVDA

### Taiwan
- [TSMC revenue up](...) #TSM #TW

### IT
- [New LLM method released](...) #AI #LLM
