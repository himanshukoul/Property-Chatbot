import { useState } from "react";
import "../static/SearchBar.css";

function SearchBar({ handleInitialSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (query.trim()) {
      handleInitialSearch(query.trim());
      setQuery("");
    }
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search for properties (e.g. 2 BHK in Delhi)"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBar;
