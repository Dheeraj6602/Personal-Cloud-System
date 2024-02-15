document.addEventListener('DOMContentLoaded', function () {
    // Assuming you have a function to retrieve file information from AWS S3
    const files = getFilesFromS3();

    const fileList = document.getElementById('file-list');

    // Iterate through the files and populate the table
    files.forEach((file, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${file.name}</td>
            <td>${file.modified}</td>
            <td>${file.type}</td>
            <td>
                <button onclick="renameFile(${file.id})" class="rename-btn">Rename</button>
                <button onclick="deleteFile(${file.id})" class="delete-btn">Delete</button>
            </td>
        `;

        fileList.appendChild(row);
    });
});

function getFilesFromS3() {
    // Simulated function to retrieve file information from AWS S3
    return [
        { id: 1, name: 'File1.txt', modified: '2023-10-31', type: 'Text' },
        { id: 2, name: 'File2.jpg', modified: '2023-10-30', type: 'Image' },
        // Add more file information here
    ];
}

function renameFile(fileId) {
    // Implement renaming logic here
    console.log(`Renaming file with ID ${fileId}`);
}

function deleteFile(fileId) {
    // Implement deletion logic here
    console.log(`Deleting file with ID ${fileId}`);
}
