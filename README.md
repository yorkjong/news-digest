# news-digest
 York's news digest.

- **Website:** [york-news-digest.netlify.app](https://york-news-digest.netlify.app) (or [news-digest.vercel.app](https://news-digest.vercel.app))
- **Bug reports:** [github.com/YorkJong/news-digest/issues](https://github.com/YorkJong/news-digest/issues)
- **Tools:**
  - [news_clip.ipynb](https://colab.research.google.com/github/YorkJong/news-digest/blob/main/notebooks/news_clip.ipynb) -- clip latest news.
  - [news_query.ipynb](https://colab.research.google.com/github/YorkJong/news-digest/blob/main/notebooks/news_query.ipynb) -- query news across multiple days.
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

### Getting Started on Colab

1. Click [news_clip.ipynb](https://colab.research.google.com/github/YorkJong/news-digest/blob/main/notebooks/news_clip.ipynb) to open it in colab.
2. Sign in your Google account if required.
3. Follow the steps in the demonstration video below.
   1. Install clip module
      - Click the ► button to start install
      - We can see `[ ]` symbol at the begin of a cell. It will be changed to ► button while the mouse cursor over it.
   2. Fill parameters of a form.
   3. Manually click ► button (means "start run") to get news with selected categories.

<video src="https://user-images.githubusercontent.com/11453572/227774236-4a16750e-afb3-411e-80cc-a9b079113a78.mov" controls="controls" style="max-width: 730px;">
</video>

### Dive into on the news-digest Website

1. Click [news-digest.vercel.app](https://news-digest.vercel.app) to open the news-digest website.
2. We can see a feature-rich UI as follows.

![news-digest](https://user-images.githubusercontent.com/11453572/226693810-07bed2e9-d4d4-4ffd-b29a-dc5c7f2851f5.jpg)

### Publish & Depoly

- I used [pengx17/logseq-publish](https://github.com/pengx17/logseq-publish) to publish the Logseq pages and to depoly it to the GitHub Pages (i.e., [yorkjong.github.io/news-digest](https://yorkjong.github.io/news-digest)).
- I used [Netlify](https://netlify.app) to save backup of the site as [york-news-digest.netlify.app](https://york-news-digest.netlify.app)

#### Demo of applying Line Notify

<video src="https://user-images.githubusercontent.com/11453572/227774419-fe4c7e47-b10a-4c9d-9efa-267997ebb641.mov" controls="controls" style="max-width: 730px;">
</video>

![Line](https://user-images.githubusercontent.com/11453572/227774718-11c5cd26-b896-4c77-935c-7af1ff04ed96.jpg)
