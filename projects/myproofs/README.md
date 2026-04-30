# myproofs

## GitHub configuration

To set up your new GitHub repository, follow these steps:

* Under your repository name, click **Settings**.
* In the **Actions** section of the sidebar, click "General".
* Check the box **Allow GitHub Actions to create and approve pull requests**.
* Click the **Pages** section of the settings sidebar.
* In the **Source** dropdown menu, select "GitHub Actions".

After following the steps above, you can remove this section from the README file.
## Current Test Case — Lemma 4

So far, the system is working well for proving simpler mathematical 
statements, and I'm currently testing it on a version of Lemma 4. 
It's still in progress — continuing to monitor how it performs on 
a more complex result like this.

Current test in `projects/myproofs/Myproofs/Basic.lean`:

```lean
import Mathlib
open BigOperators

lemma lemma4_path_sum (n : ℕ) :
  ∑ p ∈ Finset.range n, p * (n - p) = (n^3 - n) / 6 := by
  sorry
```

Here, `sorry` is a placeholder for an unfinished proof which the 
system then attempts to complete. Running with:

```bash
bash example_run.sh projects/myproofs/Myproofs
```