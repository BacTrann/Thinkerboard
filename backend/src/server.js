import express from "express";
import dotenv from "dotenv";
import cors from "cors";

import notesRoutes from "./routes/notesRoutes.js";
import rateLimiter from "./middleware/rateLimiter.js";
import { connectDB } from "./config/db.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// middleware
// IMPORTANT: cors middleware must be before rateLimiter middleware
app.use(
  cors({
    origin: "http://localhost:5173",
  })
);
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
