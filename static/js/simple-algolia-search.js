// Simple Algolia search implementation
document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const searchContainer = document.getElementById("search-container");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");
  const searchButton = document.getElementById("search-button");

  // Algolia client
  // const client = algoliasearch(
  //   "R0P8LNKXOK",
  //   "39fe5d71882d2469dc10a89f8823e6a0"
  // );

  let envConfig = {};

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

  const index = searchClient.initIndex("HaaretzArchive Index");

  // Variables
  let resultsVisible = false;
  let searchTimeout;

  // Functions
  function performSearch() {
    const query = searchInput.value.trim();

    if (query.length === 0) {
      hideResults();
      return;
    }

    index
      .search(query, {
        hitsPerPage: 10,
      })
      .then(({ hits }) => {
        // Clear previous results
        searchResults.innerHTML = "";

        if (hits.length === 0) {
          searchResults.innerHTML =
            '<div class="no-results">לא נמצאו תוצאות</div>';
        } else {
          hits.forEach((hit) => {
            const resultItem = document.createElement("div");
            resultItem.className = "search-result-item";

            const link = document.createElement("a");
            link.href = hit.url || "#";
            link.className = "search-result-link";

            const title = document.createElement("div");
            title.className = "search-result-title";
            title.textContent = hit.title || hit.name || "כותרת לא זמינה";

            link.appendChild(title);

            if (hit.date) {
              const date = document.createElement("div");
              date.className = "search-result-date";
              date.textContent = hit.date;
              link.appendChild(date);
            }

            resultItem.appendChild(link);
            searchResults.appendChild(resultItem);
          });
        }

        showResults();
      })
      .catch((err) => {
        console.error("Search error:", err);
        searchResults.innerHTML =
          '<div class="search-error">שגיאה בחיפוש</div>';
        showResults();
      });
  }

  function showResults() {
    searchResults.style.display = "block";
    resultsVisible = true;
  }

  function hideResults() {
    searchResults.style.display = "none";
    resultsVisible = false;
  }

  // Event listeners
  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(performSearch, 300);
  });

  searchInput.addEventListener("focus", function () {
    if (searchInput.value.trim().length > 0) {
      showResults();
    }
  });

  searchButton.addEventListener("click", function (e) {
    e.preventDefault();
    performSearch();
  });

  // Close results when clicking outside
  document.addEventListener("click", function (e) {
    if (resultsVisible && !searchContainer.contains(e.target)) {
      hideResults();
    }
  });

  // Prevent form submission
  const form = searchContainer.closest("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      performSearch();
    });
  }
});
