import "../static/DisplayCards.css";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { useTheme } from "@mui/material/styles";

function DisplayCards({ properties }) {
  const theme = useTheme();
  if (!properties.length) {
    return <div className="empty-msg">No properties to display</div>;
  }

  return (
    <div className="cards-container">
      {/*{properties.map((prop, index) => (
        <div className="property-card" key={index}>
          <img
            src={prop.image || "Frontendsrcassets\no-image.svg"}
            alt="property"
          />
          <h3>{prop.title}</h3>
          <p>{prop.description}</p>
          <p>
            <strong>Location:</strong> {prop.location}
          </p>
          <p>
            <strong>Price:</strong> Rs. {prop.price}
          </p>
        </div>
      ))}*/}
      {properties.map((prop) => (
        <Card
          sx={{
            width: 300,
            boxShadow: 3,
            border: `2px solid ${theme.palette.secondary.main}`,
            transition: "transform 0.3s, box-shadow 0.3s",
            "&:hover": {
              transform: "scale(1.03)",
              boxShadow: 6,
              backgroundColor: "#157c63",
              color: "white",
            },
          }}
          key={prop._id}
        >
          <CardMedia
            sx={{ height: 140 }}
            image={prop.image || "/assets/no-image.jpg"}
            title={prop.title}
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="span">
              {prop.title}
            </Typography>
            <Typography
              variant="body2"
              sx={{ color: "text.secondary" }}
              component="div"
            >
              <p>{prop.description} </p>
              <p>
                <strong>Location:</strong> {prop.location}
              </p>
              <p>
                <strong>Price:</strong> Rs. {prop.price}
              </p>
            </Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default DisplayCards;
