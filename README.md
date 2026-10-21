# BAN 6403 Labs

Lab notebooks, data and Lab Companions for BAN 6403 Text Analytics for Business (Fall 2027).

## Start here (Module 0)

Module 0 in Canvas walks you through the setup. You used the same tools in BAN 6003, so for most students this is a check and a refresher. The **Technology and Accessibility** page in Module 0 has the exact steps for Windows and macOS. You use **GitHub Desktop** for Git; you do not need Git commands.

### 1. Check the tools

Check that **Anaconda**, **GitHub Desktop** and **VS Code** (with the Python and Jupyter extensions) still work, or install them.

### 2. Accept the invitation to your repository

The instructor creates your private repository for you. You do not create it yourself. Only you and the instructor can see it; classmates cannot.

1. Give your GitHub username in the Module 0 Canvas item **Your GitHub username**.
2. Within a few days, GitHub emails you an invitation to your own repository, `[course-org]/ban6403-<your-username>`. Accept it. You can also accept it at `https://github.com/[course-org]/ban6403-<your-username>/invitations` while signed in. The invitation expires after 7 days; if it does, tell the instructor.
3. Open your repository on GitHub. It is already private and already holds every course file.

Your repository's address is your **repository link**, for example `https://github.com/[course-org]/ban6403-jdoe`. In Module 0, paste it into the Canvas item **Your repository link**. This confirms that you can open it. You give it once; every lab and project step is graded from this repository.

### 3. Clone it and set up the environment

1. Clone your repository with GitHub Desktop. On your repository's GitHub page, click the green **Code** button, then **Open with GitHub Desktop**. Or use **File > Clone Repository** in GitHub Desktop. Keep it in a normal folder such as `Documents/GitHub`, not in OneDrive or iCloud.
2. In Anaconda Prompt (Windows) or Terminal (macOS), go to the repository folder and create the course environment:

   ```text
   conda env create -f environment.yml
   ```

3. In VS Code, choose **File > Open Folder** and open this repository folder. Open `notebooks/M00_Technology_Readiness.ipynb` and choose the **ban6403** kernel.
4. Open `companions/M00_lab_companion.html` in your browser. Run the notebook until the last cell prints `READY`.
5. In GitHub Desktop, commit your work with the summary `Module 0 readiness check`, then click **Push origin**.

The course environment uses Python 3.13, pandas 3.0 and scikit-learn 1.8 or newer. If you created `ban6403` for an earlier course, update it with `conda env update -n ban6403 -f environment.yml --prune`.

**Online students: GitHub Codespaces.** Instead of the local setup in parts 1 and 3, you may run your repository in your browser with GitHub Codespaces. You still accept the invitation first (part 2). Then click **Code > Codespaces > Create codespace on main** on your repository's page. See `.devcontainer/README.md`. Codespaces use your own free monthly hours, not the instructor's. Codespaces is not reachable on the UTSA campus network, so Flex students use the Anaconda setup in class.

## Each week

Your repository already contains every notebook, Lab Companion and data file for the course. The only exception is the Module 13 held-out files. In Week 13 you download them as `m13_heldout_pack.zip` from the Module 13 page in Canvas. Unzip it and copy the files into the matching folders of your repository; the start of the Lab 13 notebook lists where each file goes.

1. Open this repository folder in VS Code and open the week's notebook in `notebooks/`.
2. Choose the **ban6403** kernel (in Codespaces, the only Python 3.13 entry).
3. Open the week's Lab Companion from `companions/` in your browser and follow it beside the notebook.
4. Run the notebook from the top and save it, so the outputs are saved in the file.
5. Commit and push your work in GitHub Desktop before the deadline.

Your repository is your own copy, so it does not receive course updates through **Fetch origin** or **Pull**. If a course file changes during the term, the instructor posts the new file in Canvas.

## How you submit

You upload nothing to Canvas for labs, milestones or the final project. The instructor grades your repository **as it is at each deadline**: the work you have pushed by then.

- **Lab notebooks:** run the whole notebook, save it with its outputs, then commit and push before the lab deadline. The saved outputs are what is graded. The lab item in Canvas holds the due date and your grade.
- **Project milestones and the final project:** commit and push your `project/` folder before each deadline.
- **What counts is when you push,** not the date on a commit. A commit that is only on your computer cannot be graded. After a push, check on GitHub.com that your work is there.

**After the course.** Your repository stays in the course organization. To keep a copy, create an empty repository in your own account before the end of the term. In GitHub Desktop, open **Repository > Repository settings**, paste the new address as the remote, and click **Push origin**. If your project used Yelp data, copy only your own files instead: Yelp's terms require you to delete the data after the course.

## Which data does each lab use?

| Data | Where | Used in |
|---|---|---|
| 24 made-up example messages | `data/raw/customer_feedback_m01.csv` | Part 1 (guided core) of Labs 1–8, 10 and 11; Lab 9 Part 1 uses saved predictions for them |
| CFPB consumer complaints (10,000) | `data/course/cfpb_complaints.csv` | Practice of Labs 1–3, 6 and 8–11; Lab 13 (held-out complaints, Week 13) and Lab 14 Part 1. Lab 12 uses them only to count complaint themes. |
| Women's clothing reviews (22,634) | `data/course/clothing_reviews.csv` | Practice of Labs 4, 5 and 7 |
| Made-up help center and support questions | `data/rag/` | Lab 12 (both parts) and the Lab 13 Practice (a prompt-injection case) |
| Made-up support inbox (154 messages) | `data/support/` | Extra practice beside Lab 12; no lab requires it |

The project uses its own data: see the project overview in Canvas and `project_starters/`.


## Folders

| Folder | Contents |
|---|---|
| `notebooks/` | One lab notebook per module, starting with the Module 0 readiness check |
| `companions/` | Step-by-step Lab Companion pages; open them in any browser |
| `data/raw/` | The 24 made-up example messages used in most guided parts, plus small example files for single labs |
| `data/course/` | Two course datasets, each with a fixed train/valid/test split: 10,000 CFPB consumer complaints and 22,634 clothing reviews (lab data). Read `README.md` and `clothing_reviews_README.md`. |
| `data/partitions/` | The fixed development/protected split of the example messages (Module 2) |
| `data/processed/` | Prepared versions of the course data, such as complaint chunks for retrieval |
| `data/embeddings/` | Embeddings computed once by the instructor, each with a manifest that records its fingerprint |
| `data/llm_outputs/` | Saved LLM outputs used in graded evaluation, with the prompts that produced them |
| `data/retrieval/`, `data/reviewed/`, `data/rag/`, `data/predictions/` | Queries, relevance judgments, reviewed samples and other files for single labs |
| `data/heldout/` | Held-out complaints for the Module 13 evaluation. Added in Week 13 from `m13_heldout_pack.zip` in Canvas |
| `data/support/` | A small made-up customer-support inbox that goes with the Module 12 help center (practice data) |
| `project_starters/` | Starter notebooks for the five project data options, and the scripts `yelp_sample.py` and `amazon_sample.py` that draw a fixed sample from data you download |
| `docs/` | Data guides and policies used in the labs |
| `project/` | Your individual project, once you start it (see the project overview in Canvas). Raw downloads go to `project/data/private/`, which Git ignores; the sample you draw goes to `project/data/sample/` and is committed. |
| `outputs/` | Files your notebooks save. The notebooks create it when you run them. |
| `environment.yml` | The package list for the `ban6403` environment |
| `.devcontainer/` | The GitHub Codespaces setup (optional, Online students) |

## Rules

- Do not change files in `data/`. Notebooks read them and write results to `outputs/`. The readiness notebook checks the fingerprints of the main data files. In Week 13, commit the new Module 13 files in `data/`.
- Never put passwords or API keys in a notebook or commit them. Keep any key in a local `.env` file, which Git ignores.
- Do not add personal or confidential text to this repository. Keep it private: do not change its visibility.
- You never need to pay for an AI service. Later labs provide the LLM outputs used for grading.

## Help

Post setup and lab questions in the course Q&A discussion in Canvas. Include the notebook, the step number and the last line of the error message.
