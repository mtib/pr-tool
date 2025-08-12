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
    status = run_command(f"git status")
    log = run_command(f"git log {args.base_branch}..HEAD --oneline --no-merges")
    diff = run_command(f"git diff {args.base_branch} -U100")

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

Git status:
{status}

Git log:
{log}

Git diff:
{diff}

Fill in the template above to generate a pull request description based on the changes and commits.
Be concise and focus on the most important changes. Use the headings provided in the template.
Do not include any additional explanations or context outside of information that is clearly relevant to the changes.
Use abbreviations and concise language where possible.

If you are on a branch `<type>/<ticket>/<description>`, the description should be a good indicator of the changes made in that branch.
Also, if the branch contains a ticket, include it in the description as well as the link to "https://montaapp.atlassian.net/browse/<ticket>" this is very important.

If the template contains comments, do not include them in the final output, but consider them for the text you are adding in the sections.
If there are checkboxes in the template, ensure they are checked if the corresponding changes are present.
If a section is not relevant, just write "No" or "N/A".
Do not include the git log or diff or branch name in the final output, but use them to inform your writing.
Include mermaid diagrams in code blocks with the `mermaid` tag if there are structured changes or hierarchies.

Your entire response should be a complete github pull request description that fits into the template provided.
"""

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-5",
        reasoning_effort='high',
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1024,
        temperature=0.5,
    )
    pr_content = response.choices[0].message.content.strip()
    print(pr_content)

if __name__ == "__main__":
    main()
