document.getElementById("searchBtn").addEventListener("click", async () => {
  const query = document.getElementById("searchInput").value;
  console.log("Querying for:", query);

  try {
    const results = await fetch("http://localhost:5000/search?q=" + query);
    const data = await results.json();
    console.log("Results received:", data);

    const list = document.getElementById("results");
    list.innerHTML = "";

    if (data.length === 0) {
      list.innerHTML = "<li>No results found</li>";
      return;
    }

    data.forEach(({ url, snippet }) => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${url}" target="_blank">${snippet}</a>`;
      list.appendChild(li);
    });

  } catch (error) {
    console.error("Search failed:", error);
    alert("Something went wrong! See console.");
  }
});
