import PropertyCard from "./PropertyCard.jsx";
import "../static/DisplayCards.css";

function DisplayCards({ properties }) {
  if (!properties.length) {
    return <div className="empty-msg">No properties to display</div>;
  }

  return (
    <div className="cards-container">
      {properties.map((post) => (
        <PropertyCard key={post._id} post={post} />
      ))}
    </div>
  );
}

export default DisplayCards;
