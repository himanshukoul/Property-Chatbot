import "../static/Navbar.css";
import Button from "@mui/material/Button";
function Navbar({
  isLoggedIn,
  userData,
  setShowLogin,
  setShowSignup,
  handleLogout,
  handleMyPosts,
}) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <i className="fa-solid fa-house"></i> Proppy
      </div>
      <div className="navbar-links">
        {isLoggedIn ? (
          <>
            <span className="user-email">Welcome, {userData?.email}</span>
            <Button
              onClick={handleMyPosts}
              variant="outlined"
              color="secondary"
            >
              My Posts
            </Button>
            <Button onClick={handleLogout} variant="outlined" color="secondary">
              Logout
            </Button>
          </>
        ) : (
          <>
            <Button
              onClick={() => setShowLogin(true)}
              variant="outlined"
              color="secondary"
            >
              Login
            </Button>
            <Button
              onClick={() => setShowSignup(true)}
              variant="outlined"
              color="secondary"
            >
              Signup
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
