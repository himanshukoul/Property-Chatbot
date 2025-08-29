import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import PropertyCard from "./PropertyCard.jsx";
import "../static/MyPostsDialog.css";

function MyPostsDialog({ open, onClose, posts }) {
  const token = localStorage.getItem("token");

  const handleUpload = async (post) => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.multiple = true;
    input.click();

    input.onchange = async () => {
      const files = input.files;
      if (!files.length) return;

      const formData = new FormData();
      for (let file of files) {
        formData.append("images", file);
      }

      const res = await fetch(
        `http://localhost:5000/api/upload_images/${post._id}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();
      alert(data.message || "Images uploaded.");
    };
  };

  const handleDelete = async (post) => {
    const confirm = window.confirm(
      "Are you sure you want to delete this post?"
    );
    if (!confirm) return;

    const res = await fetch(
      `http://localhost:5000/api/delete_listing/${post._id}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await res.json();
    alert(data.message || "Deleted.");
    window.location.reload();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>My Property Posts</DialogTitle>
      <DialogContent>
        <div className="posts-container">
          {posts.map((post) => (
            <PropertyCard
              key={post._id}
              post={post}
              showButtons
              onDelete={handleDelete}
              onUpload={handleUpload}
            />
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}

export default MyPostsDialog;
