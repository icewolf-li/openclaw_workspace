#!/usr/bin/env node

const fetch = require('node-fetch');

async function search(query, options = {}) {
  const { count = 5, includeContent = false } = options;
  
  // Get API key from environment or config
  const apiKey = process.env.BRAVE_API_KEY || 'YOUR_API_KEY';
  
  if (apiKey === 'YOUR_API_KEY') {
    console.error('Error: Please set BRAVE_API_KEY environment variable');
    process.exit(1);
  }
  
  try {
    const url = `https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=${count}`;
    
    const response = await fetch(url, {
      headers: {
        'X-Subscription-Token': apiKey,
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.web && data.web.results) {
      for (let i = 0; i < Math.min(data.web.results.length, count); i++) {
        const result = data.web.results[i];
        console.log(`--- Result ${i + 1} ---`);
        console.log(`Title: ${result.title || 'No title'}`);
        console.log(`Link: ${result.url || 'No URL'}`);
        console.log(`Snippet: ${result.description || 'No description'}`);
        
        if (includeContent && result.url) {
          console.log('Content: (Content extraction not implemented in this basic version)');
        }
        console.log('');
      }
    } else {
      console.log('No results found');
    }
  } catch (error) {
    console.error('Search error:', error.message);
    process.exit(1);
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node search.js "query" [-n count] [--content]');
  process.exit(1);
}

let query = '';
let count = 5;
let includeContent = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '-n' && i + 1 < args.length) {
    count = parseInt(args[i + 1], 10);
    i++; // Skip next argument
  } else if (args[i] === '--content') {
    includeContent = true;
  } else if (!query) {
    query = args[i];
  }
}

search(query, { count, includeContent });