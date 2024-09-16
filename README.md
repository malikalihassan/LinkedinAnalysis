<!DOCTYPE html>
<html lang="en">

<body>
    <h1>LinkedIn Profile Scraper and GPT Analysis Tool</h1>
    <p>This Python script allows users to scrape LinkedIn profiles and analyze the data using GPT-3.5. The tool fetches profile information such as the user's name, headline, services offered, and the about section, then analyzes this data using OpenAI's GPT API. The final results are written to a CSV file.</p>

<h2>Features</h2>
    <ul>
        <li><strong>Scrape LinkedIn Profiles</strong>: Extracts basic profile information like name, headline, services, and the about section from LinkedIn profiles.</li>
        <li><strong>Analyze Profile Data</strong>: Utilizes OpenAI GPT to analyze the completeness of the profile, suggest SEO improvements, and provide content recommendations.</li>
        <li><strong>Save Results</strong>: Exports the scraped and analyzed data to a CSV file for easy viewing and further use.</li>
    </ul>

 <h2>Prerequisites</h2>
    <p>Before using this tool, ensure that you have:</p>
    <ul>
        <li>Python 3.x installed</li>
        <li>A LinkedIn account with valid credentials.</li>
        <li>An OpenAI API key for GPT analysis.</li>
        <li>Chrome WebDriver installed and set up on your system.</li>
    </ul>

<h2>How to Install and Run</h2>
    <h3>Clone the repository:</h3>
    <pre><code>git clone https://github.com/malikalihassan/LinkedinAnalysis.git
cd LinkedinAnalysis
</code></pre

<h3>Create a virtual environment:</h3>
    <pre><code>python -m venv env
source env/bin/activate  # For Windows, use `env\Scripts\activate`


<p>The script will scrape the profiles listed, analyze the data using the GPT API, and save the results in <code>results.csv</code>.</p>

    

<h2>Key Functions</h2>
    <ul>
        <li><strong>linkedin_login()</strong>: Logs into LinkedIn using credentials provided in the script. Saves the session cookies for future use.</li>
        <li><strong>load_cookies()</strong>: Loads the saved cookies to avoid multiple logins and use existing sessions.</li>
        <li><strong>scrape_profile(profile_url)</strong>: Scrapes LinkedIn profiles to gather essential information such as name, headline, services, and the about section.</li>
        <li><strong>analyze_analyze_data(data)</strong>: Sends scraped profile data to OpenAI's GPT API for analysis, which provides:
            <ul>
                <li><strong>Profile Completeness</strong>: Checks if the profile is fully optimized.</li>
                <li><strong>SEO Suggestions</strong>: Provides tips for improving search visibility on LinkedIn.</li>
                <li><strong>Content Suggestions</strong>: Recommends content the user can post on LinkedIn to engage their audience.</li>
            </ul>
        </li>
        <li><strong>write_results_to_csv(final_results)</strong>: Saves the results of the scraping and analysis to a CSV file.</li>
    </ul>

<h2>Summary</h2>
    <p>This tool automates the process of scraping LinkedIn profiles and analyzing them with the power of GPT-3.5. It is useful for individuals or companies looking to audit multiple LinkedIn profiles and gather insights on how to improve them.</p>
</body>
</html>
