---
title: RSS Feeds 訂閱 news-digest 新聞
tags: RSS, 訂閱
---

- 如果你還沒用過 RSS Feeds 訂閱過任何東西，以下是個可行的步驟
  - 安裝 [RSS Feed Reader Chrome 插件](https://chrome.google.com/webstore/detail/rss-feed-reader/pnjaodmkngahhkoihejjehlcdlnohgmp)
  - 點擊後面 RSS Feeds 列表中你要訂閱的 .rss 連結，就可以看到你要訂閱的新聞了
- **RSS feeds:**
  - [Vehicle.rss](https://news-digest.vercel.app/Vehicle.rss)
  - [TechTitans.rss](https://news-digest.vercel.app/TechTitans.rss)
  - [Finance.rss](https://news-digest.vercel.app/Finance.rss)
  - [news.rss](https://news-digest.vercel.app/news.rss) (merge above 3 RSS feeds)
  - [Crypto.rss](https://news-digest.vercel.app/Crypto.rss)
  - [Taiwan.rss](https://news-digest.vercel.app/Taiwan.rss)
  - [Science.rss](https://news-digest.vercel.app/Science.rss)
  - [IT.rss](https://news-digest.vercel.app/IT.rss)
  - `https://news-digest.vercel.app/{heading}.h.rss`
     - `{heading}` can be any substring of a heading.
       - Heading "Tesla & SpaceX; Vehicle" can be reduced to "Tesla", "SpaceX", or "Vehicle".
       - Heading "Tech Titans" can be reduced to "Tech" or "Titans".
  - `https://news-digest.vercel.app/{tag}.t.rss`
    - `{tag}` can be any hashtag (`#` removed), e.g., `TSLA`, `NVDA`, `AI`.

