import algoliasearch from "algoliasearch/lite";
import instantsearch from "instantsearch.js";
import { searchBox, hits } from "instantsearch.js/es/widgets";

const searchClient = algoliasearch(
  "R0P8LNKXOK",
  "39fe5d71882d2469dc10a89f8823e6a0"
);

const search = instantsearch({
  indexName: "demo_ecommerce",
  searchClient,
});

search.addWidgets([
  searchBox({
    container: "#searchbox",
  }),

  hits({
    container: "#hits",
  }),
]);

search.start();
