const express = require("express");
const redis = require("redis");
const axios = require("axios");
const cors = require("cors");

const app = express();
const port = 3000;

const redisClient = redis.createClient({
  url: `redis://${process.env.REDIS_HOST || "localhost"}:6379`,
});

redisClient.connect().catch(console.error);

app.use(express.json());
app.use(cors());

const generateSensorData = () => ({
  temperature: (Math.random() * 100 + 50).toFixed(2),
  pressure: (Math.random() * 1000 + 500).toFixed(2),
  timestamp: new Date().toISOString(),
});

app.get("/sensor-data", async (req, res) => {
  try {
    const cachedData = await redisClient.get("sensor_data");

    if (cachedData) {
      return res.json(JSON.parse(cachedData));
    }

    const sensorData = generateSensorData();

    await redisClient.set("sensor_data", JSON.stringify(sensorData), {
      EX: 30,
    });

    res.json(sensorData);
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/alert", async (req, res) => {
  try {
    const alertData = {
      ...req.body,
      timestamp: new Date().toISOString(),
    };

    const pythonApiUrl = process.env.PYTHON_API_URL || "http://localhost:5000";
    await axios.post(`${pythonApiUrl}/event`, alertData);

    res.json({ message: "Alert sent successfully" });
  } catch (error) {
    console.error("Error sending alert:", error);
    res.status(500).json({ error: "Failed to send alert" });
  }
});

app.listen(port, () => {
  console.log(`Sensors API listening at http://localhost:${port}`);
});
