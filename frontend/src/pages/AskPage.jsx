import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

const AskPage = () => {
  const [isRateLimited, setRateLimited] = useState(false);

  useEffect(() => {
    try {
      setRateLimited(false);
    } catch (error) {
      if (error.response?.status === 429) {
        setRateLimited(true);
      }
    }
  }, []);

  return (
    <div className="min-h-screen">
      <Navbar />
      {isRateLimited && <RateLimitedUI />}
      {!isRateLimited && (
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <input
              type="text"
              placeholder="Enter your question here..."
              className="w-full p-4 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default AskPage;
