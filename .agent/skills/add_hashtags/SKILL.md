---
name: add_hashtags
description: Appends relevant hashtags to journal entries based on content analysis. Intended for LLM execution.
---

# Add Hashtags To News Links

This skill is designed for an AI to parse news headlines/links and append relevant hashtags. It cannot be run as a simple script; it requires semantic understanding.

## Execution Instructions for AI
1.  Read the target file (usually a journal page or `TempLinks.md`).
2.  For each line containing a link, analyze the title and content.
3.  Append relevant hashtags to the end of the line, space-separated.
4.  **Do NOT remove existing tags.**
5.  **Use English for most tags unless specified.**

## Tagging Rules

### Entities & Stocks
- **US Stocks**: Use Ticker symbol. **Do NOT use company name.**
    - Tesla -> `#TSLA` (NOT `#Tesla`)
    - Google/Alphabet -> `#GOOG` (NOT `#Google`)
    - Microsoft -> `#MSFT`
    - Amazon -> `#AMZN`
    - Apple -> `#AAPL`
    - Meta -> `#META`
    - NVIDIA -> `#NVDA`
    - AMD -> `#AMD`
    - Intel -> `#INTC`
    - Oracle -> `#ORCL`
    - Softbank -> `#SFTBY` (NOT `#Softbank`)
    - Bloom Energy -> `#BE`
    - Applied Materials (應材) -> `#AMAT`
    - ASML (艾司摩爾) -> `#ASML`
    - SanDisk -> `#SNDK`
    - Cisco (思科) -> `#CSCO`
    - Coinbase -> `#COIN`
    - Cloudflare -> `#NET`
    - Spotify -> `#SPOT`
    - ARM -> `#ARM`
    - Micron (美光) -> `#MU`
    - Walmart (沃爾瑪) -> `#WMT`
    - Alibaba (阿里巴巴) -> `#BABA`
    - Tencent (騰訊) -> `#TCEHY`
    - Palantir -> `#PLTR`
    - Coupang (酷澎) -> `#CPNG`
    - Uber -> `#UBER`
    - Rivian -> `#RIVN`
    - Xiaomi (小米) -> `#XIACY`
    - Infineon (英飛凌) -> `#IFNNY`
    - Figma -> `#FIG`
    - Planet Labs -> `#PL`
    - Lego (樂高) -> `#LEGO`
    - Western Digital (威騰電子) -> `#WDC`
    - Estee Lauder (雅詩蘭黛) -> `#EL`
    - Infosys -> `#INFY`
    - CoreWeave -> `#CRWV`
- **Taiwan Stocks**:
    - TSMC (台積電) -> `#TSM`
    - MediaTek (聯發科) -> `#MTK`
    - Acer (宏碁) -> `#宏碁`
    - Global Unichip / Alchip (創意) -> `#創意`
    - Others: Use Traditional Chinese Name (e.g., `#鴻海`, `#智邦`, `#中美晶`, `#創見`). **Do NOT use `#stock` tag for these.**
- **People**: `#Elon`, `#Jensen`, `#Trump`, `#Altman`.

### Topics & Industries
- **AI**: `#AI` (Always add if related to Artificial Intelligence, LLMs, Agents). Use specific technical tags like `#GPU`, `#CUDA` when applicable.
- **Semiconductor**: `#Semicon`, `#CoWoS`, `#ASIC`. **Do NOT use `#Chips`**.
- **Crypto**: `#Crypto`, `#BTC`, `#ETH`, `#MSTR`, `#ETF`, `#Stablecoin`, `#CBDC`, `#NFT`.
- **Finance**: **Do NOT use `#stock` or `#Finance` or `#Economy`** unnecessarily. ALWAYS attempt to find and use the specific US Ticker symbol (e.g. `#AVGO` for Broadcom, `#ADBE` for Adobe, `#VST` for Vistra), even if only the Chinese company name is mentioned. For Taiwan ETFs, use specific tickers (e.g. `#00988A`) and `#TW`. Use `#Gold`, `#Silver`, `#Fed`, `#UST` (US Treasuries), `#RMB` (Renminbi), `#options` for general economic or market news.
- **Software & Dev Tools**: Use specific tool/OS names (e.g., `#Windows`, `#VSCode`, `#Rust`, `#Coding`, `#Codex`) rather than generic company tags like `#MSFT`.
- **Automotive**: `#EV`, `#FSD`, `#Robotaxi`, `#Waymo`.
- **Robots**: `#Humanoid`, `#Robotics`.
- **Materials**: `#REE` (Rare Earth Elements), `#Lithium`, `#gas` (for natural gas).
- **Energy**: `#Solar`, `#Power`, `#Battery`, `#Nuclear`, `#oil`, `#gas`, `#LNG`, `#Hydrogen`.
- **Science**: `#Science`, `#Universe`, `#Biology`, `#Space`.
- **General Rule for Topics**: Use UpperCamelCase for topic tags (e.g., `#SmartPhone`, `#MachineLearning`) rather than all lowercase. Use `#labor` for employment/layoff news. Avoid generic tags like `#Privacy` for specific product issues.

### Regions
- **Taiwan**: `#TW` (Add if related to Taiwan companies, politics, or economy). **CRITICAL**: Always include this tag for any Taiwan-related news to ensure it is correctly categorized into the Taiwan section.
- **China**: `#China` (Add if related to Chinese companies or economy).
- **Japan**: `#Japan`
- **India**: `#India`
- **Korea**: `#Korea`
- **Europe**: `#Europe`

### Specific Models/Products
- AI Models: `#ChatGPT`, `#Claude`, `#ClaudeCode`, `#Gemini`, `#Sora`, `#Llama`, `#GPT5`, `#DeepSeek`, `#Kimi`, `#Qwen`.
- AI Concepts: `#Agent`, `#LLM`, `#OpenSource`, `#Skill`, `#VibeCoding`, `#Astral`.
- Hardware/Brands: `#iPhone`, `#Mac`, `#VisionPro`, `#OpenClaw`.
- Others: `#Starlink`, `#SpaceX`, `#SWMR` (Swarmer), `#drone`.

## Example
**Input:**
`- [台積電高雄廠導入 2nm 製程，預計 2025 量產](...)`
`- [OpenAI 發布 GPT-5，全面超越人類智商](...)`

**Output:**
`- [台積電高雄廠導入 2nm 製程，預計 2025 量產](...) #TSM #TW #semicon`
`- [OpenAI 發布 GPT-5，全面超越人類智商](...) #OpenAI #AI #GPT5`
