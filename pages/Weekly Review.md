- ```clojure
  #+BEGIN_QUERY
  {:title "Journal blocks in last 7 days with a page reference of AI"
   :query [:find (pull ?b [*])
           :in $ ?start ?today ?tag
           :where
           (between ?b ?start ?today)
           (page-ref ?b ?tag)]
   :inputs [:-7d :today "[[AI]]"]}
  #+END_QUERY
  ```
-
-
- ```clojure
  {{query (and [[AI]] (between [[Mar 5th, 2023]] [[Mar 11th, 2023]]) (not [[ChatGPT]]) (not [[AID]]))}}
  {{query (and [[AI]] (between :-7d :today) (not [[ChatGPT]]) (not [[AID]]))}}
  ```
-
-