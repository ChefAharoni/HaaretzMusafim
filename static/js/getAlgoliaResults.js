import algoliasearch from "algoliasearch/lite";
import { autocomplete, getAlgoliaResults } from "@algolia/autocomplete-js";
import "@algolia/autocomplete-theme-classic";
// const searchClient = algoliasearch(
//   "R0P8LNKXOK",
//   "39fe5d71882d2469dc10a89f8823e6a0"
// );

let envConfig = {};
let searchClient;

fetch("/env-config")
  .then((response) => response.json())
  .then((data) => {
    envConfig = data;
    initAlgolia();
  });

function initAlgolia() {
  searchClient = algoliasearch(
    envConfig.ALGOLIA_APP_ID,
    envConfig.ALGOLIA_SEARCH_API_KEY
  );
}

autocomplete({
  container: "#autocomplete",
  placeholder: "חיפוש כתבה...",
  getSources({ query }) {
    if (!query) {
      return [];
    }

    return [
      {
        sourceId: "articles",
        getItems() {
          return getAlgoliaResults({
            searchClient,
            queries: [
              {
                indexName: "YOUR_INDEX_NAME",
                query,
                hitsPerPage: 5, // Limit the number of results
              },
            ],
          });
        },
        templates: {
          item({ item, components }) {
            return components.Highlight({ hit: item, attribute: "title" });
          },
          noResults() {
            return "לא נמצאו תוצאות";
          },
        },
        getItemUrl({ item }) {
          return item.url; // Ensure your items have a URL attribute
        },
      },
    ];
  },
});
