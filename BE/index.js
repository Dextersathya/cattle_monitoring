const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());
app.use(cors());

// Dummy data to store posts
let COUNT = 0;
let Array = [];

app.post("/api/post", (req, res) => {
  if (!req.body.hasOwnProperty("count")) {
    return res.status(400).json({ message: 'Missing required field "count"' });
  }
  if (typeof req.body.count !== "number") {
    return res.status(400).json({ message: 'Field "count" must be a number' });
  }
  const { count } = req.body;
  console.log(count, "response");
  COUNT = count;
  res.status(201).json({
    message: "Post created successfully",
    count: COUNT,
  });
});

app.post("/api/array", (req, res) => {
  const { string } = req.body;

  // Check if the input is a non-empty string
  if (typeof string === "string" && string.trim() !== "") {
    Array.push(string);
    res.status(201).json({ message: "String added to the array." });
  } else {
    res
      .status(400)
      .json({ error: "Invalid input. Please provide a non-empty string." });
  }
});

app.get("/api/array", (req, res) => {
  // Check if the array is empty
  if (Array.length === 0) {
    res.status(200).json({ string: "" });
  } else {
    // Get the first element from the array
    const firstString = Array.shift();
    res.status(200).json({ string: firstString });
  }
});

// Route to get all posts
app.get("/api/get", (req, res) => {
  console.log("res");
  // Check if the array is empty
  if (Array.length === 0) {
    res.status(200).json({ string: "", COUNT });
  } else {
    // Get the first element from the array
    const firstString = Array.shift();
    res.status(200).json({ string: firstString, COUNT });
  }
});
app.get("/", (req, res) => {
  res.json("Success! Node.js server is running on Raspberry Pi.");
});

// Start the server
app.listen(PORT, () => {
  console.log(`http://localhost:${PORT}`);
});
