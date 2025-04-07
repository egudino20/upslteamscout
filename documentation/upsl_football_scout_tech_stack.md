
# ✅ Updated Tech Stack Overview for UPSLTeamScout

---

## 🚀 Deployment & Hosting
- **Render**
  - Hosts the Flask backend application.
  - Handles deployment pipelines (auto-deploy from GitHub).
  - Ideal for full-stack web apps and REST APIs.

---

## 🧠 Backend
- **Python + Flask**
  - Primary backend framework.
  - Handles API routing, authentication, and business logic.
  - Supports asynchronous processing for tasks like video ingestion and data processing.

---

## 🧰 Storage & Data
- **Google Cloud Storage (GCS)**
  - Stores match videos and processed tracking/event data.
  - Access controlled via a Google Cloud service account.
  - Organized as:  
    `gs://upsl_match_videos/{Division}/{Conference}/{Season}/{Club}/{Match}`  
    `gs://upsl_match_stats/{Division}/{Conference}/{Season}/{Club}/{Match}`

- **Supabase**
  - Provides Postgres database, Auth, and Realtime features.
  - Stores user metadata, preferences, and references to GCS resources.
  - Exposes APIs for interaction with client/front-end.

---

## 📊 Data Processing
- **YOLOv8 + ByteTrack + Custom Event Detection**
  - Used for object detection, tracking, and basic event recognition.
  - Hosted as a background service or batch job triggered post-upload.
  - Outputs are stored in JSON and linked to Supabase records.

---

## 📁 File Management
- **Google Cloud Service Account**
  - Credentials (`upsl-video-api-c5071e2d09bf.json`) allow secure access to GCS via Flask.
  - All video and stat file uploads/reads are authorized using this service account.

---

## 🧠 Future ML/AI Stack (optional but compatible)
- **Roboflow or On-Prem YOLO Inference**
  - For annotation, dataset management, and model training.
- **UMAP + KMeans**
  - For team color differentiation (unsupervised clustering of SigLIP embeddings).
- **Pandas + Numpy + Scikit-learn**
  - For processing tracking data and generating contextualized stats.

---

## 🌐 Frontend (Optional)
- Currently decoupled (you may use React, Svelte, or static HTML)
- Auth and API calls will route to Flask endpoints hosted on Render.
