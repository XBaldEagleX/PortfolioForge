'''
PortfolioForge - Main Orchestrator
Runs all the pieces (GitHub, LinkedIn, AI) and generates the final portfolio.
'''

import os
import json
from github_fetcher import fetch_github_data
# from linkedin_parser import parse_linkedin_pdf     # DBT
# from ai_enhancer import enhance_with_ai            # DBT

def main():
    print('Starting PortfolioForge...\n')

    # 1st Fetch the Github Data
    print('Fetching GitHub data...')
    github_data = fetch_github_data()

    #2nd Fetch LinkedIn and AI here
    # linkedin_data = parse_linkedin_pdf()
    # full_data = enhance_with_ai(github_data, linkedin_data)

    full_data = {
        "github": github_data,
        # "linkedin": linkedin_data,   # placeholder
        "generated_at": github_data["fetched_at"]
    }

    # Save the cuurent combined data
    os.makedirs('output', exist_ok=True)
    with open('output/portfolio_data.json','w') as f:
        json.dump(full_data, f, indent=2)

    print('\n Portfolio data saved to output/portfolio_data.json')
    print(f'   GitHub repos: {len(github_data['repositories'])}')
    print("\nNext step: We'll add LinkedIn parser + AI enhancement!")
    print('Run this anytime with: python main.py')

if __name__ == "__main__":
    main()

