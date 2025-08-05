import express from "express";
import {
  createNote,
  deleteNote,
  getAllNotes,
  getNoteById,
  updateNote,
  askNote,
} from "../controllers/notesController.js";

const router = express.Router();
// Interacting with user notes API
router.get("/", getAllNotes);
router.get("/:id", getNoteById);
router.post("/", createNote);
router.post("/ask", askNote);
router.put("/:id", updateNote);
router.delete("/:id", deleteNote);

export default router;
