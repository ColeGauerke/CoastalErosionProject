

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
  } catch (error) {
    console.error('Error Getting News From API: ', error)
  }

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
