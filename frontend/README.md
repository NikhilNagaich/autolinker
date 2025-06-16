# My React Blog Extractor

This project is a React application designed to extract blog content from a given URL. It consists of three main pages: an input page for entering the blog URL, a progress page to show the extraction status, and a results page to display the extracted blogs and links with download options.

## Project Structure

```
my-react-blog-extractor
├── src
│   ├── components
│   │   ├── InputPage.tsx
│   │   ├── ProgressPage.tsx
│   │   ├── ResultsPage.tsx
│   │   └── common
│   │       └── DownloadButton.tsx
│   ├── App.tsx
│   ├── index.tsx
│   ├── types
│   │   └── index.ts
│   └── utils
│       └── extractor.ts
├── public
│   └── index.html
├── package.json
├── tsconfig.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (version 5.6 or higher)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd my-react-blog-extractor
   ```
3. Install the dependencies:
   ```
   npm install
   ```

### Running the Application

To start the development server, run:
```
npm start
```
This will launch the application in your default web browser at `http://localhost:3000`.

### Usage

1. Navigate to the Input Page to enter a blog URL.
2. Click "Start" to begin the extraction process.
3. Monitor the Progress Page for the status of the extraction.
4. Once completed, view the Results Page to see the extracted blogs and links, with options to download the results.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.