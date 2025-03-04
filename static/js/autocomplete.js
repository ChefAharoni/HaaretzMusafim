import { autocomplete, getAlgoliaResults } from "@algolia/autocomplete-js";
import { createRedirectUrlPlugin } from "@algolia/autocomplete-plugin-redirect-url";
import algoliasearch from "algoliasearch/lite";

import "@algolia/autocomplete-theme-classic";

// const searchClient = algoliasearch(
//   "R0P8LNKXOK",
//   "39fe5d71882d2469dc10a89f8823e6a0"
// );

const searchClient = algoliasearch(
  process.env.ALGOLIA_APP_ID,
  process.env.ALGOLIA_SEARCH_API_KEY
);

autocomplete({
  container: "#autocomplete",
  placeholder: "חיפוש מוספים...",
  openOnFocus: true,
  insights: true,
  plugins: [createRedirectUrlPlugin()],
  getSources({ query }) {
    return [
      {
        sourceId: "demo-source",
        templates: {
          item(params) {
            const { item, html } = params;
            return html`<a class="aa-ItemLink">${item.name}</a>`;
          },
        },
        getItemInputValue({ item }) {
          return item.name;
        },
        getItems() {
          return getAlgoliaResults({
            searchClient,
            queries: [
              {
                indexName: "HaaretzArchive Index",
                query,
                params: {
                  // ruleContexts: ["enable-redirect-url"], // note: only needed for this demo data
                  hitsPerPage: 10,
                },
              },
            ],
          });
        },
      },
    ];
  },
});
