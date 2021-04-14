Dropzone.autoDisover = false;

  const myDropzone = new Dropzone("#my-dropzone", {
    url: "/api/file/",
    maxFiles: 5,
    maxFilesize:20,
    autoProcessQueue: false,
    parallelUploads: 5,
    autoDiscover: false,
    uploadMultiple: true,
    success: function(file, response){
//        console.log(response);
      window.location.href = response.link

      }


  })
  document.querySelector("#sendbutton").addEventListener('click',()=>myDropzone.processQueue())
