import express from "express";
import notesRoutes from "./routes/notesRoutes.js";
import rateLimiter from "./middleware/rateLimiter.js";
import { connectDB } from "./config/db.js";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// middleware
app.use(express.json());
app.use(rateLimiter);

app.use("/api/notes", notesRoutes);

// Connect to database then listen to port 5001
connectDB()
  .then(
    app.listen(PORT, () => {
      console.log("Server started on PORT: ", PORT);
    })
  )
  .catch((e) => console.log("Failed to connect to MongoDB", e));
