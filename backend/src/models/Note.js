import mongoose from "mongoose";

//Create Schema
const noteSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
    embedding: {
      type: String, // Wrong type to exclude from return result
      required: false,
    },
  },
  { timestamps: true } // createAt, updateAt
);

//Create model based of schema
const Note = mongoose.model("Note", noteSchema);

export default Note;
