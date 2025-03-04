import { autocomplete, getAlgoliaResults } from "@algolia/autocomplete-js";
import { createRedirectUrlPlugin } from "@algolia/autocomplete-plugin-redirect-url";
import algoliasearch from "algoliasearch/lite";

import "@algolia/autocomplete-theme-classic";

let envConfig = {};
let searchClient;

fetch("/env-config")
  .then((response) => response.json())
  .then((data) => {
    envConfig = data;
    initAlgolia();
  });

function initAlgolia() {
  const searchClient = algoliasearch(
    envConfig.ALGOLIA_APP_ID,
    envConfig.ALGOLIA_SEARCH_API_KEY
  );
}

autocomplete({
  container: "#autocomplete",
  placeholder: "חיפוש כתבות...",
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
