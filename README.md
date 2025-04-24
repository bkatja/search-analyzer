# Amazon Search Result Analyzer

## Description
`analyzer.py` is a flexible test automation script built using Playwright for Python. It is designed to validate user interactions on Amazon.com and allows configurable behaviors.

Being a coding assignment, it is structured with real-world test architecture principles in mind: readability, modularity, error handling, test reuse.

## Features
- **Flexible URL input**  
Accepts `amazon.com`, `www.amazon.com`, or full `https://` links; auto-normalized and validated.

- **Amazon workflow automation**  
Automates search → sort → open product → verify title. Default search is `"Nikon"`.

- **CLI configurable**  
All key behaviors are configurable via CLI arguments — including search term (`--search`), sort order (`--filter`), product index (`--index`), title validation (`--title-match`), and additional screenshots and output for debugging (`--debug`).
(Defaults reflect the original assignment: search for “Nikon”, sort by highest price, select the second result, and check for “Nikon D3X” in the title.)

- **Debug-friendly**  
Captures full-page screenshots on failure, saved in `/debug/` folder with timestamped names. Add the `--debug` argument to enable additional debug screenshots (e.g., before/after clicking elements to verify the correct index was clicked) and print raw error details to the console.

- **Structured approach**  
Modular files `analyzer.py`, `utils.py`, `amazon_helpers.py` and `elements.py` promote test reuse and clarity.

## Modular Architecture
- **analyzer.py**  
  - Main CLI script
  - Defines execution flow with minimal logic per step

- **utils.py**  
  - URL normalization and validation
  - DNS resolution
  - Screenshot handling
  - Safe navigation to URL that gracefully handles navigation errors, optionally printing raw exceptions in debug mode and saving a screenshot for troubleshooting.

- **amazon_helper.py**  
  - Dismiss popups (Dismisses Amazon-specific popups like cookie consent banners and location prompts. Similar logic can be applied for other interruptive elements during navigation.)
  - Search request
  - Sorting
  - Verifying results and title

- **elements.py**  
  - Collects all selectors
  - Makes selectors reusable, scoped and easy to maintain

## Design Goals
- Flexibility: optional filters and selectors, dynamic CLI args
- Readability: structured modules, detailed logs
- Reusability: utility functions and Amazon-specific helpers separated
- Scalability: easy to refactor for other domains or steps

## Known Limitations
This tool is not a full-scale Amazon crawler or testing suite. It has a rather targeted test automation with a focused feature set:
- Only two sort filters are supported: price-high-to-low and price-low-to-high
- Product selection is based on index (1-based) that does not account for certain elements like grouped listings
- Product title verification uses a simple substring match (not fuzzy or exact title checking)
- Cookie consent or additional pop ups are not handled unless specifically added to the Amazon helpers
- Errors related to unreachable or invalid URLs show generic messages. The system is built to allow more specific browser/network error classification if needed

This setup demonstrates the structure and logic needed to scale into more comprehensive test coverage, with attention to code clarity, modularity, and simple debugging.

## Requirements
- Python 3.8+
- Playwright

## Installation
- Clone or download this repository.
- Ensure you have Python installed (`python3 --version` to check).

It is recommended to use a virtual environment to manage dependencies for this project. To set it up:
```
python3 -m venv myenv
Mac: source myenv/bin/activate
Win: myenv\Scripts\activate
```

Check whether playwright is installed and install if needed:
```
pip show playwright
pip install -r requirements.txt
playwright install
```

## Usage
### Running the Program

> Tip: Use --help to view full documention at any time.  
> `python3 analyzer.py --help`

#### Assignment-Focused Example

To run the automation exactly as described in the assignment:
- Search for **"Nikon"**
- Sort by **highest price**
- Open the **second** product in results
- Verify the title contains **"Nikon D3X"**

Run: 
```
python3 analyzer.py amazon.com
```

This uses the default values for all arguments and matches the expected behavior.

---

#### Flexible Usage Example

Customize the behavior by specifying any of the available options:

```
python3 analyzer.py amazon.com --search canon --filter price-low-to-high --index 3 --title-match "EOS" --debug
```

---

### Arguments

- `url` (required)  
  Any valid URL (e.g., amazon.com, www.amazon.com, https://amazon.com).  
  The program automatically normalizes and verifies it.

- `--search` (optional)  
  The term to search for on Amazon.  
  Default: `"Nikon"`

- `--filter` (optional)  
  Sort results on Amazon.  
  Supported: `price-high-to-low`, `price-low-to-high`  
  Default: `"price-high-to-low"`

- `--index` (optional)  
  Specifies which product in the results to open (1-based).  
  Default: `2`

- `--title-match` (optional)  
  Text expected to appear in the opened product title (case-insensitive substring match).  
  Default: `"Nikon D3X"`

- `--debug` (optional)  
  Print raw error messages and capture additional screenshots for debugging.  
  Default: `False`
