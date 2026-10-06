"""Track 5d example: OCI SDK for Python (READ-ONLY).

Run:    python3 learning-path/advanced/examples/t5_oci.py [--profile DEFAULT] [--compartment <ocid>]
Needs:  pip install oci     and a config file at ~/.oci/config
Create the config with:  oci setup config   (the OCI CLI), or follow Oracle's
"SDK and CLI configuration file" docs. The file holds the path to your private
key. NEVER copy keys, fingerprints or OCIDs-with-secrets into this script.

This script only LISTS things. It creates, changes and deletes nothing.
"""

import argparse

import oci
from oci.exceptions import ConfigFileNotFound, InvalidConfig, ProfileNotFound, ServiceError


# BLOCK 1: load the config file and check it is complete
def load_config(profile="DEFAULT"):
    config = oci.config.from_file(oci.config.DEFAULT_LOCATION, profile)
    oci.config.validate_config(config)         # raises InvalidConfig if a field is missing
    return config


# BLOCK 2: who am I? Identity API: the user in the config
def whoami(config):
    identity = oci.identity.IdentityClient(config)
    user = identity.get_user(config["user"]).data
    return {"name": user.name, "email": user.email, "state": user.lifecycle_state}


# BLOCK 3: regions this tenancy is subscribed to
def list_regions(config):
    identity = oci.identity.IdentityClient(config)
    subs = identity.list_region_subscriptions(config["tenancy"]).data
    return [(s.region_name, s.status, s.is_home_region) for s in subs]


# BLOCK 4: compartments: OCI's folders for organising and permissioning resources.
# list_call_get_all_results follows the "next page" token for you.
def list_compartments(config):
    identity = oci.identity.IdentityClient(config)
    result = oci.pagination.list_call_get_all_results(
        identity.list_compartments, config["tenancy"]
    )
    return [(c.name, c.lifecycle_state, c.id) for c in result.data]


# BLOCK 5: compute instances in one compartment
def list_instances(config, compartment_id, state=None):
    compute = oci.core.ComputeClient(config)
    kwargs = {"lifecycle_state": state} if state else {}
    result = oci.pagination.list_call_get_all_results(
        compute.list_instances, compartment_id, **kwargs
    )
    return [
        {
            "name": i.display_name,
            "state": i.lifecycle_state,
            "shape": i.shape,
            "ad": i.availability_domain,
        }
        for i in result.data
    ]


# BLOCK 6: pure logic on the data (easy to test)
def count_by_state(instances):
    counts = {}
    for i in instances:
        counts[i["state"]] = counts.get(i["state"], 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Read-only OCI overview")
    parser.add_argument("--profile", default="DEFAULT")
    parser.add_argument("--compartment", help="compartment OCID (default: the tenancy root)")
    args = parser.parse_args()

    try:
        config = load_config(args.profile)
        print("Identity    :", whoami(config))
        print("Regions     :", list_regions(config))
        comps = list_compartments(config)
        print(f"Compartments: {len(comps)}")
        for name, state, _ in comps[:10]:
            print("  ", name, state)

        compartment = args.compartment or config["tenancy"]
        instances = list_instances(config, compartment)
        print(f"Instances in {compartment[:30]}...: {len(instances)}", count_by_state(instances))
        for i in instances[:10]:
            print("  ", i)
    except ConfigFileNotFound:
        print("No OCI config at ~/.oci/config. Create one with `oci setup config`.")
    except ProfileNotFound:
        print(f"Profile '{args.profile}' not found in the config file.")
    except InvalidConfig as e:
        print("The OCI config is incomplete or invalid:", e)
    except ServiceError as e:
        # e.status is the HTTP status; e.code is OCI's error name (e.g. NotAuthenticated)
        print(f"OCI rejected the request: {e.status} {e.code}: {e.message}")


if __name__ == "__main__":
    main()
