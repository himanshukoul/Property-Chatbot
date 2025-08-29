import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay } from "swiper/modules";
import "swiper/css";
import "../static/PropertyCard.css";
import NoImage from "../assets/no-image.jpg";
import CurrencyRupeeIcon from "@mui/icons-material/CurrencyRupee";
const backendBaseUrl = "http://localhost:5000";
function PropertyCard({ post, showButtons = false, onDelete, onUpload }) {
  const images = post.images?.length
    ? post.images.map((img) => backendBaseUrl + img)
    : [NoImage];

  return (
    <Card
      sx={{
        width: 300,
        borderRadius: "12px",
        border: "1.5px solid #FF7300",
        overflow: "hidden",
        transition: "transform 0.2s ease",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: 4,
        },
      }}
    >
      <Swiper
        modules={[Autoplay]}
        loop={true}
        autoplay={{
          delay: 3000,
          disableOnInteraction: false,
        }}
        spaceBetween={5}
        slidesPerView={1}
      >
        {images.map((img, idx) => (
          <SwiperSlide key={idx}>
            <img src={img} alt={`slide-${idx}`} className="card-image" />
          </SwiperSlide>
        ))}
      </Swiper>

      <CardContent className="property-card-content">
        <Typography variant="body2" color="text.secondary">
          <p>{post.description}</p>
          <p>
            <strong>Location:</strong> {post.location}
          </p>
          <p>
            <strong>Price:</strong> <CurrencyRupeeIcon fontSize="small" />{" "}
            {post.price}
          </p>
          <p>
            <strong>~ {post.user_name}</strong>
          </p>
        </Typography>
      </CardContent>

      {showButtons && (
        <CardActions sx={{ justifyContent: "space-between", px: 2 }}>
          <Button
            size="small"
            variant="outlined"
            onClick={() => onUpload(post)}
          >
            Upload Images
          </Button>
          <Button
            size="small"
            variant="contained"
            color="error"
            onClick={() => onDelete(post)}
          >
            Delete
          </Button>
        </CardActions>
      )}
    </Card>
  );
}

export default PropertyCard;
