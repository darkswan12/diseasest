import { useState } from 'react';

function App() {
  const [image, setImage] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [output, setOutput] = useState('');

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
   if (!image) {
     alert("Please add a photo first!");
     return;
   }
 
   const formData = new FormData();
   formData.append('image', image);
 
   try {
     const response = await fetch('https://diseasest-production.up.railway.app/predict/disease', {
       method: 'POST',
       body: formData,
     });
     const result = await response.json();
     if (result.error) {
       setOutput(`Error: ${result.error}`);
     } else {
       const data = result.data;
       setOutput(`
         <strong>Plant Disease:</strong> ${data.hasil}<br>
         <strong>Confidence Score:</strong> ${data.skorKepercayaan.toFixed(2)}%<br>
         <strong>Description:</strong> ${data.Description}<br>
         <strong>Treatment:</strong> ${data.Treatment}
       `);
     }
   } catch (error) {
     setOutput(`Error: ${error.message}`);
   }
 };
 

 return (
   <div className="w-full min-h-screen flex items-center justify-center bg-lime-300 text-green-700">
     <div className="w-full max-w-3xl p-6 bg-white rounded-lg shadow-lg">
       <h1 className="text-center font-extrabold text-5xl mb-8">Plant Disease Detector</h1>
       <div className="text-center">
         <label className="block text-2xl mb-4" htmlFor="imageInput">Upload Plant Image</label>
         <input 
           type="file" 
           id="imageInput" 
           className="block w-full text-lg mb-4 p-2 border border-green-500 rounded-lg" 
           onChange={handleImageChange} 
         />
         {imagePreviewUrl && (
           <div className="mb-4">
             <img id="imagePreview" className="w-full h-auto rounded-lg border border-green-500" src={imagePreviewUrl} alt="Image Preview" />
           </div>
         )}
         <button onClick={handleSubmit} className="px-6 py-2 bg-green-700 text-white text-xl font-bold rounded-lg shadow-md hover:bg-green-800 transition duration-300">Submit Photo</button>
         <div className="mt-8">
           <h2 className="text-2xl font-bold mb-4">Model Output:</h2>
           <div id="outputText" className="p-4 bg-gray-100 rounded-lg border border-green-500" dangerouslySetInnerHTML={{ __html: output }}></div>
         </div>
       </div>
     </div>
   </div>
 ); 
}

export default App;
