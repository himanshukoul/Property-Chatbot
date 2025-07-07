import { useState } from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import WavingHandIcon from "@mui/icons-material/WavingHand";

function ResumeMemoryDialog({
  open,
  onClose,
  memories,
  onSelectMemory,
  onStartFresh,
}) {
  const [selected, setSelected] = useState(null);
  console.log("ResumeMemoryDialog memories:", memories);

  const handleResume = (memory) => {
    setSelected(memory.memory_id);
    onSelectMemory(memory);
  };

  const handleStartFresh = () => {
    setSelected("fresh");
    onStartFresh();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        Welcome back <WavingHandIcon />
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" gutterBottom>
          Would you like to continue from a previous session or start fresh?{" "}
          <i className="fa-solid fa-brain"></i>
        </Typography>

        {memories.length > 0 ? (
          memories.map((memory) => (
            <Card
              key={memory.memory_id}
              variant="outlined"
              style={{ marginTop: 10, backgroundColor: "#f9f9f9" }}
            >
              <CardContent>
                <Typography variant="body2" style={{ marginBottom: 8 }}>
                  {memory.text.length > 180
                    ? memory.text.slice(0, 180) + "..."
                    : memory.text}
                </Typography>
                <Button
                  variant="contained"
                  size="small"
                  color="primary"
                  disabled={selected !== null}
                  onClick={() => handleResume(memory)}
                >
                  Resume
                </Button>
              </CardContent>
            </Card>
          ))
        ) : (
          <Typography variant="body2" color="textSecondary">
            No previous sessions found. Start a new session!{" "}
            <i className="fa-solid fa-face-sad-cry"></i>
          </Typography>
        )}
      </DialogContent>

      <DialogActions>
        <Button
          variant="text"
          onClick={handleStartFresh}
          disabled={selected !== null}
        >
          Start Fresh
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ResumeMemoryDialog;
