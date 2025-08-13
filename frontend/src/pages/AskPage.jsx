import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import api from "../lib/axios";

const AskPage = () => {
  const [isRateLimited, setRateLimited] = useState(false);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    try {
      setRateLimited(false);
    } catch (error) {
      if (error.response?.status === 429) {
        setRateLimited(true);
      }
    }
  }, []);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const res = await api.post("/notes/ask", {
        query: query,
      });
      setResponse(res.data.message);
      setQuery("");
    } catch (e) {
      console.log(`Error in handling query submit ${e}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      {isRateLimited && <RateLimitedUI />}
      {!isRateLimited && (
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <form onSubmit={handleQuerySubmit}>
              <input
                type="text"
                placeholder="Enter your question here..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full p-4 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-white-500"
              />
            </form>
          </div>
        </div>
      )}
      {loading && (
        <div className="flex justify-center items-center mt-4">
          <div className="w-8 h-8 border-4 border-gray-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}
      {response && (
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto">
            <p className="w-full min-h-64 mt-4 p-4 shadow-sm whitespace-pre-wrap">
              {response}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AskPage;
