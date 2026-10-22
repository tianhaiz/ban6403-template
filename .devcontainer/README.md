# GitHub Codespaces (Online students)

GitHub Codespaces runs your copy of the course repository in a web browser. You do not install Anaconda, GitHub Desktop or VS Code on your computer. Online students may use it instead of the Anaconda setup.

Codespaces is not reachable on the UTSA campus network. Flex students therefore use Anaconda, GitHub Desktop and VS Code on their own laptop, as described on the Technology and Accessibility page.

## What this folder does

`devcontainer.json` tells Codespaces how to build your workspace. It uses Python 3.13 and installs the same packages as `environment.yml`: numpy, pandas 3.0, scikit-learn, scipy, matplotlib, ipykernel and nbconvert. It also adds the VS Code Python and Jupyter extensions, and it hides the system Python from the kernel list, so only one Python 3.13 entry is shown. Do not change this file.

## Create your codespace (once)

1. Sign in to GitHub and open **your own repository**, `https://github.com/[course-org]/ban6403-<your-username>`. The instructor created it for you. If you cannot open it, accept the email invitation first (part 2 of the main `README.md`).
2. Click the green **Code** button, open the **Codespaces** tab and click **Create codespace on main**.
3. Wait while the codespace is built. The first time takes a few minutes, because the packages are installed.
4. VS Code opens in your browser with the repository folder already open.

## Run a notebook

1. Open the notebook in `notebooks/`, for example `M00_Technology_Readiness.ipynb`.
2. Click **Select Kernel** at the top right. Choose **Python Environments**, then choose the only Python 3.13 entry (`/usr/local/bin/python`).
3. Run the notebook from the top. In the Module 0 readiness notebook, the kernel check shows `PASS | notebook kernel: GitHub Codespaces`.

## Save your work

A codespace is a copy of your repository on a GitHub computer. Your changes reach your repository on GitHub only when you commit and push them.

1. Save the notebook (**Ctrl+S**, or **Cmd+S** on macOS).
2. Open **Source Control** in the left bar (the branch icon).
3. Type a short message, such as `Lab 1 complete`, and click **Commit**. If VS Code asks to stage your changes, choose **Yes**.
4. Click **Sync Changes** to push the commit. Your pushed work is what the instructor grades at each deadline; there is nothing to upload to Canvas.

## Stop the codespace when you are done

Your codespace is billed to **your own GitHub account**, not to the course or the instructor. A free personal account includes 120 core-hours of compute and 15 GB-month of storage each month (GitHub's figures in October 2026; see <https://docs.github.com/en/billing/concepts/product-billing/github-codespaces>). The default codespace has 2 cores, so it uses 2 core-hours per hour: about 60 hours of work a month. A running codespace uses your free hours, even when you do nothing. A GitHub Pro account (free for students through GitHub Education) includes 180 core-hours and 20 GB-month. If you use up the free amount and have no payment method on file, GitHub blocks your codespaces until the next month. If you have a payment method on file, check your budget settings, so you are not charged.

- When you finish a session, stop it: open <https://github.com/codespaces>, click **...** next to your codespace and choose **Stop codespace**.
- A stopped codespace keeps your files. Open it again from the same page.
- Do not delete the codespace before you have committed and pushed your work.
- GitHub stops an idle codespace after about 30 minutes and deletes long-unused stopped codespaces. Commit and push at the end of every session.

## If something goes wrong

- **The packages are missing** (`ModuleNotFoundError`): open the command palette (**Ctrl+Shift+P**) and run **Codespaces: Rebuild Container**.
- **The kernel list does not show Python 3.13**: wait until the setup has finished, then run **Developer: Reload Window**.
- **You cannot reach Codespaces**: use the Anaconda setup on the Technology and Accessibility page.

Post other problems in the course Q&A discussion in Canvas. Include the notebook, the step number and the last line of the error message.
