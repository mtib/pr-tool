import argparse
import os
import subprocess
from openai import OpenAI


def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description="Generate PR content using OpenAI and a template.")
    parser.add_argument("template", help="Name of the template file in the current folder", default="default.md")
    parser.add_argument("base_branch", help="Base branch to compare against", default="staging")
    args = parser.parse_args()

    # Load template (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, args.template)
    with open(template_path, "r") as f:
        template = f.read()

    # Get git log and diff
    log = run_command(f"git log {args.base_branch}..HEAD --oneline --no-merges")
    diff = run_command(f"git diff {args.base_branch}..HEAD -U10000")

    # Prepare OpenAI API
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set in environment.")
    
    org_id = os.environ.get("OPENAI_ORG_ID")
    client = OpenAI(api_key=api_key, organization=org_id)

    # Compose prompt
    prompt = f"""
Template:
{template}

Git log:
{log}

Git diff:
{diff}

Fill in the template above to generate a pull request description based on the changes and commits.
Be concise and focus on the most important changes. Use the headings provided in the template.
Do not include any additional explanations or context outside of information that is clearly relevant to the changes.
Use abbreviations and concise language where possible."""

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.5,
    )
    pr_content = response.choices[0].message.content.strip()
    print(pr_content)

if __name__ == "__main__":
    main()
