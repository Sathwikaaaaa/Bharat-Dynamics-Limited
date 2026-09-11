import { useState } from "react";
import { uploadInvoice, getJobStatus } from "./api";
import Login from "./Login";
import "./App.css";

function App() {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState("No active job");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError("");
    setStatus("No active job");
    setJobId(null);
  };

  const checkJobStatus = async (id) => {
    try {
      const result = await getJobStatus(id, token);

      setStatus(result.status);

      if (
        result.status !== "completed" &&
        result.status !== "failed"
      ) {
        setTimeout(() => {
          checkJobStatus(id);
        }, 2000);
      }
    } catch (error) {
      setError(error.message);
      setStatus("Status check failed");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select an invoice first.");
      return;
    }

    try {
      setError("");
      setStatus("Uploading...");

      const result = await uploadInvoice(file, token);

      setJobId(result.job_id);
      setStatus("queued");

      checkJobStatus(result.job_id);
    } catch (error) {
      setError(error.message);
      setStatus("Upload failed");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
  };

  if (!token) {
    return (
      <Login
        onLogin={(newToken) => {
          setToken(newToken);
        }}
      />
    );
  }

  return (
    <div className="app">

      <header className="navbar">

        <div className="logo">
          Invoice OCR
        </div>

        <div className="nav-user">

          <span>
            Dashboard
          </span>

          <button onClick={handleLogout}>
            Logout
          </button>

        </div>

      </header>


      <main className="dashboard">

        <div className="welcome">

          <h1>
            Invoice Processing Dashboard
          </h1>

          <p>
            Upload an invoice and extract structured
            information automatically.
          </p>

        </div>


        <section className="upload-card">

          <h2>
            Upload Invoice
          </h2>

          <div className="upload-area">

            <div className="upload-icon">
              📄
            </div>

            <h3>
              Select an invoice
            </h3>

            <p>
              Supported formats: PDF, JPG, JPEG, PNG
            </p>

            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={handleFileChange}
            />

            {file && (
              <div className="selected-file">
                Selected:{" "}
                <strong>
                  {file.name}
                </strong>
              </div>
            )}

            <button
              className="upload-button"
              disabled={!file}
              onClick={handleUpload}
            >
              Upload Invoice
            </button>

          </div>

        </section>


        <section className="status-card">

          <h2>
            Processing Status
          </h2>

          <div className="status-row">

            <span>
              Latest Job
            </span>

            <span className="status queued">
              {status}
            </span>

          </div>

          {jobId && (
            <p>
              Job ID:{" "}
              <strong>
                {jobId}
              </strong>
            </p>
          )}

          {error && (
            <p className="error">
              {error}
            </p>
          )}

        </section>

      </main>

    </div>
  );
}

export default App;