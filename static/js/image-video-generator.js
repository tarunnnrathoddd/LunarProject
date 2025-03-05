document.addEventListener("DOMContentLoaded", () => {
  const videoForm = document.getElementById("videoGenerationForm");
  const videoResult = document.getElementById("videoResult");

  if (videoForm) {
    videoForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(videoForm);

      try {
        videoResult.innerHTML =
          '<p class="text-center">Generating video...</p>';

        const response = await fetch("/generate-video", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.text();
          throw new Error(errorData || "Video generation failed");
        }

        const videoBlob = await response.blob();
        const videoUrl = URL.createObjectURL(videoBlob);

        videoResult.innerHTML = `
          <video controls class="w-full rounded-lg shadow-lg">
            <source src="${videoUrl}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        `;
      } catch (error) {
        videoResult.innerHTML = `
          <p class="text-red-500 text-center">Error: ${error.message}</p>
        `;
      }
    });
  }

  // Remove the moon analysis form code since it's on a different page
});
