// This file replaces static/JS/autocomplete.js
document.addEventListener("DOMContentLoaded", function () {
  // Initialize the Algolia client
  const searchClient = algoliasearch(
    "R0P8LNKXOK", // Your Algolia Application ID
    "39fe5d71882d2469dc10a89f8823e6a0" // Your Algolia Search-Only API Key
  );

  // Initialize the autocomplete
  window.autocomplete({
    container: "#autocomplete",
    placeholder: "חיפוש מוספים...",
    openOnFocus: true,
    detachedMediaQuery: "none",
    debug: true,
    getSources({ query }) {
      return [
        {
          sourceId: "haaretz-archive",
          getItems() {
            return getAlgoliaResults({
              searchClient,
              queries: [
                {
                  indexName: "haaretz_archive", // Make sure this matches your actual index name
                  query,
                  params: {
                    hitsPerPage: 10,
                  },
                },
              ],
            });
          },
          templates: {
            header() {
              return "תוצאות חיפוש";
            },
            item({ item, html }) {
              // Display the search result with title and optional date
              return html`
                <a href="${item.url || "#"}" class="aa-ItemLink">
                  <div class="aa-ItemContent">
                    <div class="aa-ItemTitle">
                      ${item.title ||
                      item.name ||
                      item._highlightResult?.title?.value ||
                      "כותרת לא זמינה"}
                    </div>
                    ${item.date
                      ? html`<div class="aa-ItemDate">${item.date}</div>`
                      : ""}
                  </div>
                </a>
              `;
            },
            noResults() {
              return "לא נמצאו תוצאות";
            },
          },
        },
      ];
    },
  });
});
