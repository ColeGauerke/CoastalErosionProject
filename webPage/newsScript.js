

// Function for searching for da news page
async function searchCoastalNews() {
  const keywords = document.getElementById('NewsSearchInput').value;
  const state = document.getElementById('NewsStateDD').value;
  const city = document.getElementById('NewsCityDD').value;
  const date = document.getElementById('NewsDatePicker').value;
  let area = `${city} ${state}`;
  console.log("Full Keywords: ", keywords);
  console.log("Date: ", date);

  const request = {
    "everything": true,
    "keyword": keywords,
    "area": area,
    "searchDate": date
  };

  try {
    //http://localhost:5073/api/Coasty/News/GetEverything
    const response = await fetch('http://localhost:5073/api/Coasty/News/GetEverything' , {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    const data = await response.json()
    console.log("News Data: ", data);
    console.log("Articles: ", data.articles )
    displayResults(data.articles);
  } catch (error) {
    console.error('Error Getting News From API: ', error)
  }

}

function displayResults(articles) {
  const container = document.getElementById('NewsResultsContainer');
  container.innerHTML = ''; // Clear artiles on function start
  if (!articles || articles.length == 0) { //No articles found
    container.innerHTML = `<div id="emptyState">
                            <div id="emptyStateIcon"></div>
                            <h3>No Articles Found</h3>
                          </div>"`; return;
  }

  const results = document.createElement('div');
  results.id = 'resultsCount';
  results.textContent = `${articles.length} articles matching your search`;
  container.append(results);

  const mainContainer = document.createElement('div');
  mainContainer.id = 'newsContainerCards';

  articles.forEach(article => {
    const card = document.createElement('div');
    card.id='newsCard';
    const publishDate = new Date(article.publishDate).toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'});
    card.innerHTML = `
      <div class="news-card-title">
        <a href="${article.url}" target="_blank">
          ${article.title}
        </a>
      </div>
      <div class="news-card-description">
        ${article.description}
      </div>
      <div class="news-card-meta">
        <div class="news-card-meta-item">
          <span class="news-card-meta-label">Source:</span>
          <span>${article.name}</span>
        </div>
        <div class="news-card-meta-item">
          <span class="news-card-meta-label">Published:</span>
          <span>${publishDate}</span>
        </div>
        <div class="news-card-meta-item">
          <span class="news-card-meta-label">Author:</span>
          <span>${article.author}</span>
        </div>
      </div>
      <a href="${article.url}" target="_blank" class="news-card-button">Read Full Article</a>
    `;
    mainContainer.appendChild(card);
  });
  container.appendChild(mainContainer);
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('NewsSearchButton').addEventListener('click', function() {
    searchCoastalNews();
  });
  document.getElementById('NewsSearchInput').addEventListener('keypress', function(e) {
    if (e.key == "Enter") {
      searchCoastalNews();
    }
  });
});
