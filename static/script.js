// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDoc,
  query,
  orderBy,
  limit,
  getDocs,
  doc,
  updateDoc,
} from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";
import {
  getStorage,
  ref as storageRef,
  uploadBytes,
  getDownloadURL,
} from "https://www.gstatic.com/firebasejs/9.6.1/firebase-storage.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "REDACTED",
  authDomain: "REDACTED",
  databaseURL: "REDACTED",
  projectId: "REDACTED",
  storageBucket: "REDACTED",
  messagingSenderId: "REDACTED",
  appId: "REDACTED",
  measurementId: "REDACTED",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);
const storage = getStorage(app);

// Home page script
if (document.getElementById("descriptionForm")) {
  let pet = null;

  document.querySelector(".cat").addEventListener("click", function () {
    document.querySelector(".dog").style.transition = "opacity 0.5s";
    document.querySelector(".dog").style.opacity = "0.5";
    document.querySelector(".cat").style.opacity = "1";
    pet = "cat";
  });

  document.querySelector(".dog").addEventListener("click", function () {
    document.querySelector(".cat").style.transition = "opacity 0.5s";
    document.querySelector(".cat").style.opacity = "0.5";
    document.querySelector(".dog").style.opacity = "1";
    pet = "dog";
  });

  document
    .getElementById("generateButton")
    .addEventListener("click", async function () {
      document.getElementById("loading").style.display = "block";
      document.getElementById("formLoading").style.display = "block"; // Show form loading icon
      const formData = new FormData(document.getElementById("descriptionForm"));
      const data = {};
      formData.forEach((value, key) => {
        if (key !== "imageUpload") {
          if (data[key]) {
            if (!Array.isArray(data[key])) {
              data[key] = [data[key]];
            }
            data[key].push(value);
          } else {
            data[key] = value;
          }
        }
      });

      data.pet = pet;
      data.timestamp = new Date(); // Add timestamp field
      const nameInput = formData.get("nameInput");
      data.name = nameInput || "No name provided"; // Include the name field

      // Generate a new random ID number
      data.id = Math.floor(Math.random() * 1000000000); // Generate a random 9-digit number

      try {
        const imageFile = formData.get("imageUpload");
        let imageUrl = "";
        if (imageFile) {
          const imageRef = storageRef(storage, `images/${imageFile.name}`);
          await uploadBytes(imageRef, imageFile);
          imageUrl = await getDownloadURL(imageRef);
          data.imageUrl = imageUrl;

          // Predict image keywords
          const imageFormData = new FormData();
          imageFormData.append("image", imageFile);
          const predictionResponse = await fetch("/predict_image_keywords", {
            method: "POST",
            body: imageFormData,
          });
          const predictionResult = await predictionResponse.json();
          if (predictionResult.description) {
            data.predictedKeywords = predictionResult.description;
          }
        }

        const docRef = await addDoc(collection(firestore, "formData"), data);
        const docSnap = await getDoc(doc(firestore, "formData", docRef.id));
        if (docSnap.exists()) {
          const fetchedData = docSnap.data();
          const list = [
            fetchedData.pet,
            fetchedData.age,
            fetchedData.size,
            fetchedData.gender,
            fetchedData.characteristics,
            fetchedData.predictedKeywords, // Include predicted keywords
          ];

          console.log(
            "Sending request to /generate_description with prompt:",
            list.join(", ")
          );

          const response = await fetch("/generate_description", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt: list.join(", ") }),
          });

          const result = await response.json();
          console.log("Received response from /generate_description:", result);

          if (result.description) {
            const capitalizeFirstLetter = (string) =>
              string.charAt(0).toUpperCase() + string.slice(1);
            data.generatedDescription = capitalizeFirstLetter(
              result.description
            ); // Save the description

            // Update Firestore document with the generated description
            await updateDoc(doc(firestore, "formData", docRef.id), {
              generatedDescription: data.generatedDescription,
            });

            console.log(
              "Generated description saved to Firestore:",
              data.generatedDescription
            );
          } else {
            console.error("No description received in the response.");
          }
        }

        const notification = document.getElementById("notification");
        notification.style.display = "block";
        setTimeout(() => {
          notification.style.display = "none";
          location.reload(); // Reload the page
        }, 3000);
      } catch (error) {
        console.error("Error generating description:", error);
        const notification = document.getElementById("notification");
        notification.textContent =
          "Failed to generate description. Please try again.";
        notification.style.display = "block";
        setTimeout(() => {
          notification.style.display = "none";
        }, 3000);
      } finally {
        document.getElementById("loading").style.display = "none";
        document.getElementById("formLoading").style.display = "none"; // Hide form loading icon
      }
    });
}

// View page script
if (document.getElementById("customerData")) {
  document.addEventListener("DOMContentLoaded", async function () {
    const container = document.getElementById("customerData");

    function capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    }

    async function fetchAndDisplayData(
      orderByField = "timestamp",
      orderDirection = "desc"
    ) {
      container.innerHTML = ""; // Clear existing data

      const formDataQuery = query(
        collection(firestore, "formData"),
        orderBy(orderByField, orderDirection),
        limit(10) // Fetch the latest 10 entries
      );

      const querySnapshot = await getDocs(formDataQuery);

      if (!querySnapshot.empty) {
        querySnapshot.forEach((doc) => {
          const entry = doc.data();

          const card = document.createElement("div");
          card.className = "customer-card";

          const img = document.createElement("img");
          img.src =
            entry.imageUrl ||
            "{{ url_for('static', filename='images/default.png') }}";
          img.alt = "Customer Image";
          card.appendChild(img);

          const info = document.createElement("div");
          info.className = "info";

          const name = document.createElement("div");
          name.className = "name";
          name.textContent = entry.name || "No name provided";
          info.appendChild(name);

          const id = document.createElement("div");
          id.className = "id";
          id.textContent = `ID: ${entry.id}`;
          info.appendChild(id);

          const gender = document.createElement("div");
          gender.className = "gender";
          gender.textContent = `Gender: ${capitalizeFirstLetter(entry.gender)}`;
          info.appendChild(gender);

          const age = document.createElement("div");
          age.className = "age";
          age.textContent = `Age: ${capitalizeFirstLetter(entry.age)}`;
          info.appendChild(age);

          const details = document.createElement("div");
          details.className = "details";
          details.textContent =
            entry.generatedDescription || "No description available.";
          details.setAttribute("data-original", details.textContent);
          info.appendChild(details);

          card.appendChild(info);
          container.appendChild(card);
        });
      } else {
        container.textContent = "No data available.";
      }
    }

    await fetchAndDisplayData();

    document
      .getElementById("filterSelect")
      .addEventListener("change", async function () {
        const filterValue = this.value;
        let orderByField = "timestamp";
        let orderDirection = "desc";

        if (filterValue === "oldest") {
          orderDirection = "asc";
        } else if (filterValue === "alphabetical") {
          orderByField = "name";
          orderDirection = "asc";
        }

        await fetchAndDisplayData(orderByField, orderDirection);
      });

    let isTranslated = false;

    document
      .getElementById("translateButton")
      .addEventListener("click", async function () {
        const cards = document.querySelectorAll(".customer-card");
        for (const card of cards) {
          const details = card.querySelector(".details");
          if (isTranslated) {
            details.textContent = details.getAttribute("data-original");
          } else {
            const description = details.getAttribute("data-original");

            const response = await fetch("/translate", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ text: description }),
            });

            const result = await response.json();
            if (result.translation) {
              details.textContent = result.translation;
            }
          }
        }
        isTranslated = !isTranslated;
      });

    document
      .getElementById("translateButton")
      .addEventListener("click", function () {
        document.getElementById("loading").style.display = "block";
        // Simulate a delay for loading
        setTimeout(function () {
          document.getElementById("loading").style.display = "none";
        }, 2000); // Adjust the delay as needed
      });

    document
      .getElementById("viewSavedButton")
      .addEventListener("click", function () {
        document
          .getElementById("savedDescriptions")
          .scrollIntoView({ behavior: "smooth" });
      });
  });
}
