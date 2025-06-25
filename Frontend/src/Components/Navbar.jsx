import "../static/Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <i className="fa-solid fa-house"></i> PropBot
      </div>
      <div className="navbar-links">
        <a href="#">Home</a>
        <a href="#">Contact</a>
      </div>
    </nav>
  );
}

export default Navbar;
