import { useState } from "react";

import {
  uploadInvoice,
  getJobStatus,
  getInvoice,
} from "./api";
import Login from "./Login";
import "./App.css";
function App() {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const [invoice, setInvoice] = useState(null);
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState("No active job");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError("");
    setStatus("No active job");
    setJobId(null);
    setInvoice(null);
  };

  const checkJobStatus = async (id) => {
  try {
    const result = await getJobStatus(id, token);

    setStatus(result.status);

    if (result.status === "completed") {
      if (result.invoice_id) {
        const invoiceResult = await getInvoice(
          result.invoice_id,
          token
        );

        console.log(
          "Processed invoice:",
          invoiceResult
        );

        setInvoice(invoiceResult);
      } else {
        setError(
          "Invoice processing completed, but no invoice was created."
        );
      }

      return;
    }

    if (result.status === "failed") {
      setError(
        result.error_message || "Invoice processing failed."
      );
      return;
    }

    setTimeout(
      () => checkJobStatus(id),
      2000
    );

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

    if (!token) {
      setError("Please login first.");
      return;
    }

    try {
      setError("");
      setInvoice(null);
      setStatus("Uploading...");

      const result = await uploadInvoice(
        file,
        token
      );

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

      {/* Navbar */}
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

        {/* Welcome */}
        <div className="welcome">

          <h1>
            Invoice Processing Dashboard
          </h1>

          <p>
            Upload an invoice and extract structured
            information automatically.
          </p>

        </div>


        {/* Upload */}
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


        {/* Processing Status */}
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


        {/* Invoice Results */}
        {invoice && (
          <section className="results-card">

            <div className="results-header">

              <div>
                <h2>
                  Invoice Results
                </h2>

                <p>
                  Extracted invoice information
                </p>
              </div>

              <span className="completed-badge">
                Completed
              </span>

            </div>


            {/* Invoice Information */}
            <div className="invoice-details">

              <div className="detail-item">
                <span>Invoice Number</span>
                <strong>
                  {invoice.invoice_number || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>Invoice Date</span>
                <strong>
                  {invoice.invoice_date || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>Vendor</span>
                <strong>
                  {invoice.vendor || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>Customer</span>
                <strong>
                  {invoice.customer || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>PO Number</span>
                <strong>
                  {invoice.po_number || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>GSTIN</span>
                <strong>
                  {invoice.gstin || "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>Subtotal</span>
                <strong>
                  {invoice.currency || ""}
                  {invoice.subtotal ?? "N/A"}
                </strong>
              </div>

              <div className="detail-item">
                <span>Tax</span>
                <strong>
                  {invoice.currency || ""}
                  {invoice.tax ?? "N/A"}
                </strong>
              </div>

              <div className="detail-item total-item">
                <span>Total</span>
                <strong>
                  {invoice.currency || ""}
                  {invoice.total ?? "N/A"}
                </strong>
              </div>

            </div>


            {/* Line Items */}
            <div className="line-items">

              <h3>
                Line Items
              </h3>

              {invoice.line_items &&
              invoice.line_items.length > 0 ? (

                <div className="table-wrapper">

                  <table>

                    <thead>
                      <tr>
                        <th>Description</th>
                        <th>HSN Code</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Amount</th>
                      </tr>
                    </thead>

                    <tbody>

                      {invoice.line_items.map(
                        (item, index) => (

                          <tr key={index}>

                            <td>
                              {item.description || "N/A"}
                            </td>

                            <td>
                              {item.hsn_code || "N/A"}
                            </td>

                            <td>
                              {item.quantity ?? "N/A"}
                            </td>

                            <td>
                              {item.unit_price ?? "N/A"}
                            </td>

                            <td>
                              {item.amount ?? "N/A"}
                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              ) : (

                <p className="no-items">
                  No line items found.
                </p>

              )}

            </div>

          </section>
        )}

      </main>

    </div>
  );
}

export default App;