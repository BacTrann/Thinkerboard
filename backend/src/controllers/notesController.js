import Note from "../models/Note.js";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

// Get all user notes
export async function getAllNotes(_, res) {
  try {
    // Call mongo model to find all notes in database, sorted by latest created time
    const notes = await Note.find().sort({ createdAt: -1 });

    // Return found note as json
    res.status(200).json(notes);
  } catch (error) {
    console.error("Error in getAllNotes controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}

export async function getNoteById(req, res) {
  try {
    const note = await Note.findById(req.params.id);
    if (!note) return res.status(404).json({ message: "Note not found" });

    res.status(200).json(note);
  } catch (error) {
    console.error("Error in getNoteById controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}

export async function createNote(req, res) {
  try {
    const { title, content } = req.body;
    const newNote = new Note({ title, content });

    const savedNote = await newNote.save();
    // TODO: Find out why even with await, embedding not updated
    axios.put(`${process.env.LLM_URL}/embed/${savedNote._id.toString()}`)
    res.status(201).json(savedNote);
  } catch (error) {
    console.error("Error in createNote controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}

export async function updateNote(req, res) {
  try {
    const { title, content } = req.body;
    const updatedNote = await Note.findByIdAndUpdate(
      req.params.id,
      { title, content },
      { new: true }
    );
    if (!updatedNote)
      return res.status(404).json({ message: "Note not found" });
    await axios.put(`${process.env.LLM_URL}/embed/${req.params.id}`);
    res.status(200).json({ message: "Note updated successfully" });
  } catch (error) {
    console.error("Error in updateNote controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}

export async function deleteNote(req, res) {
  try {
    const deleteNote = await Note.findByIdAndDelete(req.params.id);
    if (!deleteNote)
      return res.status(404).json({ message: "Failed to delete note" });

    res.status(200).json({ message: "Note deleted successfully" });
  } catch (error) {
    console.error("Error in deleteNote controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}

export async function askNote(req, res) {
  try {
    const { query } = req.body;
    const response = await axios.post(process.env.LLM_URL + "/query", {
      query: query,
    });
    return res.status(200).json({ message: response.data.message });
  } catch (error) {
    console.error("Error in askNote controller", error);
    res.status(500).json({ message: "Internal server error" });
  }
}
