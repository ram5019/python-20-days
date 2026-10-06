# Track 5: Cloud/DevOps, boto3, Azure SDK, OCI SDK

**Examples:** `examples/t5_boto3.py`, `examples/t5_boto3_mock.py`, `examples/t5_azure.py`, `examples/t5_oci.py`
**Install:**
```bash
pip install boto3 "moto[s3,ec2,sts]"                      # AWS (+ a fake AWS for practice)
pip install azure-identity azure-mgmt-resource azure-mgmt-resource-subscriptions azure-mgmt-compute   # Azure
pip install oci                                           # Oracle Cloud
```
**Prerequisites:** Day 16 (errors), Day 20 (layered code), Day 26 (APIs), Day 28 (CLI)

---

## 1. The big idea

Every cloud is, underneath, **a huge web API** (Day 26). An **SDK** (software development kit) wraps that API in friendly Python functions, so instead of building HTTP requests and signing them with secret keys, you write:

```python
s3.list_buckets()
```

```
your Python ──SDK──► signs the request, handles retries ──HTTPS──► cloud API
                                                                      │
your Python ◄── Python objects/dicts ◄── JSON response ◄──────────────┘
```

| Cloud | SDK | Python package |
|-------|-----|----------------|
| AWS | boto3 | `boto3` |
| Microsoft Azure | Azure SDK | `azure-identity` + one package per service (`azure-mgmt-compute`, ...) |
| Oracle Cloud (OCI) | OCI SDK | `oci` |

## 2. Why does this exist?

Clicking through a web console does not scale and cannot be repeated exactly. With code you can:

- **Inventory**: "list every VM across all my accounts, with its owner tag".
- **Audit**: "which storage buckets are public?", "which instances are untagged?".
- **Automate**: nightly snapshots, scheduled start/stop, cleaning up forgotten resources.
- **Integrate**: feed cloud data into Pandas (Track 1), expose it in a Flask/FastAPI dashboard (Track 2), run it from a CLI tool (Day 28).

## 3. Simple way to understand

A **hotel with a front desk**.

- The **cloud** is the hotel; **resources** (VMs, buckets, networks) are the rooms and services.
- The **SDK** is the **front-desk phone**: you say what you want in simple words, and the desk does the paperwork.
- Your **credentials** are your **room key card**. It identifies you and decides which doors open (permissions).
- A **region** is which hotel branch you are calling. Many calls fail simply because you rang the wrong branch.
- **Read-only** access is "may look at the rooms but not change anything". Always start there.

## 4. Five ideas that are the same in every cloud

| Idea | AWS | Azure | OCI |
|------|-----|-------|-----|
| **Identity** (who am I?) | `sts.get_caller_identity()` | `DefaultAzureCredential` + list subscriptions | `identity.get_user(config["user"])` |
| **Where credentials come from** | `~/.aws/credentials`, env vars, SSO, instance role | `az login`, env vars, managed identity | `~/.oci/config` (path to private key) |
| **Top-level container** | account | subscription | tenancy |
| **Folders for resources** | tags / accounts | resource groups | compartments |
| **Pagination** | `get_paginator(...)` | the SDK returns an iterator that pages automatically | `oci.pagination.list_call_get_all_results` |

**The golden rule: credentials never go in your code.** SDKs find them themselves from standard locations, so your script contains **no secrets** and is safe to commit and share.

---

## Part 1: boto3 / AWS (`t5_boto3.py`)

### Run it safely first with the fake AWS
```bash
python3 learning-path/advanced/examples/t5_boto3_mock.py
```
`moto` pretends to be AWS **inside your computer**. No account, no cost, no risk. It sets dummy credentials so nothing can reach the real AWS.

### Code walkthrough (`t5_boto3.py`)

| Block | Code | What it does |
|-------|------|--------------|
| 1 | `sts.get_caller_identity()` | the "who am I?" call: returns the account id and ARN. **Run this first** to confirm you are in the account you think you are |
| 2 | `s3.list_buckets()["Buckets"]` | the response is a dict (Day 13); a list comprehension pulls out the names |
| 3 | `get_paginator("list_objects_v2")`, `page.get("Contents", [])` | APIs return **limited pages** (S3: 1,000 objects). The paginator fetches the next page automatically. `.get(..., [])` handles an empty bucket where the key is missing |
| 4 | `Filters=[{"Name": ..., "Values": [...]}]`; nested loops over Reservations → Instances; `{t["Key"]: t["Value"] for t in tags}` | **filter on the server** (less data); EC2 nests instances inside "reservations"; AWS tags are a list of key/value dicts, so a **dict comprehension** (Day 21) makes them easy to look up |
| 5 | `summarise_by_state` | **pure logic**, no AWS calls: the Day 20 layering again |
| 6 | `main()` with `argparse` and `try/except` | CLI options (Day 28); catches **`NoCredentialsError`**, **`ClientError`** (AWS said no: read `e.response["Error"]["Code"]`) and **`BotoCoreError`** (network/config) |

### Code walkthrough (`t5_boto3_mock.py`)

| Block | What it does |
|-------|--------------|
| 1 | sets **fake** credentials *before* importing boto3, so even a bug cannot touch real AWS |
| 2 | `with mock_aws():`: inside this block every boto3 call is answered by the pretend AWS; builds 2 buckets, 25 objects and 3 instances (one stopped), then calls **the same functions** as the real script |
| 3 | asks for 10 of 25 objects: the paginator and the `limit` logic work |
| 4 | filters by `running`, and summarises: `{'running': 2, 'stopped': 1}` |
| 5 | triggers a `NoSuchBucket` error so you can see what `ClientError` looks like |

**How the blocks connect:** both files share the same functions, which is why the mock gives you real confidence about the real script. This is the main idea of **testing cloud code without a cloud**.

**Tested:** `t5_boto3_mock.py` ran end to end with the output above. `t5_boto3.py` was run only down its **no-credentials path** (it printed the friendly message); I did not run it against a real AWS account.

---

## Part 2: Azure SDK (`t5_azure.py`)

### The key difference: many small packages
Azure has one package per service. Today you need: `azure-identity` (login), `azure-mgmt-resource-subscriptions` (subscriptions), `azure-mgmt-resource` (resource groups) and `azure-mgmt-compute` (VMs). **Names and import paths have changed over time**, so old tutorials may fail with `ImportError`. The imports in this file are the ones that worked when I tested.

### Code walkthrough

| Block | Code | What it does |
|-------|------|--------------|
| 1 | `DefaultAzureCredential()` | **one** credential object, reused by every client. It tries several login methods in order (environment variables, managed identity, `az login`, ...) and uses the first that works |
| 2 | `SubscriptionClient(credential).subscriptions.list()` | the SDK returns an **iterator** that pages for you |
| 3 | `ResourceManagementClient(credential, subscription_id)` | other clients need the **subscription id** too |
| 4 | `ComputeManagementClient(...).virtual_machines.list_all()` | builds a list of dicts (Day 13 shape); `vm.tags or {}` handles missing tags |
| 5 | `resource_group_from_id(...)` | Azure IDs are **paths**; splitting on `/` extracts the resource group. A pure function, so it is testable |
| 6 | `group_by_location` | `setdefault(key, [])` is a tidy form of Day 13's grouping pattern |
| main | catches `ClientAuthenticationError` and `HttpResponseError` | friendly message instead of a crash |

**Tested:** the two helper functions returned correct results, and the **not-logged-in** path printed its message. I did **not** run any real Azure call, because I have no Azure login here.

---

## Part 3: OCI SDK (`t5_oci.py`)

### The key difference: a config file
OCI reads `~/.oci/config`, which holds your user, tenancy, region, key fingerprint and the **path** to your private key file. Create it with the OCI CLI (`oci setup config`). The Python file never contains the key.

### Code walkthrough

| Block | Code | What it does |
|-------|------|--------------|
| 1 | `oci.config.from_file(...)`, `validate_config(config)` | loads the config into a dict and **checks it is complete** before any call |
| 2 | `IdentityClient(config).get_user(config["user"]).data` | "who am I?"; every OCI response has the useful content in **`.data`** |
| 3 | `list_region_subscriptions(config["tenancy"])` | which regions your tenancy can use |
| 4 | `oci.pagination.list_call_get_all_results(func, arg)` | passes the **function itself** (Day 22) plus its arguments; the helper keeps calling it until all pages are collected |
| 5 | `ComputeClient(config).list_instances(compartment_id, lifecycle_state=...)` | instances live in a **compartment**; the optional filter is passed only when given (`**kwargs`, Day 23) |
| 6 | `count_by_state` | pure logic |
| main | catches `ConfigFileNotFound`, `ProfileNotFound`, `InvalidConfig`, `ServiceError` | `ServiceError` carries `.status`, `.code`, `.message` |

**Tested:** the helper returned the right counts, and all three **config-failure paths** (no file, incomplete file, unknown profile) printed correct messages. I also confirmed the field names I use (`display_name`, `lifecycle_state`, `shape`, `availability_domain`, ...) exist on the SDK's models. I did **not** run a real OCI call.

---

## 5. How the three examples are alike

```
1. Build credentials / config   (from standard places, never from code)
2. Create a client for ONE service      ← boto3.client("ec2") / ComputeClient(...)
3. Call a list/describe method          ← returns pages
4. Page through the results             ← paginator / iterator / list_call_get_all_results
5. Convert to plain dicts/lists         ← then use Days 13, 21, Pandas, JSON, CSV
6. Wrap in try/except for auth errors   ← each SDK has its own exception types
```

Learn one SDK well and the others feel familiar: only the names change.

## 6. Safety checklist (read before touching a real account)

1. **Start read-only.** Use credentials limited to `list` / `describe` / `get`.
2. **Know where you are.** Print the identity (account, subscription, tenancy) before doing anything.
3. **Never hard-code secrets.** No keys, tokens or passwords in code, notebooks, screenshots or git history. If a key leaks, **revoke it immediately**.
4. **Use a sandbox or test account** for anything that creates or deletes.
5. **Least privilege.** Give a script only the permissions it needs.
6. **Dry-run and confirm** before destructive operations: print what *would* be deleted, then ask.
7. **Beware cost.** Creating resources can bill you. Tag them and clean up.
8. **Respect rate limits.** Cloud APIs throttle; SDKs retry, but do not hammer them in loops.
9. For anything on a **customer or production** environment, follow your organisation's change and access rules.

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Wrong region (AWS/OCI) | "resource not found", empty lists | set the region explicitly and print it |
| Credentials in the script | leaked secrets | use the standard credential locations |
| Forgetting pagination | only the first page (for S3, 1,000 items) | use paginators / the helpers |
| Assuming a key exists in a response | `KeyError` (e.g. empty `Contents`) | `.get("Contents", [])` |
| Catching nothing | stack trace on expired credentials | catch the SDK's error types |
| `ImportError` with Azure | old tutorial or a missing package | check the package list above |
| Reading OCI results without `.data` | you get the response wrapper | use `.data` |
| Using the same credential in dev and prod | accidents | separate profiles/accounts |
| Testing against production | real changes | use moto or a sandbox |

## 8. Practice (in order)

1. **Mock first:** run `t5_boto3_mock.py`. Add a third bucket and a fourth instance, and see the output change.
2. **Mock:** write `find_untagged(instances)` (a pure function) that returns instances whose name is `"(no name)"`, and add a test in the mock script.
3. **Mock:** add a function that lists only objects larger than 10 bytes using a list comprehension.
4. **Day 27:** save the instance list to CSV with `csv.DictWriter`, then load it into Pandas and chart instances per state.
5. **Day 28:** turn `t5_boto3.py` into a CLI with subcommands (`buckets`, `instances --state running`).
6. **Real account (read-only, when ready):** run `t5_boto3.py` or `t5_azure.py` or `t5_oci.py` against a **sandbox** account and read the output.
7. **Track 2:** serve the instance summary as a FastAPI `/instances` endpoint.
8. **Mini-project:** an inventory script that writes `inventory.json` (Day 19) with every resource, name, state and owner tag, plus a "needs attention" list.

## 9. Self-check

- What is an SDK, and what does it do for you?
- Why must credentials never appear in your code?
- What is pagination, and what goes wrong if you ignore it?
- Which calls would you run first on an unfamiliar account, and why?
- What does `ClientError` tell you that `NoCredentialsError` does not?
- Why can you test the boto3 code without an AWS account?
- Name two things that are different between the three SDKs and two that are the same.

---

## You have finished the advanced path

| Track | What you can now do |
|-------|---------------------|
| Core (21 to 28) | write concise Python, wrap functions, stream data, manage environments, call APIs, convert data files, ship CLIs |
| Data Science | analyse tables with Pandas, compute with NumPy, plot with Matplotlib |
| Web | serve pages and APIs with Flask, FastAPI or Django |
| Automation | scrape pages and drive a browser |
| AI/ML | train and evaluate models with scikit-learn and PyTorch |
| Cloud/DevOps | inventory and audit AWS, Azure and OCI from code |

**Best next step:** combine tracks on a project from your own work: for example, **cloud inventory → Pandas analysis → FastAPI dashboard**. Real projects that use two or three tracks together are where this becomes durable skill.
